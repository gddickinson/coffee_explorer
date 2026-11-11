"""World land outlines for the coffee-region maps, and the equirectangular projection both maps use.

Shapes: Natural Earth 1:110m Land (public domain), stored compactly in THIRD_PARTY/ne_110m_land.json (see
THIRD_PARTY/README.md and scripts/convert_natural_earth.py). Pure Python with no GUI imports, shared by the Tkinter
map tab (tabs/map_tab.py) and the web app (web/app.py; web/static/regions.js uses the same projection).
"""
import json
from pathlib import Path

LAND_FILE = Path(__file__).resolve().parent / "THIRD_PARTY" / "ne_110m_land.json"


def _load():
    data = json.loads(LAND_FILE.read_text(encoding="utf-8"))
    return [[[tuple(p) for p in ring] for ring in poly] for poly in data["polygons"]], data["source"]


# Each polygon is [outer ring, *hole rings]; each ring a list of (lon, lat) in degrees.
LAND_POLYGONS, LAND_SOURCE = _load()


def project(lon: float, lat: float, width: float, height: float) -> tuple[float, float]:
    """Equirectangular: lon -180..180 -> x 0..width, lat 90..-90 -> y 0..height."""
    return (lon + 180.0) * width / 360.0, (90.0 - lat) * height / 180.0


def _in_ring(lon: float, lat: float, ring) -> bool:
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        (xi, yi), (xj, yj) = ring[i], ring[j]
        if (yi > lat) != (yj > lat) and lon < (xj - xi) * (lat - yi) / (yj - yi) + xi:
            inside = not inside
        j = i
    return inside


def on_land(lon: float, lat: float) -> bool:
    """True if the point lies on land in the 1:110m outlines (inside an outer ring and not in a hole)."""
    return any(_in_ring(lon, lat, outer) and not any(_in_ring(lon, lat, h) for h in holes)
               for outer, *holes in LAND_POLYGONS)
