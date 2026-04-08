"""
Coffee Explorer - Brewing methods & timer tab.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import sqlite3
import threading
import time


class BrewingTabMixin:
    """Mixin providing the Brewing Methods tab and timer."""

    def create_brewing_tab(self):
        brewing_frame = ttk.Frame(self.notebook)
        self.notebook.add(brewing_frame, text="Brewing Methods")

        paned = ttk.PanedWindow(brewing_frame, orient=tk.HORIZONTAL)
        paned.pack(fill='both', expand=True, padx=10, pady=10)

        # Left: methods list
        methods_frame = ttk.Frame(paned)
        paned.add(methods_frame, weight=1)
        ttk.Label(methods_frame, text="Brewing Methods", style='Header.TLabel').pack(pady=5)

        methods_scroll = ttk.Frame(methods_frame)
        methods_scroll.pack(fill='both', expand=True)
        self.methods_listbox = tk.Listbox(methods_scroll, font=('Arial', 10))
        methods_scrollbar = ttk.Scrollbar(methods_scroll, orient='vertical',
                                          command=self.methods_listbox.yview)
        self.methods_listbox.configure(yscrollcommand=methods_scrollbar.set)
        self.methods_listbox.pack(side='left', fill='both', expand=True)
        methods_scrollbar.pack(side='right', fill='y')
        self.methods_listbox.bind('<<ListboxSelect>>', self.on_method_select)

        # Right: details + timer
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)
        ttk.Label(right_frame, text="Method Details", style='Header.TLabel').pack(pady=5)

        self.method_details_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD,
                                                             font=('Arial', 10), height=15)
        self.method_details_text.pack(fill='both', expand=True, pady=(0, 10))
        self.method_details_text.tag_configure('title', font=('Arial', 14, 'bold'), foreground='#6F4E37')
        self.method_details_text.tag_configure('header', font=('Arial', 11, 'bold'))
        self.method_details_text.tag_configure('value', font=('Arial', 10))

        # Timer
        timer_frame = ttk.LabelFrame(right_frame, text="Brewing Timer", padding=10)
        timer_frame.pack(fill='both', expand=True)

        self.timer_label = ttk.Label(timer_frame, text="00:00", style='Timer.TLabel')
        self.timer_label.pack(pady=20)

        time_control_frame = ttk.Frame(timer_frame)
        time_control_frame.pack(pady=10)
        ttk.Label(time_control_frame, text="Minutes:").pack(side='left', padx=5)
        self.timer_minutes = tk.StringVar(value="4")
        ttk.Spinbox(time_control_frame, from_=0, to=30,
                     textvariable=self.timer_minutes, width=5).pack(side='left', padx=5)
        ttk.Label(time_control_frame, text="Seconds:").pack(side='left', padx=5)
        self.timer_seconds_var = tk.StringVar(value="00")
        ttk.Spinbox(time_control_frame, from_=0, to=59,
                     textvariable=self.timer_seconds_var, width=5).pack(side='left', padx=5)

        button_frame = ttk.Frame(timer_frame)
        button_frame.pack(pady=10)
        self.start_button = ttk.Button(button_frame, text="Start",
                                       command=self.start_timer, style='Action.TButton')
        self.start_button.pack(side='left', padx=5)
        self.pause_button = ttk.Button(button_frame, text="Pause",
                                       command=self.pause_timer, state='disabled')
        self.pause_button.pack(side='left', padx=5)
        ttk.Button(button_frame, text="Reset", command=self.reset_timer).pack(side='left', padx=5)

        self.load_brewing_methods()

    # ── Handlers ─────────────────────────────────────────────────────

    def load_brewing_methods(self):
        self.methods_listbox.delete(0, tk.END)
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT name FROM brewing_methods ORDER BY name")
            rows = cursor.fetchall()
            for row in rows:
                self.methods_listbox.insert(tk.END, row['name'])
            if rows:
                self.methods_listbox.select_set(0)
                self.on_method_select(None)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading brewing methods: {e}")

    def on_method_select(self, event):
        selection = self.methods_listbox.curselection()
        if not selection:
            return
        try:
            method_name = self.methods_listbox.get(selection[0])
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM brewing_methods WHERE name = ?", (method_name,))
            method = cursor.fetchone()
            if method:
                self.display_method_details(method)
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error: {e}")

    def display_method_details(self, method):
        self.method_details_text.delete('1.0', tk.END)
        self.method_details_text.insert(tk.END, f"{method['name']}\n", 'title')
        self.method_details_text.insert(tk.END, f"{method['category']} Brewing\n\n", 'header')

        self.method_details_text.insert(tk.END, "Parameters\n", 'header')
        self.method_details_text.insert(tk.END, f"Grind Size: {method['grind_size']}\n", 'value')
        self.method_details_text.insert(tk.END,
            f"Water Temp: {method['water_temp_c']}C ({method['water_temp_f']}F)\n", 'value')
        self.method_details_text.insert(tk.END, f"Brew Time: {method['brew_time']}\n", 'value')
        self.method_details_text.insert(tk.END,
            f"Coffee:Water Ratio: {method['coffee_water_ratio']}\n\n", 'value')

        self.method_details_text.insert(tk.END, "Equipment\n", 'header')
        self.method_details_text.insert(tk.END, f"{method['equipment_needed']}\n\n", 'value')

        self.method_details_text.insert(tk.END, "Difficulty\n", 'header')
        self.method_details_text.insert(tk.END, f"{method['difficulty_level']}\n\n", 'value')

        self.method_details_text.insert(tk.END, "Flavor Characteristics\n", 'header')
        self.method_details_text.insert(tk.END, f"{method['flavor_characteristics']}\n\n", 'value')

        self.method_details_text.insert(tk.END, "Description\n", 'header')
        self.method_details_text.insert(tk.END, f"{method['description']}\n", 'value')

    # ── Timer ────────────────────────────────────────────────────────

    def start_timer(self):
        if not self.timer_running:
            try:
                minutes = int(self.timer_minutes.get() or 0)
                seconds = int(self.timer_seconds_var.get() or 0)
                self.timer_seconds = minutes * 60 + seconds
                if self.timer_seconds > 0:
                    self.timer_running = True
                    self.start_button.config(state='disabled')
                    self.pause_button.config(state='normal')
                    self.timer_thread = threading.Thread(target=self.run_timer, daemon=True)
                    self.timer_thread.start()
            except ValueError:
                messagebox.showerror("Error", "Invalid time format")

    def pause_timer(self):
        self.timer_running = False
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled')

    def reset_timer(self):
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_label.config(text="00:00")
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled')

    def run_timer(self):
        while self.timer_running and self.timer_seconds > 0:
            minutes = self.timer_seconds // 60
            seconds = self.timer_seconds % 60
            self.root.after(0, lambda m=minutes, s=seconds:
                            self.timer_label.config(text=f"{m:02d}:{s:02d}"))
            time.sleep(1)
            self.timer_seconds -= 1

        if self.timer_seconds == 0 and self.timer_running:
            self.root.after(0, lambda: self.timer_label.config(text="00:00"))
            self.root.after(0, lambda: messagebox.showinfo("Timer", "Coffee is ready!"))
            self.root.after(0, self.reset_timer)
            try:
                self.root.bell()
            except (tk.TclError, RuntimeError):
                pass
