# Coffee Collection Explorer

See @INTERFACE.md for the project navigation map.

## Quick Start
```bash
pip install -r requirements.txt
python run_coffee_explorer.py
```

## Testing
```bash
python -m pytest test_coffee_database.py -v
python -m pytest -q tests/test_web.py      # web interface (pip install -r requirements-web.txt)
```

## Web interface
`python run_web.py` (port 8104); `python scripts/build_static.py` builds the GitHub Pages site. Keep
`web/search.py` and `web/static/search_engine.js` in step (parity test in tests/test_web.py).

See @SESSION_LOG.md for progress notes.
