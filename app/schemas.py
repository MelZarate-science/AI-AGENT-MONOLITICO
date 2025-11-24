# -*- coding: utf-8 -*-
"""
Modelos de datos (esquemas) para la validación de entradas y salidas de la API.

Este módulo utiliza Pydantic para definir los esquemas de datos que FastAPI
usará para validar las solicitudes (`requests`) y formatear las respuestas (`responses`).
"""

from pydantic import BaseModel, HttpUrl
from enum import Enum

class Formato(str, Enum):
    """Formatos de narrativa permitidos."""
    POST_SOCIAL = "Post Social"
    STORYTELLING_IMPACTO = "Storytelling de Impacto"
    RESUMEN_CASO = "Resumen de Caso"

class Tono(str, Enum):
    """Tonos de narrativa permitidos."""
    INSPIRACIONAL = "Inspiracional"
    EDUCATIVO = "Educativo"
    TECNICO = "Técnico"

class StoryRequest(BaseModel):
    """
    Esquema para la solicitud de creación de una historia.
    Valida los datos de entrada del endpoint /story.
    """
    image_url: HttpUrl
    user_text: str
    formato: Formato
    tono: Tono

    class Config:
        json_schema_extra = {
            "example": {
                "image_url": "https://images.unsplash.com/photo-1517329782489-94932c444a6e",
                "user_text": "Una reflexión sobre la importancia de la perseverancia.",
                "formato": "Post Social",
                "tono": "Inspiracional"
            }
        }

class StoryResponse(BaseModel):
    """
    Esquema para la respuesta de la creación de una historia.
    Define la estructura de la respuesta del endpoint /story.
    """
    story_id: str
    narrative: str

    class Config:
        json_schema_extra = {
            "example": {
                "story_id": "sto_a1b2c3d4e5f6",
                "narrative": "En el camino de la vida, cada paso cuenta. La perseverancia es la luz que guía nuestros sueños..."
            }
        }
