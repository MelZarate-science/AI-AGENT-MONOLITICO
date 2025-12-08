"""Modelos de datos (esquemas) para la validación de entradas y salidas de la API.

Este módulo utiliza Pydantic para definir los esquemas de datos que FastAPI
usará para validar las solicitudes (`requests`) y formatear las respuestas (`responses`).
"""

from pydantic import BaseModel, HttpUrl
from enum import Enum

class Formato(str, Enum):
    """Formatos de narrativa permitidos."""
    POST_SOCIAL = "Post social"
    STORYTELLING_IMPACTO = "Storytelling de impacto"
    RESUMEN_CASO = "Resumen de caso"

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

class EditNarrativeRequest(BaseModel):
    story_id: str
    narrative: str

    class Config:
        json_schema_extra = {
            "example": {
                "story_id": "sto_a1b2c3d4e5f6",
                "narrative": "Una versión editada y mejorada de la narrativa original."
            }
        }

class StoryVersion(BaseModel):
    major: int
    minor: int
    narrative: str
    created_at: str

class StoryVersionList(BaseModel):
    versions: list[StoryVersion]

class ExportFormat(str, Enum):
    """Formatos de exportación permitidos."""
    PDF = "pdf"
    HTML = "html"

    @classmethod
    def _missing_(cls, value):
        # Permite la coincidencia de formato sin importar mayúsculas/minúsculas
        for member in cls:
            if member.value.lower() == value.lower():
                return member
        return None

class ExportRequest(BaseModel):
    narrative: str
    format: ExportFormat
