"""
Coffee Collection Explorer - Comprehensive GUI Application

A complete coffee database browser with advanced features including
database browsing, variety/cultivar lookup, roaster info, brewing methods
with timer, tasting journal, coffee guide, history, and world map.

Tab logic is split into mixin modules under tabs/ for maintainability.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os

from tabs import (
    DatabaseTabMixin,
    VarietiesTabMixin,
    RoastersTabMixin,
    BrewingTabMixin,
    JournalTabMixin,
    GuideTabMixin,
    MapTabMixin,
)


class CoffeeExplorerApp(
    DatabaseTabMixin,
    VarietiesTabMixin,
    RoastersTabMixin,
    BrewingTabMixin,
    JournalTabMixin,
    GuideTabMixin,
    MapTabMixin,
):
    """Main application class composing all tab mixins."""

    def __init__(self, root):
        self.root = root
        self.root.title("Coffee Collection Explorer")
        self.root.geometry("1400x900")

        # Database connection - use path relative to script location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(script_dir, "coffee_collection.db")
        self.conn = None
        self.connect_db()

        # File paths (reuse script_dir from above)
        self.journal_path = os.path.join(script_dir, "coffee_journal.json")
        self.guide_path = os.path.join(script_dir, "coffee_guide.md")
        self.history_path = os.path.join(script_dir, "coffee_history.md")

        # Load journal
        self.load_journal()

        # Timer state
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_thread = None

        # Current selections
        self.current_coffee = None
        self.current_company = None

        # Create menu bar
        self.create_menu_bar()

        # Create notebook (tabbed interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=5, pady=5)

        # Create tabs (each method lives in a mixin)
        self.create_database_tab()
        self.create_varieties_tab()
        self.create_roasters_tab()
        self.create_brewing_tab()
        self.create_journal_tab()
        self.create_guide_tab()
        self.create_history_tab()
        self.create_map_tab()

        # Style configuration
        self.configure_styles()

        # Status bar
        self.create_status_bar()

    def connect_db(self):
        """Establish database connection."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            messagebox.showerror("Database Error",
                                 f"Could not connect to database: {e}")

    def create_menu_bar(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Journal (JSON)",
                              command=self.export_journal)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Coffee Database",
                              command=lambda: self.notebook.select(0))
        view_menu.add_command(label="Coffee Varieties",
                              command=lambda: self.notebook.select(1))
        view_menu.add_command(label="Coffee Roasters",
                              command=lambda: self.notebook.select(2))
        view_menu.add_command(label="Brewing Methods",
                              command=lambda: self.notebook.select(3))

        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_status_bar(self):
        self.status_bar = ttk.Label(self.root, text="Ready",
                                    relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.update_status()

    def update_status(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM coffees")
            coffee_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM varieties")
            variety_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM regions")
            region_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM roasters")
            roaster_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM products")
            product_count = cursor.fetchone()[0]

            journal_count = len(self.journal_entries)

            self.status_bar.config(
                text=(f"Database: {coffee_count} coffees | "
                      f"{variety_count} varieties | "
                      f"{region_count} regions | "
                      f"{roaster_count} roasters | "
                      f"{product_count} products | "
                      f"Journal: {journal_count} entries")
            )
        except (sqlite3.Error, AttributeError):
            self.status_bar.config(text="Ready")

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Timer.TLabel', font=('Arial', 48, 'bold'),
                         foreground='#6F4E37')
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))


def main():
    """Main entry point."""
    # Initialize database if needed, using path relative to script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, "coffee_collection.db")
    if not os.path.exists(db_path):
        import coffee_database
        db = coffee_database.CoffeeDatabase(db_path)
        db.initialize_database()

    root = tk.Tk()
    app = CoffeeExplorerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
