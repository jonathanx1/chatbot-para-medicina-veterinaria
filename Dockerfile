FROM python:3.11-slim

# Instala las librerías nativas que WeasyPrint necesita
RUN apt-get update && apt-get install -y \
    libcairo2 libpango-1.0-0 libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 libffi7 libgobject-2.0-0 \
  && rm -rf /var/lib/apt/lists/*

# Crea y activa el entorno
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto de tu código
COPY . .

# Expón el puerto y arranca con Waitress
EXPOSE 5000
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "app:app"]
