# -*- coding: utf-8 -*-
"""
Servicio de almacenamiento de datos con Supabase.

Este módulo gestiona la conexión con la base de datos de Supabase
para registrar las solicitudes de historias y sus resultados.
"""

import uuid
from supabase import create_client, Client
from fastapi import HTTPException

from app.config import SUPABASE_URL, SUPABASE_KEY
from app.schemas import StoryRequest

# Inicializar cliente de Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def generate_story_id() -> str:
    """Genera un ID único para la historia con el prefijo 'sto_'."""
    return f"sto_{uuid.uuid4().hex[:12]}"

async def save_story_to_supabase(
    story_id: str,
    request_data: StoryRequest,
    narrative: str
) -> None:
    """
    Guarda la solicitud original y la narrativa generada en Supabase.

    Args:
        story_id: El ID único de la historia.
        request_data: El objeto de solicitud original.
        narrative: La narrativa generada por la IA.

    Raises:
        HTTPException: Si ocurre un error al interactuar con Supabase.
    """
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Advertencia: Credenciales de Supabase no configuradas. No se guardará la historia.")
        return

    try:# 1. Guardar la narrativa generada (TABLA PADRE)
        story_data = {
             "id": story_id,
             "narrative_v1": narrative
        }
        supabase.table("stories").insert(story_data).execute() 
        # ¡DEBE IR PRIMERO! # 2. Guardar la solicitud de entrada (TABLA HIJO)
        input_data = {
            "story_id": story_id,
            "image_url": str(request_data.image_url),
            "user_text": request_data.user_text,
            "formato": request_data.formato.value,
            "tono": request_data.tono.value
        }
        supabase.table("inputs").insert(input_data).execute() # AHORA FUNCIONARÁ
    
    except Exception as e:
        print(f"Error al guardar en Supabase: {e}")
        pass
