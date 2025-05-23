FROM python:3.11-slim

# 1) Instala las dependencias nativas requeridas por WeasyPrint
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    libffi-dev \
    libglib2.0-0 \
  && rm -rf /var/lib/apt/lists/*

# 2) Instala tu app
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 3) Expón el puerto y arranca con waitress
EXPOSE 5000
CMD ["sh", "-c", "waitress-serve --host=0.0.0.0 --port=${PORT:-5000} app:app"]
