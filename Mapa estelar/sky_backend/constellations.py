import json
import os
import urllib.request
from astropy.time import Time
from astropy.coordinates import SkyCoord, AltAz, EarthLocation
import astropy.units as u

# Carpeta y archivo de datos
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
DATA_FILE = "constellations.lines.json"  # ahora usamos las líneas
DATA_PATH = os.path.join(DATA_DIR, DATA_FILE)

# URL de constelaciones con líneas (d3-celestial)
CONSTELLATION_URL = f"https://raw.githubusercontent.com/ofrohn/d3-celestial/master/data/{DATA_FILE}"

def ensure_constellation_data():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    if not os.path.exists(DATA_PATH):
        print(f"Descargando {DATA_FILE}...")
        urllib.request.urlretrieve(CONSTELLATION_URL, DATA_PATH)
        print(f"{DATA_FILE} descargado correctamente.")

def get_constellations(time, location, force_all_segments=False):
    """
    Devuelve las constelaciones con líneas proyectadas en AltAz.
    time: astropy Time object
    location: astropy EarthLocation object
    force_all_segments: si True, devuelve todos los segmentos aunque estén debajo del horizonte
    """
    ensure_constellation_data()

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    constellations_list = []

    for feature in data.get("features", []):
        const_id = feature.get("id")
        geometry = feature.get("geometry", {})
        if geometry.get("type") != "MultiLineString":
            continue

        lines = []

        for segment in geometry.get("coordinates", []):
            ra_list = [p[0] for p in segment]  # RA en grados
            dec_list = [p[1] for p in segment]  # Dec en grados

            coords = SkyCoord(ra=ra_list*u.deg, dec=dec_list*u.deg, frame='icrs')
            altaz = coords.transform_to(AltAz(obstime=time, location=location))

            processed_segment = []
            visible_count = 0
            for alt, az in zip(altaz.alt.deg, altaz.az.deg):
                processed_segment.append({"alt": float(alt), "az": float(az)})
                if alt > 0:
                    visible_count += 1

            if visible_count > 0 or force_all_segments:
                lines.append(processed_segment)

        if lines:
            # Calculate Centroid
            # Flatten all points to find average RA/Dec
            all_ra = []
            all_dec = []
            for segment in geometry.get("coordinates", []):
                for p in segment:
                    all_ra.append(p[0])
                    all_dec.append(p[1])
            
            if all_ra:
                avg_ra = sum(all_ra) / len(all_ra)
                avg_dec = sum(all_dec) / len(all_dec)
                
                # Transform centroid to AltAz
                centroid_coord = SkyCoord(ra=avg_ra*u.deg, dec=avg_dec*u.deg, frame='icrs')
                centroid_altaz = centroid_coord.transform_to(AltAz(obstime=time, location=location))
                
                # Check visibility of centroid (optional, or pass if constellation is visible)
                # We add it if the constellation has lines
                
                from constellation_names import iau_names
                full_name = iau_names.get(const_id, const_id)
                
                constellations_list.append({
                    "id": const_id,
                    "name": full_name,
                    "centroid": {
                        "alt": float(centroid_altaz.alt.deg),
                        "az": float(centroid_altaz.az.deg),
                        "visible": bool(centroid_altaz.alt.deg > 0)
                    },
                    "lines": lines
                })
    
    return constellations_list

# --- Ejemplo de prueba ---
if __name__ == "__main__":
    time = Time("2026-01-25 16:51:00")
    location = EarthLocation(lat=20.689*u.deg, lon=-88.201*u.deg, height=10*u.m)

    consts = get_constellations(time, location, force_all_segments=True)
    print(f"Constelaciones encontradas: {len(consts)}")
    print(json.dumps(consts[:3], indent=2))  # muestra las 3 primeras para no saturar


