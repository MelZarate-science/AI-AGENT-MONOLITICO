# -*- coding: utf-8 -*-
"""
Servicio de preprocesamiento de texto.

Este módulo contiene funciones para la limpieza y normalización
básica de texto de entrada del usuario.
"""

import re

def preprocess_text(texto: str) -> str:
    """
    Realiza una limpieza y normalización básica del texto.

    El objetivo es estandarizar el texto de entrada sin alterar
    significativamente su contenido o significado.

    - Elimina espacios en blanco al inicio y al final.
    - Reemplaza múltiples espacios/saltos de línea con un solo espacio.

    Args:
        text: El texto de entrada del usuario.

    Returns:
        El texto preprocesado.
    """
    if not isinstance(texto, str):
        return ""

    # Eliminar espacios al inicio y al final
    processed_text = texto.strip()

    # Reemplazar múltiples espacios, tabulaciones y saltos de línea con un solo espacio
    processed_text = re.sub(r'\s+', ' ', processed_text)

    return processed_text
