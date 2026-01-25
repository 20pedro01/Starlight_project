from astropy.time import Time
from astropy.coordinates import EarthLocation
import astropy.units as u

from stars import get_visible_stars
from solar_system import get_solar_system_objects
from constellations import get_constellations

def generate_sky(lat, lon, datetime_utc, mag_limit=6.0, force_all_constellations=True, include_all_solar_objects=True):
    """
    Genera un cielo completo con:
    - Estrellas visibles hasta mag_limit
    - Sol, Luna y planetas (opcional: include_all_solar_objects=True para incluir siempre)
    - Constelaciones (todas si force_all_constellations=True)
    """
    location = EarthLocation(lat=lat * u.deg, lon=lon * u.deg)
    time = Time(datetime_utc)

    # Estrellas visibles según el límite de magnitud
    stars = get_visible_stars(time, location, mag_limit)

    # Objetos del sistema solar
    solar_system = get_solar_system_objects(
        time,
        location,
        include_below_horizon=include_all_solar_objects
    )

    # Constelaciones
    constellations = get_constellations(
        time,
        location,
        force_all_segments=force_all_constellations
    )

    return {
        "metadata": {
            "lat": lat,
            "lon": lon,
            "datetime_utc": datetime_utc
        },
        "stars": stars,
        "solar_system": solar_system,
        "constellations": constellations
    }


