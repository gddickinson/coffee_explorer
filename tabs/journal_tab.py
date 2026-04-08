"""
Coffee Explorer - Tasting journal tab.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import sqlite3
import json
import os
from datetime import datetime


class JournalTabMixin:
    """Mixin providing the Tasting Journal tab and its handlers."""

    def create_journal_tab(self):
        journal_frame = ttk.Frame(self.notebook)
        self.notebook.add(journal_frame, text="Tasting Journal")

        header_frame = ttk.Frame(journal_frame)
        header_frame.pack(fill='x', padx=10, pady=10)
        ttk.Label(header_frame, text="Coffee Tasting Journal",
                  style='Title.TLabel').pack(side='left')
        ttk.Button(header_frame, text="New Entry", command=self.new_journal_entry,
                   style='Action.TButton').pack(side='right', padx=5)

        content_frame = ttk.Frame(journal_frame)
        content_frame.pack(fill='both', expand=True, padx=10, pady=5)

        list_frame = ttk.Frame(content_frame)
        list_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        ttk.Label(list_frame, text="Journal Entries", style='Header.TLabel').pack(anchor='w', pady=5)

        list_scroll = ttk.Frame(list_frame)
        list_scroll.pack(fill='both', expand=True)
        self.journal_listbox = tk.Listbox(list_scroll, font=('Arial', 10))
        journal_scrollbar = ttk.Scrollbar(list_scroll, orient='vertical',
                                          command=self.journal_listbox.yview)
        self.journal_listbox.configure(yscrollcommand=journal_scrollbar.set)
        self.journal_listbox.pack(side='left', fill='both', expand=True)
        journal_scrollbar.pack(side='right', fill='y')
        self.journal_listbox.bind('<<ListboxSelect>>', self.on_journal_select)

        details_frame = ttk.Frame(content_frame)
        details_frame.pack(side='right', fill='both', expand=True)
        ttk.Label(details_frame, text="Entry Details", style='Header.TLabel').pack(anchor='w', pady=5)

        self.journal_details_text = scrolledtext.ScrolledText(details_frame, wrap=tk.WORD,
                                                              font=('Arial', 10))
        self.journal_details_text.pack(fill='both', expand=True)
        self.journal_details_text.tag_configure('title', font=('Arial', 14, 'bold'), foreground='#6F4E37')
        self.journal_details_text.tag_configure('header', font=('Arial', 11, 'bold'))
        self.journal_details_text.tag_configure('value', font=('Arial', 10))

        self.load_journal_list()

    # ── Journal persistence ──────────────────────────────────────────

    def load_journal(self):
        """Load journal from file, handling corrupt JSON gracefully."""
        self.journal_entries = []
        if os.path.exists(self.journal_path):
            try:
                with open(self.journal_path, 'r', encoding='utf-8') as f:
                    self.journal_entries = json.load(f)
            except (json.JSONDecodeError, IOError, ValueError):
                self.journal_entries = []

    def save_journal(self):
        try:
            with open(self.journal_path, 'w', encoding='utf-8') as f:
                json.dump(self.journal_entries, f, indent=2, ensure_ascii=False)
            self.update_status()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save journal: {e}")

    def load_journal_list(self):
        self.journal_listbox.delete(0, tk.END)
        for entry in sorted(self.journal_entries, key=lambda x: x.get('date', ''), reverse=True):
            coffee_name = entry.get('coffee_name', 'Unknown')
            date = entry.get('date', '')
            rating = entry.get('rating', 0)
            stars = '*' * rating
            display = f"{date} - {coffee_name} {stars}"
            self.journal_listbox.insert(tk.END, display)

    # ── New entry dialog ─────────────────────────────────────────────

    def new_journal_entry(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("New Tasting Entry")
        dialog.geometry("500x600")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="Coffee Name:").pack(anchor='w', padx=10, pady=(10, 0))
        coffee_var = tk.StringVar()
        if self.current_coffee:
            coffee_var.set(self.current_coffee)
        coffee_combo = ttk.Combobox(dialog, textvariable=coffee_var, width=50)
        coffee_combo.pack(padx=10, pady=5, fill='x')

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM coffees ORDER BY name")
            coffee_combo['values'] = [row['name'] for row in cursor.fetchall()]
        except (sqlite3.Error, AttributeError):
            pass

        ttk.Label(dialog, text="Rating:").pack(anchor='w', padx=10, pady=(10, 0))
        rating_var = tk.IntVar(value=3)
        rating_frame = ttk.Frame(dialog)
        rating_frame.pack(padx=10, pady=5)
        for i in range(1, 6):
            ttk.Radiobutton(rating_frame, text=f"{'*' * i}", variable=rating_var,
                            value=i).pack(side='left', padx=5)

        ttk.Label(dialog, text="Brewing Details:").pack(anchor='w', padx=10, pady=(10, 0))
        brewing_text = tk.Text(dialog, height=3, width=50)
        brewing_text.pack(padx=10, pady=5)
        brewing_text.insert('1.0', "Method: \nGrind: \nRatio: ")

        ttk.Label(dialog, text="Tasting Notes:").pack(anchor='w', padx=10, pady=(10, 0))
        notes_text = scrolledtext.ScrolledText(dialog, height=10, width=50)
        notes_text.pack(padx=10, pady=5, fill='both', expand=True)

        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)

        def save_entry():
            coffee_name = coffee_var.get()
            if not coffee_name:
                messagebox.showerror("Error", "Please select a coffee")
                return
            entry = {
                'coffee_name': coffee_name,
                'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'rating': rating_var.get(),
                'brewing': brewing_text.get('1.0', tk.END).strip(),
                'notes': notes_text.get('1.0', tk.END).strip(),
            }
            self.journal_entries.append(entry)
            self.save_journal()
            self.load_journal_list()
            dialog.destroy()

        ttk.Button(button_frame, text="Save", command=save_entry,
                   style='Action.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side='left', padx=5)

    # ── Selection / export ───────────────────────────────────────────

    def on_journal_select(self, event):
        selection = self.journal_listbox.curselection()
        if not selection:
            return
        sorted_entries = sorted(self.journal_entries,
                                key=lambda x: x.get('date', ''), reverse=True)
        if selection[0] < len(sorted_entries):
            entry = sorted_entries[selection[0]]
            self.journal_details_text.delete('1.0', tk.END)
            self.journal_details_text.insert(tk.END, f"{entry['coffee_name']}\n", 'title')
            self.journal_details_text.insert(tk.END, f"{entry['date']}\n", 'header')
            self.journal_details_text.insert(tk.END, f"{'*' * entry['rating']}\n\n", 'value')
            self.journal_details_text.insert(tk.END, "Brewing Details\n", 'header')
            self.journal_details_text.insert(tk.END, f"{entry['brewing']}\n\n", 'value')
            self.journal_details_text.insert(tk.END, "Tasting Notes\n", 'header')
            self.journal_details_text.insert(tk.END, f"{entry['notes']}\n", 'value')

    def export_journal(self):
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.journal_entries, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Success", "Journal exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export: {e}")
