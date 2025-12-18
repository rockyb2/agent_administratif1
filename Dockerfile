FROM python:3.11-slim

# Désactiver le buffering de Python
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Dossier de travail
WORKDIR /app

# Dépendances système minimales (compilateurs + libs pour psycopg2, reportlab, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libjpeg-dev \
    zlib1g-dev \
    curl \
  && rm -rf /var/lib/apt/lists/*

# Copier les dépendances Python
COPY requirements.txt .

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste du code de l'application
COPY . .

# Exposer le port FastAPI
EXPOSE 8000

# Commande de démarrage par défaut
CMD ["uvicorn", "mcp_server:app", "--host", "0.0.0.0", "--port", "8000"]
