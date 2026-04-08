"""
Coffee Explorer - Guide and History tabs.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import os


class GuideTabMixin:
    """Mixin providing the Coffee Guide and Coffee History tabs."""

    def create_guide_tab(self):
        guide_frame = ttk.Frame(self.notebook)
        self.notebook.add(guide_frame, text="Coffee Guide")

        header_frame = ttk.Frame(guide_frame)
        header_frame.pack(fill='x', padx=10, pady=10)
        ttk.Label(header_frame, text="Complete Coffee Guide",
                  style='Title.TLabel').pack(side='left')
        ttk.Button(header_frame, text="Reload",
                   command=self.load_guide).pack(side='right', padx=5)

        self.guide_text = scrolledtext.ScrolledText(guide_frame, wrap=tk.WORD,
                                                    font=('Arial', 10))
        self.guide_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        self.guide_text.tag_configure('title', font=('Arial', 16, 'bold'), foreground='#6F4E37')
        self.guide_text.tag_configure('heading', font=('Arial', 14, 'bold'), foreground='#4a4a4a')
        self.guide_text.tag_configure('subheading', font=('Arial', 12, 'bold'))

        self.load_guide()

    def create_history_tab(self):
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text="Coffee History")

        header_frame = ttk.Frame(history_frame)
        header_frame.pack(fill='x', padx=10, pady=10)
        ttk.Label(header_frame, text="The Complete History of Coffee",
                  style='Title.TLabel').pack(side='left')
        ttk.Button(header_frame, text="Reload",
                   command=self.load_history).pack(side='right', padx=5)

        self.history_text = scrolledtext.ScrolledText(history_frame, wrap=tk.WORD,
                                                      font=('Arial', 10))
        self.history_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        self.history_text.tag_configure('title', font=('Arial', 16, 'bold'), foreground='#6F4E37')
        self.history_text.tag_configure('heading', font=('Arial', 14, 'bold'), foreground='#4a4a4a')
        self.history_text.tag_configure('subheading', font=('Arial', 12, 'bold'))

        self.load_history()

    # ── Markdown loading ─────────────────────────────────────────────

    def _render_markdown(self, text_widget, content):
        """Simple markdown renderer into a ScrolledText widget."""
        for line in content.split('\n'):
            if line.startswith('# '):
                text_widget.insert(tk.END, line[2:] + '\n', 'title')
            elif line.startswith('## '):
                text_widget.insert(tk.END, '\n' + line[3:] + '\n', 'heading')
            elif line.startswith('### '):
                text_widget.insert(tk.END, '\n' + line[4:] + '\n', 'subheading')
            else:
                text_widget.insert(tk.END, line + '\n')

    def load_guide(self):
        self.guide_text.delete('1.0', tk.END)
        if os.path.exists(self.guide_path):
            try:
                with open(self.guide_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self._render_markdown(self.guide_text, content)
                self.guide_text.see('1.0')
            except Exception as e:
                self.guide_text.insert(tk.END, f"Error loading guide: {e}")
        else:
            self.guide_text.insert(tk.END, "Coffee guide file not found.\n\n")
            self.guide_text.insert(tk.END,
                "Please ensure coffee_guide.md is in the same directory as the application.")

    def load_history(self):
        self.history_text.delete('1.0', tk.END)
        if os.path.exists(self.history_path):
            try:
                with open(self.history_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self._render_markdown(self.history_text, content)
                self.history_text.see('1.0')
            except Exception as e:
                self.history_text.insert(tk.END, f"Error loading history: {e}")
        else:
            self.history_text.insert(tk.END, "Coffee history file not found.\n\n")
            self.history_text.insert(tk.END,
                "Please ensure coffee_history.md is in the same directory as the application.")

    def show_about(self):
        messagebox.showinfo("About Coffee Collection Explorer",
            "Coffee Collection Explorer v1.1\n\n"
            "A comprehensive coffee database browser\n\n"
            "Features:\n"
            "- 29 coffee origins worldwide\n"
            "- 20 coffee varieties/cultivars\n"
            "- 28 coffee roasters & brands\n"
            "- 61 coffee products\n"
            "- 12 brewing methods with timer\n"
            "- Tasting journal\n"
            "- Complete coffee guide\n"
            "- Comprehensive coffee history\n"
            "- Interactive world map\n\n"
            "Explore the wonderful world of coffee!"
        )
