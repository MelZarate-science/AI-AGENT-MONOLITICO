# AutoStory-Builder-Prompt-Maestro

Este proyecto es un generador de narrativas automatizado que utiliza IA para crear historias basadas en una imagen y texto proporcionados por el usuario.

## Configuración del Entorno

### 1. Crear Entorno Virtual

Asegúrate de tener Python 3.10+ instalado.

```bash
python -m venv venv
```

### 2. Activar Entorno Virtual

**En Windows:**
```bash
venc\Scripts\activate
```

**En macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Instalar Dependencias

Instala las dependencias exactas del proyecto.

```bash
pip install -r requirements.txt
```

### 4. Configurar Variables de Entorno

Crea un archivo `.env` a partir del ejemplo y añade tus claves.

```bash
# En Windows (usa copy)
copy .env.example .env

# En macOS/Linux (usa cp)
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales de Supabase y Gemini.

## Ejecución

Para iniciar la aplicación, ejecuta Uvicorn desde la carpeta `autostory`:

```bash
uvicorn app.main:app --reload
```

La API estará disponible en `http://127.0.0.1:8000/docs`

## ⚠️ Solución de Problemas Comunes: Error de Compatibilidad de Websockets

Si al ejecutar la aplicación se encuentra un error relacionado con la librería `realtime` o `websockets` (ej. `ImportError: cannot import name 'ClientConnection'`), se debe a un problema de **compatibilidad** entre el código de un paquete de terceros y las versiones modernas de `websockets`.

Para resolverlo, es necesario aplicar una corrección manual directamente en el código fuente dentro del entorno virtual. Esta corrección debe realizarse solo una vez.

### 1. Ubicación del Archivo

Localiza y abre el siguiente archivo dentro de tu entorno virtual (`venv`):

venv/Lib/site-packages/realtime_async/client.py


### 2. Aplicación del Parche de Compatibilidad

Edita la **Línea 12** de este archivo para reemplazar la sintaxis obsoleta por la corrección necesaria.

| Descripción | Código Obsoleto (Línea 12) | Código Corregido (Línea 12) |
| :--- | :--- | :--- |
| **Sintaxis** | `from websockets.asyncio.client import ClientConnection` | `from websockets.client import WebSocketClientProtocol as ClientConnection` |

### 3. Impacto de la Corrección

Esta modificación resuelve el problema de la siguiente manera:

* Se utiliza la ruta de importación **correcta** para las clases de cliente en las versiones modernas de `websockets` (`websockets.client`).
* Se renombra la clase moderna (`WebSocketClientProtocol`) al nombre que el código de `realtime` esperaba (`ClientConnection`), resolviendo el `ImportError` y permitiendo que la aplicación se cargue correctamente con Uvicorn.