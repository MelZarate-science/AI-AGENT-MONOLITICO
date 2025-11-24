# -*- coding: utf-8 -*-
"""
Punto de entrada principal de la API AutoStory Builder.

Este módulo define la aplicación FastAPI y sus endpoints. Orquesta
el flujo completo de generación de historias.
"""

from fastapi import FastAPI, BackgroundTasks

from app.schemas import StoryRequest, StoryResponse
from app.services.image_processor import process_image_from_url
from app.services.text_processor import preprocess_text
from app.services.captioner import generate_captions_from_image
from app.services.generator import generate_narrative
from app.services.storage import generate_story_id, save_story_to_supabase

import time
from fastapi.requests import Request
from fastapi.responses import Response

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="AutoStory Builder API",
    description="Una API para generar narrativas creativas a partir de imágenes y texto.",
    version="1.0.0"
)

# 🌟 AÑADIR ESTE MIDDLEWARE 🌟
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    
    # 1. Métrica en Consola: Imprime la duración en la terminal de Uvicorn
    print(f"TIEMPO DE RESPUESTA: {process_time:.4f} segundos")
    
    # 2. Métrica en Header: Añade la duración a los encabezados de respuesta
    response.headers["X-Process-Time"] = str(process_time)
    
    return response

@app.post("/story", response_model=StoryResponse)
async def create_story_endpoint(request: StoryRequest, background_tasks: BackgroundTasks):
    """
    Endpoint principal para generar una nueva historia.

    Recibe una URL de imagen y texto, y devuelve una narrativa generada por IA.
    El proceso sigue el pipeline definido:
    1. Preprocesamiento de imagen y texto.
    2. Generación de captions para la imagen.
    3. Ensamblaje de prompt y generación de narrativa.
    4. Almacenamiento en segundo plano.
    """
    # 1. PREPROCESAMIENTO
    processed_image_bytes = await process_image_from_url(str(request.image_url))
    processed_text = preprocess_text(request.user_text)

    # 2. CAPTIONING
    image_captions = await generate_captions_from_image(processed_image_bytes)

    # 3. GENERACIÓN
    # (El ensamblaje del prompt se hace dentro de generate_narrative)
    final_narrative = await generate_narrative(
        image_captions=image_captions,
        user_text=processed_text,
        formato=request.formato,
        tono=request.tono
    )

    # 4. STORAGE (en segundo plano)
    story_id = generate_story_id()
    background_tasks.add_task(
        save_story_to_supabase,
        story_id=story_id,
        request_data=request,
        narrative=final_narrative
    )

    # 5. RESPUESTA
    return StoryResponse(story_id=story_id, narrative=final_narrative)

@app.get("/", summary="Health Check")
def read_root():
    """Endpoint de health check para verificar que la API está funcionando."""
    return {"status": "ok", "message": "Welcome to AutoStory Builder API"}
