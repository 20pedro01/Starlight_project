import astropy.units as u
from astropy.coordinates import SkyCoord, AltAz
from astroquery.vizier import Vizier



# Fallback stars (Sirius, Canopus, Rigil Kentaurus, Arcturus, Vega, Capella, Rigel, Procyon, Achernar, Betelgeuse)
FALLBACK_STARS = [
    {"name": "Sirius", "alt_deg": 45, "az_deg": 180, "magnitude": -1.46},
    {"name": "Canopus", "alt_deg": 30, "az_deg": 190, "magnitude": -0.74},
    {"name": "Rigil Kentaurus", "alt_deg": 20, "az_deg": 170, "magnitude": -0.27},
    {"name": "Arcturus", "alt_deg": 60, "az_deg": 90, "magnitude": -0.05},
    {"name": "Vega", "alt_deg": 70, "az_deg": 270, "magnitude": 0.03},
    {"name": "Capella", "alt_deg": 50, "az_deg": 320, "magnitude": 0.08},
    {"name": "Rigel", "alt_deg": 40, "az_deg": 200, "magnitude": 0.13},
    {"name": "Procyon", "alt_deg": 55, "az_deg": 150, "magnitude": 0.34},
    {"name": "Betelgeuse", "alt_deg": 42, "az_deg": 195, "magnitude": 0.50},
    {"name": "Altair", "alt_deg": 65, "az_deg": 290, "magnitude": 0.77},
]

def get_visible_stars(time, location, mag_limit=6.0):
    try:
        Vizier.ROW_LIMIT = -1
        Vizier.columns = ["HIP", "_RA.icrs", "_DE.icrs", "Vmag"]

        catalog = Vizier.query_constraints(
            catalog="I/239/hip_main",
            Vmag=f"<{mag_limit}"
        )[0]

        # Coordenadas ecuatoriales
        stars = SkyCoord(
            ra=catalog["_RA.icrs"],
            dec=catalog["_DE.icrs"],
            frame="icrs"
        )

        # Conversión a Alt/Az
        altaz = stars.transform_to(
            AltAz(obstime=time, location=location)
        )

        # Solo estrellas sobre el horizonte
        mask = altaz.alt.deg > 0

        visible_alt = altaz.alt.deg[mask]
        visible_az = altaz.az.deg[mask]
        visible_mag = catalog["Vmag"][mask]
        visible_hip = catalog["HIP"][mask]

        # Construcción del resultado
        return [
            {
                "name": f"HIP {hip}",
                "type": "star",
                "alt_deg": float(alt),
                "az_deg": float(az),
                "magnitude": float(mag)
            }
            for hip, alt, az, mag in zip(
                visible_hip,
                visible_alt,
                visible_az,
                visible_mag
            )
        ]
    except Exception as e:
        print(f"Error fetching stars from Vizier: {e}")
        # Return fallback stars placed somewhat randomly or just static for demo
        # Modify fallback to be roughly valid or just return them
        return FALLBACK_STARS
