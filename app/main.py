"""Punto de entrada principal de la API AutoStory Builder.

Este módulo define la aplicación FastAPI y sus endpoints. Orquesta
el flujo completo de generación de historias.
"""

from fastapi import FastAPI, BackgroundTasks, File, Form, UploadFile  # Se añade File, Form, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import Response
import httpx


from app.schemas import StoryResponse, Tono, Formato, EditNarrativeRequest    
from app.services.text_processor import preprocess_text
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
    image: UploadFile | None = File(None),
    texto: str | None = Form(None),
    formato: Formato = Form(...),
    tono: Tono = Form(...),
    background_tasks: BackgroundTasks = BackgroundTasks(),
):
    # --- Validación ---
    if not image and not texto:
        raise HTTPException(
            status_code=400,
            detail="Debes enviar una imagen o un texto para generar una historia."
        )

    # --- Imagen ---
    image_bytes = None
    if image:
        image_bytes = await image.read()

    # --- Texto ---
    processed_text = preprocess_text(texto) if texto else ""

    # --- Generación multimodal ---
    final_narrative = await generate_narrative(
        image_bytes=image_bytes,
        user_text=processed_text,
        formato=formato,
        tono=tono
    )

    # --- Versión 1.0 ---
    story_id = generate_story_id()

    background_tasks.add_task(
        save_story_to_supabase,
        story_id=story_id,
        image_url=None,            # Ya no se usa
        user_text=texto,
        formato=formato,
        tono=tono,
        narrative=final_narrative
    )

    return StoryResponse(
        story_id=story_id,
        narrative=final_narrative
    )

from app.services.storage import save_minor_version

@app.post("/save_edit")
async def save_edit(req: EditNarrativeRequest):

    result = await save_minor_version(
        story_id=req.story_id,
        narrative=req.narrative
    )

    return {
        "status": "ok",
        "version": f"{result['major']}.{result['minor']}",
        "message": "Versión guardada correctamente"
    }


@app.get("/", summary="Health Check")
def read_root():
    """Endpoint de health check para verificar que la API está funcionando."""
    return {"status": "ok", "message": "Welcome to AutoStory Builder API"}
