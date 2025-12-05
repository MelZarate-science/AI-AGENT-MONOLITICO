""" Servicio de construcción de prompts.

Este módulo ensambla el prompt final que se enviará al modelo de IA
generativa, combinando el contexto de la imagen, el texto del usuario
y las directivas de formato y tono.
"""

from app.schemas import Formato, Tono

def build_final_prompt(
    user_text: str,
    formato: Formato,
    tono: Tono
) -> str:
    """
    Construye el prompt final para el modelo de generación de texto.

    Args:
        image_captions: Descripción técnica de la imagen generada por Gemini Vision.
        user_text: Texto proporcionado por el usuario.
        formato: El formato de salida deseado (ej. Post Social).
        tono: El tono deseado para la narrativa (ej. Inspiracional).

    Returns:
        El prompt final como una única cadena de texto.
    """

    system_prompt = """
    Eres un experto en storytelling y redacción creativa. Tu tarea es generar una narrativa
    convincente y de alta calidad basada en el contexto proporcionado. Debes seguir
    estrictamente las directivas de formato y tono.
    """

    final_prompt = f"""
    {system_prompt}
    
    **Texto del Usuario (Idea Central):**
    ---
    {user_text}
    ---

    **Directivas de Generación:**
    ---
    1. **Formato Requerido:** {formato.value}
    2. **Tono de la Narrativa:** {tono.value}
    ---

    **Tarea:**
    Genera la narrativa final. No incluyas encabezados, solo el texto solicitado. La narrativa no debe exceder las 150 palabras.
    """

    return final_prompt.strip()
