from .sky_engine import generate_sky
import json

if __name__ == "__main__":
    # --- Configuración de lugar y tiempo ---
    lat = 20.689
    lon = -88.201
    datetime_utc = "2026-01-25 16:51:00"

    # --- Genera todo el cielo ---
    full_sky = generate_sky(
        lat=lat,
        lon=lon,
        datetime_utc=datetime_utc,
        mag_limit=6.0,
        force_all_constellations=True,
        include_all_solar_objects=False
    )

    # --- Información resumida ---
    print(f"Se encontraron {len(full_sky['stars'])} estrellas visibles")
    print(f"Se encontraron {len(full_sky['solar_system'])} objetos del sistema solar (Sol, Luna y planetas)")
    print(f"Se encontraron {len(full_sky['constellations'])} constelaciones")

