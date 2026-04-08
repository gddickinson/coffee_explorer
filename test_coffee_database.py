"""
Smoke tests for the coffee database module.

These tests verify that the database can be created, populated, and
queried without errors. They use a temporary in-memory database to
avoid touching the real data file.
"""

import os
import sys
import tempfile

import pytest

sys.path.insert(0, os.path.dirname(__file__))

from coffee_database import CoffeeDatabase


@pytest.fixture
def db_path(tmp_path):
    """Return a temporary database file path."""
    return str(tmp_path / "test_coffee.db")


@pytest.fixture
def populated_db(db_path):
    """Create and populate a temporary coffee database."""
    db = CoffeeDatabase(db_path)
    db.initialize_database()
    return db_path


class TestDatabaseCreation:
    def test_tables_created(self, db_path):
        db = CoffeeDatabase(db_path)
        db.connect()
        db.create_tables()
        # Verify core tables exist
        db.cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = {row[0] for row in db.cursor.fetchall()}
        assert "coffees" in tables
        assert "varieties" in tables
        assert "regions" in tables
        assert "brewing_methods" in tables
        assert "roasters" in tables
        assert "products" in tables
        db.close()

    def test_initialize_populates_data(self, populated_db):
        import sqlite3

        conn = sqlite3.connect(populated_db)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM coffees")
        assert cursor.fetchone()[0] > 0

        cursor.execute("SELECT COUNT(*) FROM varieties")
        assert cursor.fetchone()[0] > 0

        cursor.execute("SELECT COUNT(*) FROM regions")
        assert cursor.fetchone()[0] > 0

        cursor.execute("SELECT COUNT(*) FROM brewing_methods")
        assert cursor.fetchone()[0] > 0

        cursor.execute("SELECT COUNT(*) FROM roasters")
        assert cursor.fetchone()[0] > 0

        cursor.execute("SELECT COUNT(*) FROM products")
        assert cursor.fetchone()[0] > 0

        conn.close()

    def test_idempotent_init(self, db_path):
        """Running initialize_database twice should not duplicate data."""
        db = CoffeeDatabase(db_path)
        db.initialize_database()

        import sqlite3

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM coffees")
        count1 = cursor.fetchone()[0]
        conn.close()

        db2 = CoffeeDatabase(db_path)
        db2.initialize_database()

        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM coffees")
        count2 = cursor.fetchone()[0]
        conn.close()

        assert count1 == count2


class TestDatabaseQueries:
    def test_coffee_has_required_fields(self, populated_db):
        import sqlite3

        conn = sqlite3.connect(populated_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM coffees LIMIT 1")
        row = cursor.fetchone()
        assert row is not None
        assert row["name"]
        assert row["origin_country"]
        conn.close()

    def test_variety_has_species(self, populated_db):
        import sqlite3

        conn = sqlite3.connect(populated_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM varieties LIMIT 1")
        row = cursor.fetchone()
        assert row is not None
        assert row["species"]
        conn.close()

    def test_region_has_coordinates(self, populated_db):
        import sqlite3

        conn = sqlite3.connect(populated_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM regions LIMIT 1")
        row = cursor.fetchone()
        assert row is not None
        assert row["latitude"] is not None
        assert row["longitude"] is not None
        conn.close()

    def test_brewing_method_has_parameters(self, populated_db):
        import sqlite3

        conn = sqlite3.connect(populated_db)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM brewing_methods LIMIT 1")
        row = cursor.fetchone()
        assert row is not None
        assert row["grind_size"]
        assert row["water_temp_c"] is not None
        conn.close()
