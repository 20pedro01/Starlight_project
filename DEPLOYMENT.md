# Guía de Despliegue (Deployment)

Para poner tu proyecto en internet, necesitas alojar el **Backend (Python)** y el **Frontend (HTML/JS)** en servidores. Como tu proyecto tiene dos partes distintas, lo ideal es usar servicios especializados para cada una.

Recomendación: **Render** (Backend) + **Netlify** (Frontend). Ambos tienen planes gratuitos.

---

## Paso 1: Preparar el Backend (Python)

1.  **Repositorio**: Asegúrate de que tu carpeta `sky_backend` y archivos raíz (`requirements.txt`, `Procfile`) estén en un repositorio de GitHub.
    *   *Nota: Si tienes todo en un solo repo, puedes configurar Render para buscar en la carpeta raíz.*
2.  **Crear servicio en Render.com**:
    *   Regístrate y selecciona "New Web Service".
    *   Conecta tu repositorio de GitHub.
    *   **Build Command**: `pip install -r sky_backend/requirements.txt`
    *   **Start Command**: `uvicorn sky_backend.app:app --host 0.0.0.0 --port $PORT`
    *   Despliega. Render te dará una URL (ej. `https://starlight-api.onrender.com`).

3.  **Probar**: Entra a `https://tu-url-render.com/docs` para ver si la API responde.

---

## Paso 2: Conectar Frontend con Backend

1.  Abre el archivo `sky_frontend/js/main.js` en tu editor.
2.  Busca la línea 1: `const API_URL = "http://localhost:8000/generate";`
3.  Cámbiala por la URL que te dio Render:
    ```javascript
    const API_URL = "https://starlight-api.onrender.com/generate";
    ```
4.  Guarda el cambio y súbelo a GitHub.

---

## Paso 3: Desplegar el Frontend (Web)

1.  **Netlify o Vercel**:
    *   Regístrate en **Netlify**.
    *   Arrastra tu carpeta `sky_frontend` al área de "Sites" (o conéctalo con GitHub seleccionando esa carpeta como raíz de publicación).
2.  **Listo**: Netlify te dará una URL (ej. `https://starlight-project.netlify.app`).

---

## Resumen de Archivos Clave para Depsliegue

*   `Procfile`: Le dice al servidor cómo arrancar tu Python. (Ya creado en la raíz).
*   `requirements.txt`: Lista de librerías necesarias. (Ya actualizado).
*   `sky_backend/`: Tu código Python.
