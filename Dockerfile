# =========================
# Imagen base
# =========================
FROM python:3.11-slim

# =========================
# Crear usuario no root y carpeta de la app
# =========================
RUN useradd --create-home appuser
WORKDIR /app

# =========================
# Copiar e instalar dependencias
# =========================
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# =========================
# Copiar el backend y frontend
# =========================
COPY --chown=appuser:appuser sky_backend/ ./sky_backend/
COPY --chown=appuser:appuser sky_frontend/ ./sky_frontend/

# =========================
# Cambiar a usuario no root
# =========================
USER appuser

# =========================
# Exponer puerto (Cloud Run usa 8080)
# =========================
EXPOSE 8080

# =========================
# Comando para iniciar la app
# =========================
CMD ["uvicorn", "sky_backend.app:app", "--host", "0.0.0.0", "--port", "8080"]


