from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from sky_engine import generate_sky
import os

app = FastAPI(title="Sky Map API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, cambia a tu dominio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================
# Servir frontend
# ========================
frontend_path = os.path.join(os.path.dirname(__file__), "../sky_frontend")
app.mount("/static", StaticFiles(directory=os.path.join(frontend_path)), name="static")

@app.get("/")
def index():
    return FileResponse(os.path.join(frontend_path, "index.html"))

# ========================
# API
# ========================
class SkyRequest(BaseModel):
    lat: float
    lon: float
    datetime_utc: str  # Format: YYYY-MM-DD HH:MM:SS o ISO

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

# ========================
# Run locally
# ========================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)