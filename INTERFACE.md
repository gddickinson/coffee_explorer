# Coffee Collection Explorer -- Interface Map

## Project Structure

| File / Directory | Purpose |
|------------------|---------|
| `coffee_explorer.py` | Main app class (`CoffeeExplorerApp`), entry point |
| `coffee_database.py` | `CoffeeDatabase` -- schema creation and data population |
| `run_coffee_explorer.py` | Launcher script |
| `tabs/` | Tab mixin modules (one per notebook tab) |
| `tabs/database_tab.py` | `DatabaseTabMixin` -- coffee origins browser |
| `tabs/varieties_tab.py` | `VarietiesTabMixin` -- cultivar lookup |
| `tabs/roasters_tab.py` | `RoastersTabMixin` -- roaster/brand browser + products |
| `tabs/brewing_tab.py` | `BrewingTabMixin` -- brewing methods + countdown timer |
| `tabs/journal_tab.py` | `JournalTabMixin` -- tasting journal CRUD |
| `tabs/guide_tab.py` | `GuideTabMixin` -- coffee guide + history markdown viewer |
| `tabs/map_tab.py` | `MapTabMixin` -- interactive world map of regions |
| `world_shapes.py` | `CONTINENT_POLYGONS` -- simplified continent outlines (pure data; used by map tab and web map) |
| `coffee_guide.md` | Markdown content for the guide tab |
| `coffee_history.md` | Markdown content for the history tab |
| `test_coffee_database.py` | Smoke tests for database creation and queries |
| `run_web.py` | Starts the web app (uvicorn, http://127.0.0.1:8104) |
| `requirements-web.txt` | Pinned web/test dependencies |
| `web/app.py` | FastAPI app: `/api/*` routes, `STATIC_ENDPOINTS` exported to the static site, journal POST (local only) |
| `web/data.py` | Read-only DB access via `CoffeeDatabase` (`connect()` uses SQLite `mode=ro`), cross-links (coffee<->variety/region) |
| `web/search.py` | `SPECS`, `filter_rows()`, `facets()` -- search/filter rules for every list endpoint |
| `web/journal.py` | Tasting journal load/add (same JSON format as the desktop tab; `COFFEE_JOURNAL` env overrides the path) |
| `web/static/index.html`, `style.css`, `core.js` | Shell page, shared kit theme and router (kit files, unchanged) |
| `web/static/style_app.css` | Coffee accent colours and page styles |
| `web/static/main.js` | Registers lazy page modules, mode line, background, starts router |
| `web/static/ui.js` | `listPage()` (filterable lists synced to the URL), `kv()`, `sections()`, `crumb()` |
| `web/static/static_api.js` | Static site: answers `api()` from exported JSON; filters lists/search in the browser; journal -> needs server |
| `web/static/search_engine.js` | JS mirror of `web/search.py` (+ `search_engine.test.mjs`) |
| `web/static/markdown.js` | Tiny safe markdown renderer for guide/history (+ `markdown.test.mjs`) |
| `web/static/timer.js` | Brewing countdown timer, `parseBrewTime()` |
| `web/static/home.js` | Pages: home, search (all tables), about |
| `web/static/coffees.js`, `varieties.js`, `roasters.js`, `brewing.js`, `regions.js`, `guide.js`, `journal.js` | Pages: coffees/coffee, varieties/variety, roasters/roaster/products/product, brewing/method/timer, map/region, guide/history, journal |
| `web/static/background.js`, `icon.svg` | Animated background (off under reduced motion), favicon |
| `scripts/build_static.py` | Exports the static site to `site/` (all `STATIC_ENDPOINTS` as JSON) |
| `scripts/screenshots.py` | Playwright smoke test + README screenshots (`docs/img/`) |
| `tests/test_web.py` | Web tests: endpoints, filters, read-only DB, journal, static build, JS tests, JS/Python search parity |
| `.github/workflows/pages.yml` | Test, build and publish the static site on push to main |

## Key Classes

- **`CoffeeExplorerApp`** (`coffee_explorer.py`): Tkinter root window, menu bar, status bar. Composes all tab mixins via multiple inheritance.
- **`CoffeeDatabase`** (`coffee_database.py`): Creates SQLite tables and populates them with seed data (coffees, varieties, regions, roasters, products, brewing methods).

## Module Connections

```
run_coffee_explorer.py
  -> coffee_explorer.py (CoffeeExplorerApp)
       -> tabs/database_tab.py
       -> tabs/varieties_tab.py
       -> tabs/roasters_tab.py
       -> tabs/brewing_tab.py
       -> tabs/journal_tab.py
       -> tabs/guide_tab.py
       -> tabs/map_tab.py
  -> coffee_database.py (CoffeeDatabase, on first run)

run_web.py
  -> web/app.py -> web/data.py (-> coffee_database.CoffeeDatabase, read-only), web/search.py, web/journal.py
                -> world_shapes.py
  -> web/static/main.js -> page modules -> core.js api() -> /api/* (local) or static_api.js (GitHub Pages)
scripts/build_static.py -> web/app.py via TestClient -> site/api/*.json
```

## Data Files

- `coffee_collection.db` -- SQLite database (tracked in git; the web app opens it read-only)
- `coffee_journal.json` -- User tasting entries (tracked, currently empty; local only, never exported to the static site)
- `docs/img/` -- README screenshots of the web interface
