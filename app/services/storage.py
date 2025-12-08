"""Servicio de almacenamiento de datos con Supabase (REST).

Este módulo registra las historias y sus inputs usando exclusivamente
la API REST de Supabase, evitando los problemas del antiguo cliente Python.
"""

import uuid
import httpx
from fastapi import HTTPException
from app.schemas import Formato, Tono
from app.config import SUPABASE_URL, SUPABASE_KEY
#from app.schemas import StoryRequest


def generate_story_id() -> str:
    """Genera un ID único con prefijo 'sto_'."""
    return f"sto_{uuid.uuid4().hex[:12]}"

async def save_story_to_supabase(
    story_id: str, 
    image_url: str | None,         
    user_text: str,
    formato: Formato,       # Tipo Formato (del Enum)
    tono: Tono,             # Tipo Tono (del Enum)
    narrative: str
) -> None:
    
    """
    Guarda:
    - story (id)
    - inputs (imagen, texto, formato, tono)
    - version v1.0 (narrative)
    """

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("⚠ Advertencia: Variables de entorno de Supabase no configuradas.")
        return

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal" 
    }

    async with httpx.AsyncClient() as client:

        # -------------------------
        # 1) Insert story raíz
        # -------------------------
        r1 = await client.post(
            f"{SUPABASE_URL}/rest/v1/stories",
            headers=headers,
            json={"id": story_id}
        )

        if r1.status_code >= 300:
            print("❌ Error guardando story:", r1.text)
            return

        # -------------------------
        # 2) Insert inputs originales
        # -------------------------
        r2 = await client.post(
            f"{SUPABASE_URL}/rest/v1/inputs",
            headers=headers,
            json={
                "story_id": story_id,
                "image_url": image_url,
                "user_text": user_text,
                "formato": formato.value,
                "tono": tono.value
            }
        )

        if r2.status_code >= 300:
            print("❌ Error guardando inputs:", r2.text)
            return

        # -------------------------
        # 3) Insert versión 1.0
        # -------------------------
        r3 = await client.post(
            f"{SUPABASE_URL}/rest/v1/story_versions",
            headers=headers,
            json={
                "story_id": story_id,
                "major": 1,
                "minor": 0,
                "narrative": narrative
            }
        )

        if r3.status_code >= 300:
            print("❌ Error guardando versión:", r3.text)
            return

    print("✅ Story, inputs y v1.0 guardados correctamente.")

async def save_minor_version(
    story_id: str,
    narrative: str
) -> dict:
    """
    Busca la última versión (major, minor)
    y guarda una nueva versión minor += 1.
    """

    if not SUPABASE_URL or not SUPABASE_KEY:
        raise HTTPException(500, "Supabase no configurado")

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:

        # 1) Obtener última versión
        query = (
            f"{SUPABASE_URL}/rest/v1/story_versions"
            f"?story_id=eq.{story_id}"
            f"&order=major.desc,minor.desc"
            f"&limit=1"
        )

        r_latest = await client.get(query, headers=headers)
        if r_latest.status_code != 200:
            raise HTTPException(500, "Error buscando última versión")

        versions = r_latest.json()
        if not versions:
            raise HTTPException(404, "No existen versiones para este story_id")

        major = versions[0]["major"]
        minor = versions[0]["minor"]

        # 2) Nueva versión: incrementa el minor
        new_major = major
        new_minor = minor + 1

        payload = {
            "story_id": story_id,
            "major": new_major,
            "minor": new_minor,
            "narrative": narrative
        }

        r_insert = await client.post(
            f"{SUPABASE_URL}/rest/v1/story_versions",
            headers=headers,
            json=payload
        )

        if r_insert.status_code >= 300:
            raise HTTPException(500, f"Error guardando nueva versión: {r_insert.text}")

    return {
        "major": new_major,
        "minor": new_minor
    }

async def get_story_versions(story_id: str) -> list[dict]:
    """
    Obtiene todas las versiones de una historia de Supabase.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise HTTPException(500, "Supabase no configurado")

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        query = (
            f"{SUPABASE_URL}/rest/v1/story_versions"
            f"?story_id=eq.{story_id}"
            f"&order=major.desc,minor.desc"
        )

        response = await client.get(query, headers=headers)

        if response.status_code != 200:
            raise HTTPException(500, "Error al obtener las versiones de la historia")

        return response.json()