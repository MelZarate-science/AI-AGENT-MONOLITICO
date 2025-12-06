import google.generativeai as genai
from app.config import GEMINI_API_KEY

if not GEMINI_API_KEY:
    raise RuntimeError("❌ GEMINI_API_KEY no está configurada en variables de entorno.")

# Inicializa el SDK una sola vez
genai.configure(api_key=GEMINI_API_KEY)

# Exportá un modelo para todos
model = genai.GenerativeModel("gemini-2.5-flash")
