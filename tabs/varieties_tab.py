"""
Coffee Explorer - Varieties browser tab.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sqlite3


class VarietiesTabMixin:
    """Mixin providing the Coffee Varieties tab and its handlers."""

    def create_varieties_tab(self):
        varieties_frame = ttk.Frame(self.notebook)
        self.notebook.add(varieties_frame, text="Coffee Varieties")

        header_frame = ttk.Frame(varieties_frame)
        header_frame.pack(fill='x', padx=10, pady=10)
        ttk.Label(header_frame, text="Coffee Varieties & Cultivars",
                  style='Title.TLabel').pack(side='left')

        content_frame = ttk.Frame(varieties_frame)
        content_frame.pack(fill='both', expand=True, padx=10, pady=5)

        list_frame = ttk.Frame(content_frame)
        list_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        ttk.Label(list_frame, text="Variety List", style='Header.TLabel').pack(anchor='w', pady=5)

        list_scroll = ttk.Frame(list_frame)
        list_scroll.pack(fill='both', expand=True)

        self.variety_listbox = tk.Listbox(list_scroll, font=('Arial', 10))
        variety_scrollbar = ttk.Scrollbar(list_scroll, orient='vertical',
                                          command=self.variety_listbox.yview)
        self.variety_listbox.configure(yscrollcommand=variety_scrollbar.set)
        self.variety_listbox.pack(side='left', fill='both', expand=True)
        variety_scrollbar.pack(side='right', fill='y')
        self.variety_listbox.bind('<<ListboxSelect>>', self.on_variety_select)
        self.variety_names = []

        details_frame = ttk.Frame(content_frame)
        details_frame.pack(side='right', fill='both', expand=True)
        ttk.Label(details_frame, text="Variety Details", style='Header.TLabel').pack(anchor='w', pady=5)

        self.variety_details_text = scrolledtext.ScrolledText(details_frame, wrap=tk.WORD,
                                                              font=('Arial', 10), height=30)
        self.variety_details_text.pack(fill='both', expand=True)
        self.variety_details_text.tag_configure('title', font=('Arial', 16, 'bold'), foreground='#6F4E37')
        self.variety_details_text.tag_configure('header', font=('Arial', 11, 'bold'), foreground='#4a4a4a')
        self.variety_details_text.tag_configure('value', font=('Arial', 10))

        self.load_varieties()

    def load_varieties(self):
        self.variety_listbox.delete(0, tk.END)
        self.variety_names = []
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM varieties ORDER BY name")
            rows = cursor.fetchall()
            for row in rows:
                self.variety_listbox.insert(tk.END, row['name'])
                self.variety_names.append(row['name'])
            if rows:
                self.variety_listbox.select_set(0)
                self.on_variety_select(None)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading varieties: {e}")

    def on_variety_select(self, event):
        selection = self.variety_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        if index < len(self.variety_names):
            variety_name = self.variety_names[index]
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM varieties WHERE name = ?", (variety_name,))
                variety = cursor.fetchone()
                if variety:
                    self.display_variety_details(variety)
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error: {e}")

    def display_variety_details(self, variety):
        self.variety_details_text.delete('1.0', tk.END)
        self.variety_details_text.insert(tk.END, f"{variety['name']}\n", 'title')
        self.variety_details_text.insert(tk.END, f"{variety['species']}\n\n", 'header')

        self.variety_details_text.insert(tk.END, "Origin\n", 'header')
        self.variety_details_text.insert(tk.END, f"Country: {variety['origin_country']}\n", 'value')
        self.variety_details_text.insert(tk.END, f"Discovered: {variety['discovered_year']}\n\n", 'value')

        self.variety_details_text.insert(tk.END, "Characteristics\n", 'header')
        self.variety_details_text.insert(tk.END, f"{variety['characteristics']}\n\n", 'value')

        self.variety_details_text.insert(tk.END, "Flavor Notes\n", 'header')
        self.variety_details_text.insert(tk.END, f"{variety['flavor_notes']}\n\n", 'value')

        self.variety_details_text.insert(tk.END, "Disease Resistance\n", 'header')
        self.variety_details_text.insert(tk.END, f"{variety['disease_resistance']}\n\n", 'value')

        self.variety_details_text.insert(tk.END, "Yield\n", 'header')
        self.variety_details_text.insert(tk.END, f"{variety['yield']}\n\n", 'value')

        if variety['notes']:
            self.variety_details_text.insert(tk.END, "Additional Notes\n", 'header')
            self.variety_details_text.insert(tk.END, f"{variety['notes']}\n", 'value')
