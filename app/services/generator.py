# -*- coding: utf-8 -*-
"""
Servicio de generación de narrativa con Gemini.

Este módulo utiliza el modelo de lenguaje de Gemini para generar
la narrativa final a partir de un prompt estructurado.
"""

import google.generativeai as genai
from fastapi import HTTPException

from app.config import GEMINI_API_KEY
from app.services.prompt_builder import build_final_prompt
from app.schemas import Formato, Tono

# La API de Gemini ya se configura en el módulo captioner.
# Si este módulo se usara de forma independiente, se necesitaría
# genai.configure(api_key=GEMINI_API_KEY) aquí también.

async def generate_narrative(
    image_captions: str,
    user_text: str,
    formato: Formato,
    tono: Tono
) -> str:
    """
    Genera una narrativa utilizando el modelo Gemini.

    Construye el prompt final y llama a la API de Gemini para obtener
    la narrativa v1.0.

    Args:
        image_captions: Descripción técnica de la imagen.
        user_text: Texto de entrada del usuario.
        formato: Formato de la narrativa.
        tono: Tono de la narrativa.

    Returns:
        La narrativa generada como una cadena de texto.

    Raises:
        HTTPException: Si ocurre un error durante la llamada a la API.
    """
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="La API Key de Gemini no está configurada."
        )

    try:
        # Construir el prompt final
        final_prompt = build_final_prompt(
            image_captions=image_captions,
            user_text=user_text,
            formato=formato,
            tono=tono
        )

        # Inicializar el modelo de texto
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Generar contenido
        response = await model.generate_content_async(final_prompt)

        return response.text

    except Exception as e:
        print(f"Error al generar narrativa con Gemini: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error en el servicio de IA al generar la narrativa: {e}"
        )
