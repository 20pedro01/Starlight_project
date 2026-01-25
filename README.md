# ✨ Starlight Project

**Starlight** es una aplicación web interactiva que permite generar mapas estelares personalizados y precisos para cualquier fecha y lugar. Ideal para capturar la alineación de las estrellas en momentos memorables.

![Starlight Preview](sky_frontend/assets/preview_placeholder.png) <!-- Opcional: Agrega una captura si tienes -->

## 🚀 Características

*   **Precisión Astronómica**: Utiliza `astropy` y catálogos estelares reales (Hipparcos) para calcular la posición de estrellas, constelaciones y planetas.
*   **Diseño Premium**: Interfaz moderna con tema oscuro ("Deep Space") y efectos de cristal (Glassmorphism).
*   **Personalización Total**:
    *   Selección de fecha y hora exacta.
    *   Ubicación por búsqueda (nombre de ciudad) o selección en mapa interactivo (Leaflet).
    *   Mensaje dedicatoria personalizado.
*   **Formatos de Exportación**:
    *   📸 Imagen PNG de alta calidad.
    *   📄 Archivo PDF tamaño carta listo para imprimir.

## 📂 Estructura del Proyecto

```text
root/
│
├── DEPLOYMENT.md          # Guía detallada para desplegar en la nube
├── Procfile               # Configuración de arranque para Render/Heroku
├── README.md              # Este archivo
├── requirements.txt       # Dependencias de Python
│
├── sky_backend/           # Lógica del Servidor (Python/FastAPI)
│   ├── data/              # Datos estáticos (ej. líneas de constelaciones)
│   ├── app.py             # Servidor API (FastAPI)
│   ├── constellations.py  # Módulo de cálculo de constelaciones
│   ├── constellation_names.py # Mapeo de nombres IAU
│   ├── main.py            # Script de prueba manual
│   ├── models.py          # Modelos de datos
│   ├── sky_engine.py      # Motor principal de generación
│   ├── solar_system.py    # Cálculo de planetas, Sol y Luna
│   └── stars.py           # Consulta de catálogo estelar
│
└── sky_frontend/          # Interfaz de Usuario (HTML/JS/CSS)
    ├── assets/            # Imágenes y recursos estáticos
    ├── css/
    │   └── style.css      # Estilos globales y responsivos
    ├── js/
    │   └── main.js        # Lógica de dibujo en Canvas y conexión API
    ├── index.html         # Página principal (Generador)
    └── about.html         # Página "Sobre Nosotros"
```

## 🛠️ Instalación y Uso Local

### Prerrequisitos
*   **Python 3.10+** instalado.
*   Navegador web moderno.

### 1. Configurar el Backend (API)

Abre una terminal en la carpeta raíz del proyecto:

1.  **Instalar dependencias**:
    ```bash
    pip install -r sky_backend/requirements.txt
    ```

2.  **Iniciar el servidor**:
    ```bash
    uvicorn sky_backend.app:app --reload
    ```
    *El servidor iniciará en `http://127.0.0.1:8000`.*

### 2. Iniciar el Frontend (Web)

1.  Ve a la carpeta `sky_frontend`.
2.  Abre el archivo `index.html` en tu navegador (doble clic).
3.  ¡Listo! La web se conectará automáticamente a tu servidor local.

## 🌍 Despliegue (Deployment)

Para subir el proyecto a internet (Railway, Render, Netlify), consulta el archivo **[DEPLOYMENT.md](DEPLOYMENT.md)** incluido en este repositorio.

## 📜 Licencia

© 2026 Starlight Project.
Creado por Pedro Cauich.

