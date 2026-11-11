"""Read-only access to the coffee database for the web app.

The database location and schema come from the repo's own `coffee_database.CoffeeDatabase`; the web app only ever
opens the file read-only (SQLite `mode=ro`) and never writes to it. If the file is missing (a fresh checkout without
the tracked .db), it is built once by `CoffeeDatabase.initialize_database()` in a temporary cache directory, never in
the repo.
"""
import os
import sqlite3
import tempfile
from functools import lru_cache
from pathlib import Path

from coffee_database import CoffeeDatabase

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "coffee_collection.db"
GUIDE_PATH = ROOT / "coffee_guide.md"
HISTORY_PATH = ROOT / "coffee_history.md"

# table name -> (primary key column, display-name column)
TABLES = {
    "coffees": ("id", "name"),
    "varieties": ("id", "name"),
    "regions": ("id", "name"),
    "brewing_methods": ("id", "name"),
    "roasters": ("roaster_id", "roaster_name"),
    "products": ("product_id", "product_name"),
}

# The regions table and the coffees table spell one country differently.
COUNTRY_ALIASES = {"USA (Hawaii)": "United States (Hawaii)"}


def db_path() -> str:
    """Path of the SQLite file, building a temporary copy with the repo's own code if the tracked file is missing."""
    if DB_PATH.exists():
        return CoffeeDatabase(str(DB_PATH)).db_path
    cache = Path(tempfile.gettempdir()) / "coffee_explorer_web" / "coffee_collection.db"
    if not cache.exists():
        cache.parent.mkdir(parents=True, exist_ok=True)
        CoffeeDatabase(str(cache)).initialize_database()
    return str(cache)


def connect() -> sqlite3.Connection:
    """Read-only connection (the web app never modifies the database)."""
    uri = "file:" + Path(db_path()).as_posix() + "?mode=ro"
    conn = sqlite3.connect(uri, uri=True, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


@lru_cache(maxsize=None)
def table(name: str) -> tuple:
    """All rows of one table as dicts, ordered by display name (cached; the data is static)."""
    if name not in TABLES:
        raise KeyError(name)
    _pk, label = TABLES[name]
    conn = connect()
    try:
        rows = conn.execute(f"SELECT * FROM {name} ORDER BY {label} COLLATE NOCASE").fetchall()
    finally:
        conn.close()
    return tuple(dict(r) for r in rows)


def rows(name: str) -> list[dict]:
    return [dict(r) for r in table(name)]


def get(name: str, item_id: int) -> dict | None:
    pk = TABLES[name][0]
    return next((dict(r) for r in table(name) if r[pk] == item_id), None)


def roaster_names() -> dict:
    return {r["roaster_id"]: r["roaster_name"] for r in table("roasters")}


def products() -> list[dict]:
    """Products with their roaster's name attached and the flag columns as booleans."""
    names = roaster_names()
    out = []
    for p in table("products"):
        p = dict(p)
        p["roaster_name"] = names.get(p["roaster_id"], "")
        for k in ("organic", "fair_trade", "single_origin"):
            p[k] = bool(p[k])
        out.append(p)
    return out


def region_country(country: str) -> str:
    return COUNTRY_ALIASES.get(country, country)


def coffees_in_country(country: str) -> list[dict]:
    """Coffee origins grown in a region's country (regions and coffees share no key, so match on country)."""
    return [c for c in table("coffees") if region_country(c["origin_country"]) == country]


def _variety_mentions(variety_field: str, name: str) -> bool:
    """True if a coffee's free-text variety field lists this cultivar (e.g. "Caturra, Bourbon" lists Bourbon)."""
    base = name.split(" (")[0].split("/")[0].lower()
    parts = [p.strip().lower() for p in (variety_field or "").replace("/", ",").split(",")]
    return any(p == base or p.startswith(base + " ") or p.endswith(" " + base) for p in parts)


def coffees_with_variety(name: str) -> list[dict]:
    return [c for c in table("coffees") if _variety_mentions(c["variety"], name)]


def varieties_in_coffee(variety_field: str) -> list[dict]:
    return [v for v in table("varieties") if _variety_mentions(variety_field, v["name"])]


def stats() -> dict:
    return {"coffees": len(table("coffees")), "varieties": len(table("varieties")), "regions": len(table("regions")),
            "brewing_methods": len(table("brewing_methods")), "roasters": len(table("roasters")),
            "products": len(table("products")),
            "countries": len({c["origin_country"] for c in table("coffees")}),
            "roaster_countries": len({r["country_of_origin"] for r in table("roasters")})}


def read_markdown(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def env_path(var: str, default: Path) -> Path:
    return Path(os.environ.get(var) or default)
