# -*- coding: utf-8 -*-
"""
Servicio de almacenamiento de datos con Supabase (REST).

Este módulo registra las historias y sus inputs usando exclusivamente
la API REST de Supabase, evitando los problemas del antiguo cliente Python.
"""

import uuid
import httpx
from fastapi import HTTPException

from app.config import SUPABASE_URL, SUPABASE_KEY
from app.schemas import StoryRequest


def generate_story_id() -> str:
    """Genera un ID único con prefijo 'sto_'."""
    return f"sto_{uuid.uuid4().hex[:12]}"


async def save_story_to_supabase(story_id: str, request_data: StoryRequest, narrative: str) -> None:
    """
    Guarda la narrativa generada y los inputs originales en Supabase usando REST.

    Se realizan dos inserciones:
    1. Tabla stories  (padre)
    2. Tabla inputs   (hijo)
    """

    if not SUPABASE_URL or not SUPABASE_KEY:
        print("⚠ Advertencia: Variables de entorno de Supabase no configuradas.")
        return

    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"  # evita respuesta pesada
    }

    # ---- 1. Insert en tabla 'stories'
    story_payload = {
        "id": story_id,
        "narrative_v1": narrative
    }

    # ---- 2. Insert en tabla 'inputs'
    input_payload = {
        "story_id": story_id,
        "image_url": str(request_data.image_url),
        "user_text": request_data.user_text,
        "formato": request_data.formato.value,
        "tono": request_data.tono.value
    }

    async with httpx.AsyncClient() as client:
        # Insert historia
        r1 = await client.post(
            f"{SUPABASE_URL}/rest/v1/stories",
            headers=headers,
            json=story_payload
        )

        if r1.status_code >= 300:
            print("❌ Error guardando story:", r1.text)
            return

        # Insert inputs
        r2 = await client.post(
            f"{SUPABASE_URL}/rest/v1/inputs",
            headers=headers,
            json=input_payload
        )

        if r2.status_code >= 300:
            print("❌ Error guardando inputs:", r2.text)
            return

    print("✅ Datos guardados en Supabase correctamente.")
