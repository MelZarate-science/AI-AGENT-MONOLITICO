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

## Corrección Manual del Código Fuente

Dado que la instalación estándar de pip no podía resolver el error de código dentro del paquete de terceros, tuvimos que aplicar una solución de último recurso: modificar manualmente el código fuente del paquete defectuoso dentro de tu entorno virtual.

1. Identificación y Ubicación
Localizamos la línea de código problemática, que era la línea 12 del archivo: C:\Users\Angel\Desktop\autostory\venv\Lib\site-packages\realtime\_async\client.py

2. Aplicación del Parche de Compatibilidad (Doble Corrección)
Corregimos la sintaxis obsoleta de la siguiente manera:

Línea Original Rota:

Python

from websockets.asyncio.client import ClientConnection
Corrección Final Aplicada:

Python

from websockets.client import WebSocketClientProtocol as ClientConnection
Esta corrección hizo dos cosas:

Utilizó la ubicación correcta para las clases de cliente en las versiones modernas de websockets (websockets.client).

Renombró la clase moderna (WebSocketClientProtocol) a la clase que el código de realtime esperaba (ClientConnection), resolviendo así el ImportError final.

Al sincronizar manualmente la importación de realtime con tu versión actual de websockets, eliminamos el último obstáculo de compatibilidad, permitiendo que Uvicorn cargara tu aplicación con éxito.