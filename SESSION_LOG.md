# Session Log

## 2026-11-11 -- Web interface and static GitHub Pages site (branch `web-interface`)
- Added a FastAPI web app (`web/`, `run_web.py`, port 8104) and a static site build (`scripts/build_static.py`,
  `.github/workflows/pages.yml`) following the shared web kit.
- Pages: home, coffee origins, varieties, roasters, products, brewing methods + timer, regions map (inline SVG),
  guide and history (markdown rendered in JS), search across all tables, tasting journal (local only), about.
- Data is read through `coffee_database.CoffeeDatabase` with a read-only SQLite connection; the .db is never written.
- Search/filter rules live in `web/search.py` and are mirrored in `web/static/search_engine.js`; a test checks both
  give identical results on the full data.
- `coffee_journal.json` is personal tasting notes (currently empty): served only by the local app, never exported.
- Factored the continent outlines from `tabs/map_tab.py` into `world_shapes.py` (map tab now imports them).
- Local environment note: the anaconda base Python behind `.venv` is missing `libsqlite3.0.dylib`, so `import sqlite3`
  fails; tests were run with `DYLD_LIBRARY_PATH=/opt/anaconda3/pkgs/libsqlite-3.53.3-h1b79a29_0/lib`.
- Tests: `tests/test_web.py` 187 passed; `test_coffee_database.py` 7 passed; screenshots smoke test all ok.
