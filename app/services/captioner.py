# -*- coding: utf-8 -*-
"""
Servicio de "captioning" de imágenes utilizando Gemini.

Este módulo se conecta con la API de Google Gemini para generar
descripciones técnicas y objetivas de una imagen.
"""

import google.generativeai as genai
from PIL import Image
from io import BytesIO
from fastapi import HTTPException

from app.config import GEMINI_API_KEY

# Configurar la API de Gemini
try:
    genai.configure(api_key=GEMINI_API_KEY)
except Exception as e:
    print(f"Error al configurar la API de Gemini: {e}")
    # La aplicación no podrá funcionar sin la API.

async def generate_captions_from_image(image_bytes: bytes) -> str:
    """
    Genera captions técnicos para una imagen utilizando el modelo Gemini Vision.

    Args:
        image_bytes: Los bytes de la imagen procesada (formato JPEG).

    Returns:
        Una cadena de texto con los captions generados.

    Raises:
        HTTPException: Si ocurre un error durante la llamada a la API de Gemini.
    """
    if not GEMINI_API_KEY:
        raise HTTPException(
            status_code=500,
            detail="La API Key de Gemini no está configurada."
        )

    try:
        # Cargar la imagen desde los bytes
        img = Image.open(BytesIO(image_bytes))

        # Inicializar el modelo de visión
        model = genai.GenerativeModel('gemini-2.5-flash')

        # Prompt para solicitar descripciones técnicas y objetivas
        prompt = [
            "Analiza la siguiente imagen y proporciona una descripción técnica y objetiva. "
            "Enfócate en los elementos presentes, su composición, estilo visual y posibles connotaciones. "
            "Evita interpretaciones subjetivas o narrativas. "
            "Enumera los puntos clave de forma concisa.",
            img
        ]

        # Generar contenido
        response = await model.generate_content_async(prompt)

        return response.text

    except Exception as e:
        print(f"Error al generar captions con Gemini: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error en el servicio de IA al generar captions: {e}"
        )
