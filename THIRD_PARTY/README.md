# Third-party data

## ne_110m_land.json -- Natural Earth 1:110m Land

- **Source:** Natural Earth, "Land" at 1:110m scale (`ne_110m_land`), https://www.naturalearthdata.com/
  (file taken from the official repository, https://github.com/nvkelso/natural-earth-vector,
  `geojson/ne_110m_land.geojson`, downloaded 2026-11-11; SHA-256 of the downloaded GeoJSON
  `9e0729ee253ca7d7a5c4ae9395fb1902264c5377c52e224d13dd85010e2835d9`).
- **Licence:** public domain. "All versions of Natural Earth raster + vector map data found on this website are in
  the public domain" (https://www.naturalearthdata.com/about/terms-of-use/). No permission or attribution is required;
  credited here anyway: "Made with Natural Earth."
- **Changes:** converted by `scripts/convert_natural_earth.py` to a compact JSON list of polygons
  (`[outer ring, *hole rings]`, each a list of `[lon, lat]`), coordinates rounded to 0.01 degree, consecutive
  duplicate points removed. 127 polygons, 5129 points, about 77 kB.
- **Used by:** `world_shapes.py` -> the desktop Coffee Regions map tab (`tabs/map_tab.py`) and the web map
  (`/api/world`, `web/static/regions.js`).
