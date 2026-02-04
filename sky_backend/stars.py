import astropy.units as u
from astropy.coordinates import SkyCoord, AltAz
from astroquery.vizier import Vizier


def get_visible_stars(time, location, mag_limit=6.0):
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
