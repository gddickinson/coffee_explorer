# Coffee Collection Explorer -- Roadmap

## Current State
A feature-rich Tkinter GUI application with SQLite backend for exploring coffee varieties, roasters, brewing methods, and regions. Contains 29 coffee origins, 20 varieties, 28 roasters, 61+ products, and 12 brewing methods. Includes tasting journal, brewing timer, interactive world map, coffee guide, and coffee history. Three Python files: `coffee_database.py` (DB setup/population), `coffee_explorer.py` (main GUI), and `run_coffee_explorer.py` (launcher). Database auto-created on first run.

## Short-term Improvements
- [x] Add `requirements.txt` (Pillow is the only external dependency)
- [x] Split `coffee_explorer.py` into separate tab modules if it exceeds 500 lines (likely very large)
- [ ] Split `coffee_database.py` into schema definition and data population modules
- [x] Add error handling for corrupt `coffee_journal.json` on load
- [ ] Add input validation for tasting journal entries (empty fields, invalid ratings)
- [x] Remove hardcoded database path; use relative path from script location

## Feature Enhancements
- [ ] Add export to CSV/Excel for coffee database and tasting journal
- [ ] Implement coffee comparison tool (side-by-side origin/roaster comparison)
- [ ] Add photo support for tasting journal entries
- [ ] Implement price tracking and purchase history
- [ ] Add flavor wheel visualization using matplotlib embedded in Tkinter
- [ ] Create cupping scoresheet form following SCA protocol
- [ ] Add dark mode theme option

## Long-term Vision
- [ ] Migrate from Tkinter to a web UI (Flask/FastAPI + HTMX) for multi-device access
- [ ] Add barista recipe calculator (grind size, water temp, ratio by method)
- [ ] Implement community features -- share tasting notes, compare with other users
- [ ] Add API integration with coffee roaster websites for live pricing
- [ ] Support importing data from other coffee tracking apps
- [ ] Create a mobile-friendly Progressive Web App version

## Technical Debt
- [x] `coffee_explorer.py` is almost certainly a single monolithic file with all tab logic -- must split
- [ ] `coffee_database.py` contains both schema and hardcoded data -- separate data into JSON/YAML fixtures
- [ ] `coffee_guide.md` and `coffee_history.md` are loaded at runtime as raw markdown -- add proper rendering
- [x] `coffee_collection.db` is tracked in version control -- add to `.gitignore`
- [ ] `coffee_journal.json` is user data mixed with source code -- store in user home directory
- [x] No tests for database queries or GUI behavior
