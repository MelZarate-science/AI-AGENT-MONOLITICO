# -*- coding: utf-8 -*-
"""
Punto de entrada principal de la API AutoStory Builder.

Este módulo define la aplicación FastAPI y sus endpoints. Orquesta
el flujo completo de generación de historias.
"""

from fastapi import FastAPI, BackgroundTasks, File, Form, UploadFile  # Se añade File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import Response


from app.schemas import StoryResponse, Tono, Formato    
from app.services.image_processor import _process_image_in_memory
from app.services.text_processor import preprocess_text
from app.services.captioner import generate_captions_from_image
from app.services.generator import generate_narrative
from app.services.storage import generate_story_id, save_story_to_supabase

import time

# Inicializar la aplicación FastAPI
app = FastAPI(
    title="AutoStory Builder API",
    description="Una API para generar narrativas creativas a partir de imágenes y texto.",
    version="1.0.0"
)

app.add_middleware(
  CORSMiddleware,
  allow_origins=[
    "https://auto-story-builder-one.vercel.app",
    "https://id-preview--e5b4310e-df83-40ed-a563-fc6551a3d19e.lovable.app"
  ],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
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
async def create_story_endpoint(
    image_file: UploadFile = File(..., description="La imagen a procesar."), # Cambio 1
    user_text: str = Form(..., description="El texto central del usuario."),   # Cambio ,2
    formato: Formato = Form(..., description="El formato de la narrativa."),  # Cambio 3
    tono: Tono = Form(..., description="El tono de la narrativa."),         # Cambio 4
    background_tasks: BackgroundTasks = BackgroundTasks(),):

    # --- Lectura del archivo y Preprocesamiento ---
    
    # 1.1. Leer el archivo cargado en memoria (Async)
    image_bytes = await image_file.read()

    # 1. PREPROCESAMIENTO DE IMAGEN
    processed_image_bytes = _process_image_in_memory(image_bytes)

    if not processed_image_bytes:
        raise HTTPException(
            status_code=422,
            detail="No se pudo procesar la imagen. El archivo puede estar corrupto o en un formato no soportado."
        )

    # 2. PREPROCESAMIENTO DE TEXTO

    processed_text = preprocess_text(user_text)

    # 3. CAPTIONING
    image_captions = await generate_captions_from_image(processed_image_bytes)

    # 3. GENERACIÓN
    # (El ensamblaje del prompt se hace dentro de generate_narrative)
    final_narrative = await generate_narrative(
        image_captions=image_captions,
        user_text=processed_text,
        formato= formato,
        tono= tono
    )

    # 5. STORAGE (en segundo plano)
    story_id = generate_story_id()
    
    # ¡CORRECCIÓN CRÍTICA! 
    # Ya no se usa 'request', se pasan los argumentos individuales.
    # image_url usa el nombre del archivo como placeholder (Opción A).
    background_tasks.add_task(
        save_story_to_supabase,
        story_id=story_id,
        image_url=f"Uploaded File: {image_file.filename}", 
        user_text=user_text,
        formato=formato,
        tono=tono,
        narrative=final_narrative
    )

    # 6. RESPUESTA
    return StoryResponse(story_id=story_id, narrative=final_narrative)

@app.get("/", summary="Health Check")
def read_root():
    """Endpoint de health check para verificar que la API está funcionando."""
    return {"status": "ok", "message": "Welcome to AutoStory Builder API"}
