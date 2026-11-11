"""Web interface for Coffee Collection Explorer (FastAPI + plain ES-module front end).

Contents:
- app.py      FastAPI app: JSON API under /api, front end at /, STATIC_ENDPOINTS for the static site
- data.py     read-only access to coffee_collection.db through coffee_database.CoffeeDatabase
- search.py   search/filter rules for list endpoints (mirrored by static/search_engine.js)
- journal.py  tasting journal read/append (local server only, never exported)
- static/     index.html, theme, page modules, static_api.js for GitHub Pages
"""
