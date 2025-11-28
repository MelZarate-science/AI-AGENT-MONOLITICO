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
