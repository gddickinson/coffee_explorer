"""
Coffee Explorer - Roasters/brands browser tab.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sqlite3


class RoastersTabMixin:
    """Mixin providing the Coffee Roasters tab and its handlers."""

    def create_roasters_tab(self):
        brands_frame = ttk.Frame(self.notebook)
        self.notebook.add(brands_frame, text="Coffee Roasters")

        header_frame = ttk.Frame(brands_frame)
        header_frame.pack(fill='x', padx=10, pady=10)
        ttk.Label(header_frame, text="Coffee Roasters & Brands",
                  style='Title.TLabel').pack(side='left')

        # Search and filters
        search_filter_frame = ttk.Frame(brands_frame)
        search_filter_frame.pack(fill='x', padx=10, pady=(0, 10))

        row1 = ttk.Frame(search_filter_frame)
        row1.pack(fill='x', pady=(0, 5))

        ttk.Label(row1, text="Search:").pack(side='left', padx=5)
        self.roaster_search_var = tk.StringVar()
        roaster_search = ttk.Entry(row1, textvariable=self.roaster_search_var, width=30)
        roaster_search.pack(side='left', padx=5)
        roaster_search.bind('<KeyRelease>', self.on_roaster_search)

        ttk.Label(row1, text="Country:").pack(side='left', padx=(20, 5))
        self.roaster_country_var = tk.StringVar(value="All")
        country_combo = ttk.Combobox(row1, textvariable=self.roaster_country_var,
                                     values=["All", "USA", "Italy", "UK", "Japan", "Australia"],
                                     state='readonly', width=15)
        country_combo.pack(side='left', padx=5)
        country_combo.bind('<<ComboboxSelected>>', self.on_roaster_search)

        ttk.Label(row1, text="Segment:").pack(side='left', padx=(20, 5))
        self.roaster_segment_var = tk.StringVar(value="All")
        segment_combo = ttk.Combobox(row1, textvariable=self.roaster_segment_var,
                                     values=["All", "mass-market", "premium", "specialty", "luxury"],
                                     state='readonly', width=15)
        segment_combo.pack(side='left', padx=5)
        segment_combo.bind('<<ComboboxSelected>>', self.on_roaster_search)

        ttk.Button(row1, text="Clear", command=self.clear_roaster_filters).pack(side='left', padx=(20, 5))

        # Main content
        content_frame = ttk.Frame(brands_frame)
        content_frame.pack(fill='both', expand=True, padx=10, pady=5)

        roasters_frame = ttk.Frame(content_frame)
        roasters_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        ttk.Label(roasters_frame, text="Roasters", style='Header.TLabel').pack(anchor='w', pady=5)

        roasters_scroll = ttk.Frame(roasters_frame)
        roasters_scroll.pack(fill='both', expand=True)

        self.roasters_listbox = tk.Listbox(roasters_scroll, font=('Arial', 10))
        roasters_scrollbar = ttk.Scrollbar(roasters_scroll, orient='vertical',
                                           command=self.roasters_listbox.yview)
        self.roasters_listbox.configure(yscrollcommand=roasters_scrollbar.set)
        self.roasters_listbox.pack(side='left', fill='both', expand=True)
        roasters_scrollbar.pack(side='right', fill='y')
        self.roasters_listbox.bind('<<ListboxSelect>>', self.on_roaster_select)
        self.roaster_data = []

        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side='right', fill='both', expand=True)

        details_label_frame = ttk.LabelFrame(right_panel, text="Roaster Information", padding=10)
        details_label_frame.pack(fill='both', expand=True, pady=(0, 5))

        self.roaster_details_text = scrolledtext.ScrolledText(details_label_frame, wrap=tk.WORD,
                                                              font=('Arial', 10), height=12)
        self.roaster_details_text.pack(fill='both', expand=True)
        self.roaster_details_text.tag_configure('company', font=('Arial', 16, 'bold'), foreground='#6F4E37')
        self.roaster_details_text.tag_configure('header', font=('Arial', 11, 'bold'), foreground='#4a4a4a')
        self.roaster_details_text.tag_configure('value', font=('Arial', 10))

        products_label_frame = ttk.LabelFrame(right_panel, text="Products", padding=10)
        products_label_frame.pack(fill='both', expand=True)

        products_scroll = ttk.Frame(products_label_frame)
        products_scroll.pack(fill='both', expand=True)

        self.products_listbox = tk.Listbox(products_scroll, font=('Arial', 9))
        products_scrollbar = ttk.Scrollbar(products_scroll, orient='vertical',
                                           command=self.products_listbox.yview)
        self.products_listbox.configure(yscrollcommand=products_scrollbar.set)
        self.products_listbox.pack(side='left', fill='both', expand=True)
        products_scrollbar.pack(side='right', fill='y')
        self.products_listbox.bind('<<ListboxSelect>>', self.on_product_select)
        self.current_products = []

        self.load_roasters()

    # ── Handlers ─────────────────────────────────────────────────────

    def load_roasters(self, search_term='', country='All', segment='All'):
        self.roasters_listbox.delete(0, tk.END)
        self.roaster_data = []
        try:
            cursor = self.conn.cursor()
            query = """
                SELECT roaster_id, roaster_name, country_of_origin, market_segment
                FROM roasters WHERE 1=1
            """
            params = []
            if country != 'All':
                query += " AND country_of_origin = ?"
                params.append(country)
            if segment != 'All':
                query += " AND market_segment = ?"
                params.append(segment)
            if search_term:
                query += " AND (roaster_name LIKE ? OR description LIKE ?)"
                params.extend([f'%{search_term}%'] * 2)
            query += " ORDER BY roaster_name"
            cursor.execute(query, params)
            rows = cursor.fetchall()
            for row in rows:
                display = f"{row['roaster_name']} ({row['country_of_origin']})"
                self.roasters_listbox.insert(tk.END, display)
                self.roaster_data.append({'id': row['roaster_id'], 'name': row['roaster_name']})
            if rows:
                self.roasters_listbox.select_set(0)
                self.on_roaster_select(None)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading roasters: {e}")

    def on_roaster_search(self, event=None):
        self.load_roasters(self.roaster_search_var.get(),
                           self.roaster_country_var.get(),
                           self.roaster_segment_var.get())

    def clear_roaster_filters(self):
        self.roaster_search_var.set('')
        self.roaster_country_var.set('All')
        self.roaster_segment_var.set('All')
        self.load_roasters()

    def on_roaster_select(self, event):
        selection = self.roasters_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        if index < len(self.roaster_data):
            roaster_id = self.roaster_data[index]['id']
            try:
                cursor = self.conn.cursor()
                cursor.execute("SELECT * FROM roasters WHERE roaster_id = ?", (roaster_id,))
                roaster = cursor.fetchone()
                if roaster:
                    self.display_roaster_details(roaster)
                    self.load_roaster_products(roaster_id)
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Error: {e}")

    def display_roaster_details(self, roaster):
        self.roaster_details_text.delete('1.0', tk.END)
        self.roaster_details_text.insert(tk.END, f"{roaster['roaster_name']}\n", 'company')
        self.roaster_details_text.insert(tk.END,
            f"{roaster['market_segment'].title()} Roaster\n\n", 'header')

        self.roaster_details_text.insert(tk.END, "Company Information\n", 'header')
        if roaster['parent_company']:
            self.roaster_details_text.insert(tk.END, f"Parent: {roaster['parent_company']}\n", 'value')
        self.roaster_details_text.insert(tk.END, f"Founded: {roaster['founded_year']}\n", 'value')
        self.roaster_details_text.insert(tk.END,
            f"Headquarters: {roaster['headquarters_city']}, {roaster['country_of_origin']}\n", 'value')
        if roaster['website']:
            self.roaster_details_text.insert(tk.END, f"Website: {roaster['website']}\n", 'value')
        self.roaster_details_text.insert(tk.END, "\n")

        if roaster['roasting_style']:
            self.roaster_details_text.insert(tk.END, "Roasting Style\n", 'header')
            self.roaster_details_text.insert(tk.END, f"{roaster['roasting_style']}\n\n", 'value')
        if roaster['certifications']:
            self.roaster_details_text.insert(tk.END, "Certifications\n", 'header')
            self.roaster_details_text.insert(tk.END, f"{roaster['certifications']}\n\n", 'value')
        if roaster['description']:
            self.roaster_details_text.insert(tk.END, "Description\n", 'header')
            self.roaster_details_text.insert(tk.END, f"{roaster['description']}\n", 'value')

    def load_roaster_products(self, roaster_id):
        self.products_listbox.delete(0, tk.END)
        self.current_products = []
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM products WHERE roaster_id = ? ORDER BY product_name",
                           (roaster_id,))
            products = cursor.fetchall()
            for product in products:
                price_str = (f"{product['price_currency']} {product['price']:.2f}"
                             if product['price'] else "N/A")
                display = f"{product['product_name']} - {product['roast_level']} - {price_str}"
                self.products_listbox.insert(tk.END, display)
                self.current_products.append(dict(product))
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading products: {e}")

    def on_product_select(self, event):
        selection = self.products_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        if index < len(self.current_products):
            product = self.current_products[index]

            popup = tk.Toplevel(self.root)
            popup.title(f"Product Details - {product['product_name']}")
            popup.geometry("500x400")
            popup.transient(self.root)

            details_text = scrolledtext.ScrolledText(popup, wrap=tk.WORD, font=('Arial', 10))
            details_text.pack(fill='both', expand=True, padx=10, pady=10)
            details_text.tag_configure('title', font=('Arial', 14, 'bold'), foreground='#6F4E37')
            details_text.tag_configure('header', font=('Arial', 11, 'bold'))
            details_text.tag_configure('value', font=('Arial', 10))

            details_text.insert(tk.END, f"{product['product_name']}\n\n", 'title')
            details_text.insert(tk.END, "Product Information\n", 'header')
            details_text.insert(tk.END, f"Type: {product['coffee_type'].title()}\n", 'value')
            details_text.insert(tk.END, f"Roast Level: {product['roast_level'].title()}\n", 'value')
            details_text.insert(tk.END, f"Format: {product['format']}\n", 'value')
            if product['weight_oz']:
                details_text.insert(tk.END,
                    f"Weight: {product['weight_oz']} oz ({product['weight_g']}g)\n\n", 'value')

            details_text.insert(tk.END, "Pricing & Availability\n", 'header')
            if product['price']:
                details_text.insert(tk.END,
                    f"Price: {product['price_currency']} {product['price']:.2f}\n", 'value')
            details_text.insert(tk.END, f"Available in: {product['countries_available']}\n\n", 'value')

            details_text.insert(tk.END, "Certifications\n", 'header')
            details_text.insert(tk.END, f"Organic: {'Yes' if product['organic'] else 'No'}\n", 'value')
            details_text.insert(tk.END, f"Fair Trade: {'Yes' if product['fair_trade'] else 'No'}\n", 'value')
            details_text.insert(tk.END,
                f"Single Origin: {'Yes' if product['single_origin'] else 'No'}\n\n", 'value')

            if product['special_features']:
                details_text.insert(tk.END, "Special Features\n", 'header')
                details_text.insert(tk.END, f"{product['special_features']}\n", 'value')

            details_text.config(state='disabled')
            ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)
