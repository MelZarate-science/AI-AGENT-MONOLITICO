# -*- coding: utf-8 -*-
"""
Módulo de configuración para cargar variables de entorno.

Este módulo utiliza python-dotenv para cargar variables desde un archivo .env
y las expone para ser utilizadas en toda la aplicación.
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

def get_env_variable(var_name: str) -> str:
    """
    Obtiene una variable de entorno o lanza un error si no se encuentra.

    Args:
        var_name: El nombre de la variable de entorno.

    Returns:
        El valor de la variable de entorno.

    Raises:
        ValueError: Si la variable de entorno no está configurada.
    """
    value = os.getenv(var_name)
    if value is None:
        raise ValueError(f"La variable de entorno '{var_name}' no está configurada.")
    return value

# Variables de entorno requeridas
try:
    SUPABASE_URL: str = get_env_variable("SUPABASE_URL")
    SUPABASE_KEY: str = get_env_variable("SUPABASE_KEY")
    GEMINI_API_KEY: str = get_env_variable("GEMINI_API_KEY")
except ValueError as e:
    print(f"Error de configuración: {e}")
    # En un caso real, se debería terminar la aplicación aquí.
    SUPABASE_URL, SUPABASE_KEY, GEMINI_API_KEY = "", "", ""
