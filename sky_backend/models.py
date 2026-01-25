from dataclasses import dataclass

@dataclass
class SkyObject:
    name: str
    type: str          # star, sun, moon, planet
    alt_deg: float
    az_deg: float
    magnitude: float | None = None
