"""
Servicio de generación de narrativa con Gemini (multimodal).
"""

import google.generativeai as genai
from fastapi import HTTPException

from app.config import GEMINI_API_KEY
from app.services.gemini_client import model
from app.services.prompt_builder import build_final_prompt
from app.schemas import Formato, Tono


def _safe_extract_text(response):
    """Extractor robusto para evitar response.text vacío."""
    if hasattr(response, "text") and response.text:
        return response.text

    if hasattr(response, "candidates") and response.candidates:
        try:
            parts = response.candidates[0].content.parts
            text_parts = [p.text for p in parts if hasattr(p, "text")]
            if text_parts:
                return " ".join(text_parts)
        except:
            pass

    return ""


async def generate_narrative(
    image_bytes: bytes | None,
    user_text: str,
    formato: Formato,
    tono: Tono
) -> str:
    """
    Genera narrativa usando:
    - imagen (bytes) si existe
    - texto del usuario
    - formato
    - tono
    """

    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="La API Key de Gemini no está configurada."
        )

    try:
        model = genai.GenerativeModel("gemini-2.5-flash")

        # 1. Armado del prompt
        final_prompt = build_final_prompt(
            user_text=user_text,
            formato=formato,
            tono=tono
        )

        # 2. Inputs multimodales
        inputs = [final_prompt]

        if image_bytes:
            inputs.append({"mime_type": "image/jpeg", "data": image_bytes})

        # 3. Llamada al modelo
        response = await model.generate_content_async(inputs)

        # 4. Extracción robusta
        narrative = _safe_extract_text(response)

        if not narrative:
            raise HTTPException(
                status_code=500,
                detail="Gemini no devolvió texto utilizable."
            )

        return narrative

    except Exception as e:
        print(f"Error en generate_narrative: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error en servicio de IA: {str(e)}"
        )