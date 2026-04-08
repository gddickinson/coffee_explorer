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
| `coffee_guide.md` | Markdown content for the guide tab |
| `coffee_history.md` | Markdown content for the history tab |
| `test_coffee_database.py` | Smoke tests for database creation and queries |

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
```

## Data Files

- `coffee_collection.db` -- SQLite database (auto-created, in .gitignore)
- `coffee_journal.json` -- User tasting entries (in .gitignore)
