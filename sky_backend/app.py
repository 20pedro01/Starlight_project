from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from .sky_engine import generate_sky
import os

app = FastAPI(title="Sky Map API")

# ------------------------
# Configurar CORS
# ------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción cambia a tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# Servir frontend
# ------------------------
# Dentro del contenedor, sky_frontend está en /app/sky_frontend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "../sky_frontend")

# Montamos la carpeta completa como /static
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# Endpoints para HTML
@app.get("/")
def index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/about")
def about():
    return FileResponse(os.path.join(FRONTEND_DIR, "about.html"))

# ------------------------
# API
# ------------------------
class SkyRequest(BaseModel):
    lat: float
    lon: float
    datetime_utc: str  # Formato ISO o "YYYY-MM-DD HH:MM:SS"

@app.post("/generate")
def generate_sky_map(request: SkyRequest):
    try:
        data = generate_sky(
            lat=request.lat,
            lon=request.lon,
            datetime_utc=request.datetime_utc
        )
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ------------------------
# Run local
# ------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)

