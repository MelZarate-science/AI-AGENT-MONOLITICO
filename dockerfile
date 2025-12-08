FROM python:3.11-slim

# Dependencias del sistema necesarias para WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libcairo2 \
    libcairo2-dev \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libxml2 \
    libxslt1.1 \
    shared-mime-info \
    fonts-dejavu-core \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Variables de entorno recomendadas
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

# Directorio de trabajo
WORKDIR /app

# Copiar proyecto
COPY . .

# Instalar dependencias Python
RUN pip install --no-cache-dir -r requirements.txt

# Crear usuario no root
RUN useradd -m appuser
USER appuser

# Exponer puerto
EXPOSE 10000

# Ejecutar backend
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
