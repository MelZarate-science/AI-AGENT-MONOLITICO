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
    formato: Formato,
    tono: Tono,
    narrative: str
):
    """
    Crea una historia NUEVA.
    Determina automáticamente:
    - major version = siguiente disponible (1, 2, 3…)
    - minor = 0
    """

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("⚠ Supabase no configurado.")
        return

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:

        # 1) Obtener mayor versión existente
        query = (
            f"{SUPABASE_URL}/rest/v1/story_versions"
            "?select=major"
            "&order=major.desc"
            "&limit=1"
        )
        r = await client.get(query, headers=headers)

        if r.status_code != 200:
            raise HTTPException(500, "Error obteniendo versión mayor")

        data = r.json()

        if data:
            next_major = data[0]["major"] + 1
        else:
            next_major = 1

        # minor siempre arranca en 0
        next_minor = 0

        # 2) Insert story raíz
        await client.post(
            f"{SUPABASE_URL}/rest/v1/stories",
            headers=headers,
            json={"id": story_id}
        )

        # 3) Insert inputs
        await client.post(
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

        # 4) Insert versión mayor real
        await client.post(
            f"{SUPABASE_URL}/rest/v1/story_versions",
            headers=headers,
            json={
                "story_id": story_id,
                "major": next_major,
                "minor": next_minor,
                "narrative": narrative
            }
        )

    print(f"✅ Historia guardada como v{next_major}.{next_minor}")

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