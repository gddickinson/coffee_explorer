"""Tasting journal for the local web app: same file and entry format as the desktop Journal tab
(tabs/journal_tab.py): a JSON list of {coffee_name, date, rating, brewing, notes}.

The journal holds the user's own tasting notes, so it is served only by the local server and never exported to the
static site. Set COFFEE_JOURNAL to use another file (the tests do).
"""
import json
from datetime import datetime

from .data import ROOT, env_path

DEFAULT_PATH = ROOT / "coffee_journal.json"


def path():
    return env_path("COFFEE_JOURNAL", DEFAULT_PATH)


def _read() -> list[dict]:
    """Entries in file order; a missing, empty or corrupt file counts as an empty journal (as in the desktop app)."""
    p = path()
    try:
        entries = json.loads(p.read_text(encoding="utf-8")) if p.exists() else []
    except (json.JSONDecodeError, OSError, ValueError):
        entries = []
    if not isinstance(entries, list):
        entries = []
    return entries


def load() -> list[dict]:
    """Entries, newest first."""
    return sorted(_read(), key=lambda e: e.get("date", ""), reverse=True)


def add(coffee_name: str, rating: int, brewing: str = "", notes: str = "") -> dict:
    coffee_name = (coffee_name or "").strip()
    if not coffee_name:
        raise ValueError("Please select a coffee")
    if not 1 <= int(rating) <= 5:
        raise ValueError("Rating must be 1-5")
    entry = {"coffee_name": coffee_name, "date": datetime.now().strftime("%Y-%m-%d %H:%M"), "rating": int(rating),
             "brewing": (brewing or "").strip(), "notes": (notes or "").strip()}
    entries = _read()
    entries.append(entry)
    path().write_text(json.dumps(entries, indent=2, ensure_ascii=False), encoding="utf-8")
    return entry
