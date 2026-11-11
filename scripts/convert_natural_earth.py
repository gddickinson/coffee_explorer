"""Convert Natural Earth ne_110m_land.geojson to THIRD_PARTY/ne_110m_land.json: polygons of (lon, lat) rounded to 0.01 deg.

Run: python -I scripts/convert_natural_earth.py <ne_110m_land.geojson> THIRD_PARTY/ne_110m_land.json
"""
import json, sys
src, dst = sys.argv[1], sys.argv[2]
g = json.load(open(src))
def clean(r):
    ring = []
    for lon, lat in r:
        p = [round(lon, 2), round(lat, 2)]
        if not ring or ring[-1] != p:
            ring.append(p)
    return ring if len(ring) >= 4 else None

polygons = []
for f in g["features"]:
    geom = f["geometry"]
    polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
    for poly in polys:
        rings = [r for r in map(clean, poly) if r]
        if rings and len(rings[0]) >= 4:
            polygons.append(rings)
out = {"source": "Natural Earth 1:110m Land (ne_110m_land), public domain, https://www.naturalearthdata.com/",
       "version": "nvkelso/natural-earth-vector master, downloaded 2026-11-11",
       "note": "polygons as [outer ring, *hole rings]; coordinates (lon, lat) rounded to 0.01 degree", "polygons": polygons}
json.dump(out, open(dst, "w"), separators=(",", ":"))
print(len(g["features"]), "features ->", len(polygons), "polygons,", sum(len(r) for p in polygons for r in p), "points,", sum(len(p) - 1 for p in polygons), "holes")
