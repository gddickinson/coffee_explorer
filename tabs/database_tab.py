"""
Coffee Explorer - Database browser tab.

Provides the main coffee origins browser with search and detail view.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sqlite3


class DatabaseTabMixin:
    """Mixin providing the Coffee Database tab and its handlers."""

    def create_database_tab(self):
        """Create the coffee database browser tab."""
        db_frame = ttk.Frame(self.notebook)
        self.notebook.add(db_frame, text="Coffee Database")

        # Search frame
        search_frame = ttk.Frame(db_frame)
        search_frame.pack(fill='x', padx=10, pady=10)

        ttk.Label(search_frame, text="Search:").pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(side='left', padx=5)
        self.search_entry.bind('<KeyRelease>', self.on_search)

        ttk.Label(search_frame, text="Roast Level:").pack(side='left', padx=(20, 5))
        self.roast_var = tk.StringVar(value="All")
        roast_combo = ttk.Combobox(search_frame, textvariable=self.roast_var,
                                   values=["All", "Light", "Medium", "Dark"],
                                   state='readonly', width=15)
        roast_combo.pack(side='left', padx=5)
        roast_combo.bind('<<ComboboxSelected>>', self.on_search)

        ttk.Button(search_frame, text="Clear", command=self.clear_search).pack(side='left', padx=5)

        # Main content frame
        content_frame = ttk.Frame(db_frame)
        content_frame.pack(fill='both', expand=True, padx=10, pady=5)

        # Left: Coffee list
        list_frame = ttk.Frame(content_frame)
        list_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))

        ttk.Label(list_frame, text="Coffee Origins", style='Header.TLabel').pack(anchor='w', pady=5)

        list_scroll_frame = ttk.Frame(list_frame)
        list_scroll_frame.pack(fill='both', expand=True)

        self.coffee_listbox = tk.Listbox(list_scroll_frame, font=('Arial', 10))
        list_scrollbar = ttk.Scrollbar(list_scroll_frame, orient='vertical',
                                       command=self.coffee_listbox.yview)
        self.coffee_listbox.configure(yscrollcommand=list_scrollbar.set)

        self.coffee_listbox.pack(side='left', fill='both', expand=True)
        list_scrollbar.pack(side='right', fill='y')

        self.coffee_listbox.bind('<<ListboxSelect>>', self.on_coffee_select)
        self.coffee_names = []

        # Right: Coffee details
        details_frame = ttk.Frame(content_frame)
        details_frame.pack(side='right', fill='both', expand=True)

        ttk.Label(details_frame, text="Coffee Details", style='Header.TLabel').pack(anchor='w', pady=5)

        self.details_text = scrolledtext.ScrolledText(details_frame, wrap=tk.WORD,
                                                      font=('Arial', 10), height=30)
        self.details_text.pack(fill='both', expand=True)

        self.details_text.tag_configure('title', font=('Arial', 16, 'bold'), foreground='#6F4E37')
        self.details_text.tag_configure('header', font=('Arial', 11, 'bold'), foreground='#4a4a4a')
        self.details_text.tag_configure('value', font=('Arial', 10))

        # Load initial data
        self.load_coffee_list()

    # ── Data loading and event handlers ──────────────────────────────

    def load_coffee_list(self, search_term='', roast='All'):
        """Load coffee list with optional filters."""
        self.coffee_listbox.delete(0, tk.END)
        self.coffee_names = []

        try:
            cursor = self.conn.cursor()
            query = "SELECT id, name, origin_country FROM coffees WHERE 1=1"
            params = []

            if roast != 'All':
                query += " AND roast_level LIKE ?"
                params.append(f'%{roast}%')

            if search_term:
                query += " AND (name LIKE ? OR origin_country LIKE ? OR flavor_profile LIKE ?)"
                params.extend([f'%{search_term}%'] * 3)

            query += " ORDER BY name"
            cursor.execute(query, params)
            rows = cursor.fetchall()

            for row in rows:
                display_name = f"{row['name']} ({row['origin_country']})"
                self.coffee_listbox.insert(tk.END, display_name)
                self.coffee_names.append(row['name'])

            if rows:
                self.coffee_listbox.select_set(0)
                self.on_coffee_select(None)

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading coffees: {e}")

    def on_search(self, event=None):
        search_term = self.search_var.get()
        roast = self.roast_var.get()
        self.load_coffee_list(search_term, roast)

    def clear_search(self):
        self.search_var.set('')
        self.roast_var.set('All')
        self.load_coffee_list()

    def on_coffee_select(self, event):
        selection = self.coffee_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        if index < len(self.coffee_names):
            coffee_name = self.coffee_names[index]
            self.current_coffee = coffee_name

            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM coffees WHERE name = ?", (coffee_name,))
                coffee = cursor.fetchone()
                if coffee:
                    self.display_coffee_details(coffee)
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error: {e}")

    def display_coffee_details(self, coffee):
        self.details_text.delete('1.0', tk.END)

        self.details_text.insert(tk.END, f"{coffee['name']}\n", 'title')
        self.details_text.insert(tk.END,
            f"{coffee['origin_country']} - {coffee['origin_region']}\n\n", 'header')

        self.details_text.insert(tk.END, "Variety & Processing\n", 'header')
        self.details_text.insert(tk.END, f"Variety: {coffee['variety']}\n", 'value')
        self.details_text.insert(tk.END, f"Processing: {coffee['processing_method']}\n", 'value')
        self.details_text.insert(tk.END, f"Roast Level: {coffee['roast_level']}\n\n", 'value')

        self.details_text.insert(tk.END, "Flavor Profile\n", 'header')
        self.details_text.insert(tk.END, f"{coffee['flavor_profile']}\n", 'value')
        self.details_text.insert(tk.END, f"Aroma: {coffee['aroma']}\n", 'value')
        self.details_text.insert(tk.END, f"Body: {coffee['body']}\n", 'value')
        self.details_text.insert(tk.END, f"Acidity: {coffee['acidity']}\n\n", 'value')

        self.details_text.insert(tk.END, "Growing Conditions\n", 'header')
        self.details_text.insert(tk.END,
            f"Altitude: {coffee['altitude_min']}-{coffee['altitude_max']} meters\n", 'value')
        self.details_text.insert(tk.END, f"Harvest: {coffee['harvest_season']}\n", 'value')
        self.details_text.insert(tk.END, f"Caffeine: {coffee['caffeine_content']}\n\n", 'value')

        if coffee['cupping_score']:
            self.details_text.insert(tk.END, "Quality\n", 'header')
            self.details_text.insert(tk.END,
                f"Cupping Score: {coffee['cupping_score']}/100\n\n", 'value')

        self.details_text.insert(tk.END, "Tasting Notes\n", 'header')
        self.details_text.insert(tk.END, f"{coffee['tasting_notes']}\n\n", 'value')

        self.details_text.insert(tk.END, "History\n", 'header')
        self.details_text.insert(tk.END, f"{coffee['history']}\n\n", 'value')

        self.details_text.insert(tk.END, "Price Range\n", 'header')
        self.details_text.insert(tk.END, f"{coffee['price_range']}\n", 'value')
