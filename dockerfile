FROM python:3.11-slim

# Dependencias del sistema para WeasyPrint (Debian 12/Trixie)
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2 \
    libcairo2-dev \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    libxml2 \
    libxslt1.1 \
    shared-mime-info \
    fonts-dejavu-core \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Config
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 10000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "10000"]
