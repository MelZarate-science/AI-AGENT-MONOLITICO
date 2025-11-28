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
venv\Scripts\activate
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

