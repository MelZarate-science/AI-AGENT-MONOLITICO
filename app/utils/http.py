# -*- coding: utf-8 -*-
"""
Utilidades HTTP para descargar recursos de forma segura.

Este módulo proporciona funciones para interactuar con recursos externos,
principalmente para la descarga de imágenes.
"""

import httpx
from typing import Optional

async def download_image_async(image_url: str) -> Optional[bytes]:
    """
    Descarga la imagen con una sola solicitud GET y valida el Content-Type.
    """
    allowed_content_types = ["image/jpeg", "image/png", "image/webp", "image/gif"]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            # 1. HACER SOLO LA SOLICITUD GET
            response = await client.get(image_url, headers=headers, follow_redirects=True)
            
            # 2. Verificar el estado HTTP
            response.raise_for_status() 

            # 3. Validar Content-Type
            content_type = response.headers.get("content-type")
            if content_type not in allowed_content_types:
                print(f"Error: Tipo de contenido no permitido: {content_type}")
                return None
            
            # 4. Devolver el contenido si todo es correcto
            return response.content

    except httpx.HTTPStatusError as e:
        print(f"Error de estado HTTP (GET) al descargar: {e.response.status_code}. URL: {image_url}")
        return None
    except httpx.RequestError as e:
        print(f"Error de red/timeout al descargar: {e}. URL: {image_url}")
        return None
    except Exception as e:
        print(f"Error inesperado al descargar la imagen: {e}")
        return None