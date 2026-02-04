from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from .sky_engine import generate_sky
import os

# Rate limiting
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Inicializar rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(title="Sky Map API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ------------------------
# Configurar CORS
# ------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://starlight-project-911911786039.europe-west1.run.app",
        "http://localhost:8080",  # Para desarrollo local
        "http://127.0.0.1:8080"   # Para desarrollo local
    ],
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
@limiter.limit("10/minute")  # Máximo 10 peticiones por minuto por IP
def generate_sky_map(request: Request, sky_request: SkyRequest):
    try:
        data = generate_sky(
            lat=sky_request.lat,
            lon=sky_request.lon,
            datetime_utc=sky_request.datetime_utc
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

