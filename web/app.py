"""FastAPI web app for Coffee Collection Explorer: serves the front end in static/ and the JSON API under /api.

Run with `python run_web.py` (http://127.0.0.1:8104, local only). Data is read (read-only) from coffee_collection.db
via web/data.py. `scripts/build_static.py` exports every path in STATIC_ENDPOINTS to JSON for the GitHub Pages site,
so keep that list in step with the GET routes below. List endpoints with query parameters are answered on the static
site by static_api.js filtering the exported full lists (same rules as web/search.py). The journal is local-only.
"""
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from world_shapes import CONTINENT_POLYGONS  # noqa: E402

from . import data, journal  # noqa: E402
from .search import SPECS, facets, filter_rows  # noqa: E402

STATIC = Path(__file__).resolve().parent / "static"

app = FastAPI(title="Coffee Collection Explorer")
app.mount("/static", StaticFiles(directory=STATIC), name="static")

# API kind -> database table (products get their roaster's name attached by data.products()).
KIND_TABLE = {"coffees": "coffees", "varieties": "varieties", "regions": "regions", "brewing": "brewing_methods",
              "roasters": "roasters", "products": "products"}


def kind_rows(kind: str) -> list[dict]:
    return data.products() if kind == "products" else data.rows(KIND_TABLE[kind])


def listing(kind: str, request: Request) -> list[dict]:
    return filter_rows(kind, kind_rows(kind), dict(request.query_params))


def one(kind: str, item_id: int) -> dict:
    pk = SPECS[kind]["id"]
    row = next((r for r in kind_rows(kind) if r[pk] == item_id), None)
    if row is None:
        raise HTTPException(404, f"unknown {kind} id {item_id}")
    return row


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(STATIC / "index.html")


@app.get("/api/stats")
def stats():
    return data.stats()


@app.get("/api/facets")
def all_facets():
    """Filter options with counts for every list page."""
    return {kind: facets(kind, kind_rows(kind)) for kind in KIND_TABLE}


@app.get("/api/coffees")
def coffees(request: Request):
    return listing("coffees", request)


@app.get("/api/coffees/{item_id}")
def coffee(item_id: int):
    c = one("coffees", item_id)
    regions = [r for r in data.rows("regions") if r["country"] == data.region_country(c["origin_country"])]
    return {**c, "regions": regions, "varieties": data.varieties_in_coffee(c["variety"])}


@app.get("/api/varieties")
def varieties(request: Request):
    return listing("varieties", request)


@app.get("/api/varieties/{item_id}")
def variety(item_id: int):
    v = one("varieties", item_id)
    return {**v, "coffees": data.coffees_with_variety(v["name"])}


@app.get("/api/regions")
def regions(request: Request):
    return listing("regions", request)


@app.get("/api/regions/{item_id}")
def region(item_id: int):
    r = one("regions", item_id)
    return {**r, "coffees": data.coffees_in_country(r["country"])}


@app.get("/api/brewing")
def brewing(request: Request):
    return listing("brewing", request)


@app.get("/api/brewing/{item_id}")
def brewing_method(item_id: int):
    return one("brewing", item_id)


@app.get("/api/roasters")
def roasters(request: Request):
    return listing("roasters", request)


@app.get("/api/roasters/{item_id}")
def roaster(item_id: int):
    r = one("roasters", item_id)
    return {**r, "products": [p for p in data.products() if p["roaster_id"] == item_id]}


@app.get("/api/products")
def products(request: Request):
    return listing("products", request)


@app.get("/api/products/{item_id}")
def product(item_id: int):
    return one("products", item_id)


@app.get("/api/world")
def world():
    """Continent outlines (lon, lat) from world_shapes.py plus the region markers, for the SVG map."""
    regs = [{k: r[k] for k in ("id", "name", "country", "latitude", "longitude")} for r in data.rows("regions")]
    return {"continents": {k: [list(p) for p in v] for k, v in CONTINENT_POLYGONS.items()}, "regions": regs}


@app.get("/api/content/{name}")
def content(name: str):
    paths = {"guide": data.GUIDE_PATH, "history": data.HISTORY_PATH}
    if name not in paths:
        raise HTTPException(404, "unknown content")
    return {"name": name, "markdown": data.read_markdown(paths[name])}


@app.get("/api/search")
def search(q: str = ""):
    """Search every table at once (empty q returns nothing)."""
    if not q.strip():
        return {kind: [] for kind in KIND_TABLE}
    return {kind: filter_rows(kind, kind_rows(kind), {"q": q}) for kind in KIND_TABLE}


# --- local-only: tasting journal (personal notes; never exported to the static site) -----------------------------
class JournalEntry(BaseModel):
    coffee_name: str
    rating: int = 3
    brewing: str = ""
    notes: str = ""


@app.get("/api/journal")
def journal_list():
    return {"entries": journal.load(), "coffees": [c["name"] for c in data.rows("coffees")]}


@app.post("/api/journal")
def journal_add(entry: JournalEntry):
    try:
        return journal.add(entry.coffee_name, entry.rating, entry.brewing, entry.notes)
    except ValueError as e:
        raise HTTPException(400, str(e))


def _detail_paths() -> list[str]:
    out = []
    for kind in KIND_TABLE:
        pk = SPECS[kind]["id"]
        out += [f"/{kind}/{r[pk]}" for r in kind_rows(kind)]
    return out


# GET paths (without the /api prefix) written to the static site as api/<path>.json. The journal is deliberately absent.
STATIC_ENDPOINTS = (["/stats", "/facets", "/world", "/content/guide", "/content/history"]
                    + [f"/{kind}" for kind in KIND_TABLE] + _detail_paths())
