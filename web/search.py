"""Search and filter rules for every list endpoint.

Mirrored exactly by web/static/search_engine.js, which answers the same queries on the static site from the exported
full lists (tests/test_web.py checks that both give the same ids). Rules:
- `q`: split into words; every word must occur (case-insensitive substring) in the row's searchable text.
- exact filters: the column must equal the value; `contains` filters: case-insensitive substring (like the desktop
  app's `roast_level LIKE '%Light%'`); `flag` filters: value "1" keeps rows where the column is true.
"""

# kind -> searchable text fields, exact filters, contains filters, flag filters, id column
SPECS = {
    "coffees": {"text": ["name", "origin_country", "origin_region", "variety", "processing_method", "flavor_profile",
                         "aroma", "tasting_notes"],
                "exact": {"country": "origin_country"}, "contains": {"roast": "roast_level", "process": "processing_method"},
                "flag": {}, "id": "id"},
    "varieties": {"text": ["name", "species", "origin_country", "characteristics", "flavor_notes", "notes"],
                  "exact": {"species": "species"}, "contains": {}, "flag": {}, "id": "id"},
    "regions": {"text": ["name", "country", "climate", "soil_type", "famous_coffees", "description"],
                "exact": {"country": "country"}, "contains": {}, "flag": {}, "id": "id"},
    "brewing": {"text": ["name", "category", "grind_size", "equipment_needed", "flavor_characteristics", "description"],
                "exact": {"category": "category", "difficulty": "difficulty_level"}, "contains": {}, "flag": {},
                "id": "id"},
    "roasters": {"text": ["roaster_name", "parent_company", "headquarters_city", "country_of_origin", "roasting_style",
                          "certifications", "description"],
                 "exact": {"country": "country_of_origin", "segment": "market_segment"},
                 "contains": {"cert": "certifications"}, "flag": {}, "id": "roaster_id"},
    "products": {"text": ["product_name", "roaster_name", "coffee_type", "roast_level", "format", "special_features",
                          "countries_available"],
                 "exact": {"roaster": "roaster_id", "type": "coffee_type", "roast": "roast_level",
                           "currency": "price_currency"},
                 "contains": {}, "flag": {"organic": "organic", "fair_trade": "fair_trade",
                                          "single_origin": "single_origin"}, "id": "product_id"},
}

# Facet columns shown as filter drop-downs (kind -> param -> column).
FACETS = {kind: {**spec["exact"], **{k: v for k, v in spec["contains"].items() if k != "cert"}}
          for kind, spec in SPECS.items()}
FACETS["roasters"]["cert"] = "certifications"


def _text(row: dict, fields: list[str]) -> str:
    return " ".join(str(row.get(f) or "") for f in fields).lower()


def filter_rows(kind: str, rows: list[dict], params: dict) -> list[dict]:
    spec = SPECS[kind]
    words = str(params.get("q") or "").lower().split()
    out = []
    for r in rows:
        if any(params.get(p) not in (None, "") and str(r.get(col)) != str(params[p]) for p, col in spec["exact"].items()):
            continue
        if any(params.get(p) and str(params[p]).lower() not in str(r.get(col) or "").lower()
               for p, col in spec["contains"].items()):
            continue
        if any(str(params.get(p) or "") == "1" and not r.get(col) for p, col in spec["flag"].items()):
            continue
        if words:
            text = _text(r, spec["text"])
            if not all(w in text for w in words):
                continue
        out.append(r)
    return out


def _cert_terms(value: str) -> list[str]:
    """'Organic (select), Direct trade' -> ['Organic', 'Direct Trade'] (normalised for a filter list)."""
    out = []
    for part in (value or "").split(","):
        t = part.split("(")[0].strip()
        if t:
            out.append(" ".join(w if w.isupper() or not w[:1].isalpha() else w[0].upper() + w[1:] for w in t.split()))
    return out


def facets(kind: str, rows: list[dict]) -> dict:
    """{param: {value: count}} for each filter of a kind, sorted by value."""
    out = {}
    for param, col in FACETS[kind].items():
        counts: dict = {}
        for r in rows:
            vals = _cert_terms(r.get(col)) if param == "cert" else [r.get(col)]
            for v in vals:
                if v not in (None, ""):
                    counts[str(v)] = counts.get(str(v), 0) + 1
        out[param] = dict(sorted(counts.items(), key=lambda kv: kv[0].lower()))
    return out
