# -*- coding: utf-8 -*-
"""
Servicio de procesamiento de imágenes.

Este módulo se encarga de descargar, validar, redimensionar y convertir
imágenes para su posterior análisis por modelos de IA.
"""

from PIL import Image, UnidentifiedImageError
from io import BytesIO
from typing import Optional
from fastapi import HTTPException

from app.utils.http import download_image_async

def _process_image_in_memory(image_bytes: bytes) -> Optional[bytes]:
    """
    Procesa una imagen en memoria: la convierte a RGB y la redimensiona.

    Esta es una operación síncrona y potencialmente intensiva en CPU.

    Args:
        image_bytes: Los bytes de la imagen original.

    Returns:
        Los bytes de la imagen procesada en formato JPEG, o None si hay un error.
    """
    try:
        with Image.open(BytesIO(image_bytes)) as img:
            # 1. Convertir a RGB para estandarizar el formato
            img_rgb = img.convert("RGB")

            # 2. Redimensionar a un máximo de 512x512 manteniendo el aspect ratio
            img_rgb.thumbnail((512, 512), Image.Resampling.LANCZOS)

            # 3. Guardar la imagen procesada en un buffer de bytes en formato JPEG
            buffer = BytesIO()
            img_rgb.save(buffer, format="JPEG")
            return buffer.getvalue()

    except UnidentifiedImageError:
        print("Error: No se pudo identificar el formato de la imagen.")
        return None
    except Exception as e:
        print(f"Error inesperado durante el procesamiento de la imagen: {e}")
        return None

async def process_image_from_url(image_url: str) -> bytes:
    """
    Orquesta la descarga y procesamiento de una imagen desde una URL.

    Args:
        image_url: La URL de la imagen a procesar.

    Returns:
        Los bytes de la imagen procesada.

    Raises:
        HTTPException: Si la imagen no se puede descargar o procesar.
    """
    # Descargar la imagen
    image_bytes = await download_image_async(image_url)
    if not image_bytes:
        raise HTTPException(
            status_code=400,
            detail="No se pudo descargar o validar la imagen desde la URL proporcionada."
        )

    # Procesar la imagen (FastAPI ejecutará esto en un threadpool si es necesario)
    processed_image_bytes = _process_image_in_memory(image_bytes)
    if not processed_image_bytes:
        raise HTTPException(
            status_code=422,
            detail="No se pudo procesar la imagen. El archivo puede estar corrupto o en un formato no soportado."
        )

    return processed_image_bytes
