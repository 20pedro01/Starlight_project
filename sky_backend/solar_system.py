import astropy.units as u
from astropy.coordinates import get_sun, get_body, AltAz

PLANETS = ["mercury", "venus", "mars", "jupiter", "saturn", "uranus", "neptune"]

def get_solar_system_objects(time, location, include_below_horizon=False):
    objects = []

    # ☀️ Sol
    sun = get_sun(time).transform_to(AltAz(obstime=time, location=location))
    if include_below_horizon or sun.alt.deg > 0:
        objects.append({
            "name": "Sun",
            "type": "sun",
            "alt_deg": float(sun.alt.deg),
            "az_deg": float(sun.az.deg)
        })

    # 🌙 Luna
    moon = get_body("moon", time, location).transform_to(
        AltAz(obstime=time, location=location)
    )
    if include_below_horizon or moon.alt.deg > 0:
        objects.append({
            "name": "Moon",
            "type": "moon",
            "alt_deg": float(moon.alt.deg),
            "az_deg": float(moon.az.deg)
        })

    # 🪐 Planetas
    for planet in PLANETS:
        body = get_body(planet, time, location).transform_to(
            AltAz(obstime=time, location=location)
        )
        if include_below_horizon or body.alt.deg > 0:
            objects.append({
                "name": planet.capitalize(),
                "type": "planet",
                "alt_deg": float(body.alt.deg),
                "az_deg": float(body.az.deg)
            })

    return objects

