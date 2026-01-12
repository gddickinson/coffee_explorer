"""
Coffee Collection Explorer - Comprehensive GUI Application
A complete coffee database browser with advanced features

Features:
- Coffee Database Browser
- Coffee Varieties/Cultivars
- Coffee Roasters/Brands
- Brewing Methods & Timer
- Tasting Journal
- Coffee Regions Map
- Glossary
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import sqlite3
from pathlib import Path
from PIL import Image, ImageTk, ImageDraw
import os
import json
from datetime import datetime
import threading
import time

class CoffeeExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coffee Collection Explorer")
        self.root.geometry("1400x900")
        
        # Database connection
        self.db_path = "coffee_collection.db"
        self.conn = None
        self.connect_db()
        
        # File paths
        script_dir = os.path.dirname(os.path.abspath(__file__))
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
        
        # Create tabs
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
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.conn.row_factory = sqlite3.Row
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Could not connect to database: {e}")
    
    def create_menu_bar(self):
        """Create application menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Export Journal (JSON)", command=self.export_journal)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Coffee Database", command=lambda: self.notebook.select(0))
        view_menu.add_command(label="Coffee Varieties", command=lambda: self.notebook.select(1))
        view_menu.add_command(label="Coffee Roasters", command=lambda: self.notebook.select(2))
        view_menu.add_command(label="Brewing Methods", command=lambda: self.notebook.select(3))
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
    
    def create_status_bar(self):
        """Create status bar at bottom"""
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        self.update_status()
    
    def update_status(self):
        """Update status bar with database stats"""
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
            
            status_text = f"Database: {coffee_count} coffees | {variety_count} varieties | {region_count} regions | {roaster_count} roasters | {product_count} products | Journal: {journal_count} entries"
            self.status_bar.config(text=status_text)
        except:
            self.status_bar.config(text="Ready")
    
    def configure_styles(self):
        """Configure ttk styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('TNotebook', background='#f0f0f0')
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Timer.TLabel', font=('Arial', 48, 'bold'), foreground='#6F4E37')
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))
    
    # ==============================================
    # TAB CREATION METHODS
    # ==============================================
    
    def create_database_tab(self):
        """Create the coffee database browser tab"""
        db_frame = ttk.Frame(self.notebook)
        self.notebook.add(db_frame, text="☕ Coffee Database")
        
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
        list_scrollbar = ttk.Scrollbar(list_scroll_frame, orient='vertical', command=self.coffee_listbox.yview)
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
        
        # Configure text tags
        self.details_text.tag_configure('title', font=('Arial', 16, 'bold'), foreground='#6F4E37')
        self.details_text.tag_configure('header', font=('Arial', 11, 'bold'), foreground='#4a4a4a')
        self.details_text.tag_configure('value', font=('Arial', 10))
        
        # Load initial data
        self.load_coffee_list()
    
    def create_varieties_tab(self):
        """Create the coffee varieties browser tab"""
        varieties_frame = ttk.Frame(self.notebook)
        self.notebook.add(varieties_frame, text="🌱 Coffee Varieties")
        
        # Header
        header_frame = ttk.Frame(varieties_frame)
        header_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(header_frame, text="Coffee Varieties & Cultivars",
                 style='Title.TLabel').pack(side='left')
        
        # Main content
        content_frame = ttk.Frame(varieties_frame)
        content_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left: Variety list
        list_frame = ttk.Frame(content_frame)
        list_frame.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        ttk.Label(list_frame, text="Variety List", style='Header.TLabel').pack(anchor='w', pady=5)
        
        list_scroll = ttk.Frame(list_frame)
        list_scroll.pack(fill='both', expand=True)
        
        self.variety_listbox = tk.Listbox(list_scroll, font=('Arial', 10))
        variety_scrollbar = ttk.Scrollbar(list_scroll, orient='vertical', command=self.variety_listbox.yview)
        self.variety_listbox.configure(yscrollcommand=variety_scrollbar.set)
        
        self.variety_listbox.pack(side='left', fill='both', expand=True)
        variety_scrollbar.pack(side='right', fill='y')
        
        self.variety_listbox.bind('<<ListboxSelect>>', self.on_variety_select)
        self.variety_names = []
        
        # Right: Variety details
        details_frame = ttk.Frame(content_frame)
        details_frame.pack(side='right', fill='both', expand=True)
        
        ttk.Label(details_frame, text="Variety Details", style='Header.TLabel').pack(anchor='w', pady=5)
        
        self.variety_details_text = scrolledtext.ScrolledText(details_frame, wrap=tk.WORD,
                                                              font=('Arial', 10), height=30)
        self.variety_details_text.pack(fill='both', expand=True)
        
        self.variety_details_text.tag_configure('title', font=('Arial', 16, 'bold'), foreground='#6F4E37')
        self.variety_details_text.tag_configure('header', font=('Arial', 11, 'bold'), foreground='#4a4a4a')
        self.variety_details_text.tag_configure('value', font=('Arial', 10))
        
        # Load varieties
        self.load_varieties()
    
    def create_roasters_tab(self):
        """Create coffee roasters/brands browser tab"""
        brands_frame = ttk.Frame(self.notebook)
        self.notebook.add(brands_frame, text="🏪 Coffee Roasters")
        
        # Header with search
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
        
        # Main content frame
        content_frame = ttk.Frame(brands_frame)
        content_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left: Roasters list
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
        
        # Right: Roaster details and products
        right_panel = ttk.Frame(content_frame)
        right_panel.pack(side='right', fill='both', expand=True)
        
        # Roaster details section
        details_label_frame = ttk.LabelFrame(right_panel, text="Roaster Information", padding=10)
        details_label_frame.pack(fill='both', expand=True, pady=(0, 5))
        
        self.roaster_details_text = scrolledtext.ScrolledText(details_label_frame, wrap=tk.WORD,
                                                              font=('Arial', 10), height=12)
        self.roaster_details_text.pack(fill='both', expand=True)
        
        self.roaster_details_text.tag_configure('company', font=('Arial', 16, 'bold'), foreground='#6F4E37')
        self.roaster_details_text.tag_configure('header', font=('Arial', 11, 'bold'), foreground='#4a4a4a')
        self.roaster_details_text.tag_configure('value', font=('Arial', 10))
        
        # Products section
        products_label_frame = ttk.LabelFrame(right_panel, text="Products", padding=10)
        products_label_frame.pack(fill='both', expand=True)
        
        # Products list
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
        
        # Load roasters
        self.load_roasters()
    
    def create_brewing_tab(self):
        """Create brewing methods and timer tab"""
        brewing_frame = ttk.Frame(self.notebook)
        self.notebook.add(brewing_frame, text="⏱️ Brewing Methods")
        
        # Split into two panels
        paned = ttk.PanedWindow(brewing_frame, orient=tk.HORIZONTAL)
        paned.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left: Brewing methods list
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
        
        # Right: Method details and timer
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=2)
        
        # Method details
        ttk.Label(right_frame, text="Method Details", style='Header.TLabel').pack(pady=5)
        
        self.method_details_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD,
                                                             font=('Arial', 10), height=15)
        self.method_details_text.pack(fill='both', expand=True, pady=(0, 10))
        
        self.method_details_text.tag_configure('title', font=('Arial', 14, 'bold'), foreground='#6F4E37')
        self.method_details_text.tag_configure('header', font=('Arial', 11, 'bold'))
        self.method_details_text.tag_configure('value', font=('Arial', 10))
        
        # Timer section
        timer_frame = ttk.LabelFrame(right_frame, text="Brewing Timer", padding=10)
        timer_frame.pack(fill='both', expand=True)
        
        self.timer_label = ttk.Label(timer_frame, text="00:00", style='Timer.TLabel')
        self.timer_label.pack(pady=20)
        
        # Time controls
        time_control_frame = ttk.Frame(timer_frame)
        time_control_frame.pack(pady=10)
        
        ttk.Label(time_control_frame, text="Minutes:").pack(side='left', padx=5)
        self.timer_minutes = tk.StringVar(value="4")
        ttk.Spinbox(time_control_frame, from_=0, to=30, textvariable=self.timer_minutes,
                   width=5).pack(side='left', padx=5)
        
        ttk.Label(time_control_frame, text="Seconds:").pack(side='left', padx=5)
        self.timer_seconds_var = tk.StringVar(value="00")
        ttk.Spinbox(time_control_frame, from_=0, to=59, textvariable=self.timer_seconds_var,
                   width=5).pack(side='left', padx=5)
        
        # Timer buttons
        button_frame = ttk.Frame(timer_frame)
        button_frame.pack(pady=10)
        
        self.start_button = ttk.Button(button_frame, text="Start", command=self.start_timer,
                                      style='Action.TButton')
        self.start_button.pack(side='left', padx=5)
        
        self.pause_button = ttk.Button(button_frame, text="Pause", command=self.pause_timer,
                                      state='disabled')
        self.pause_button.pack(side='left', padx=5)
        
        ttk.Button(button_frame, text="Reset", command=self.reset_timer).pack(side='left', padx=5)
        
        # Load brewing methods
        self.load_brewing_methods()
    
    def create_journal_tab(self):
        """Create tasting journal tab"""
        journal_frame = ttk.Frame(self.notebook)
        self.notebook.add(journal_frame, text="📝 Tasting Journal")
        
        # Header
        header_frame = ttk.Frame(journal_frame)
        header_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(header_frame, text="Coffee Tasting Journal", style='Title.TLabel').pack(side='left')
        ttk.Button(header_frame, text="New Entry", command=self.new_journal_entry,
                  style='Action.TButton').pack(side='right', padx=5)
        
        # Main content
        content_frame = ttk.Frame(journal_frame)
        content_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Left: Journal entries list
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
        
        # Right: Entry details
        details_frame = ttk.Frame(content_frame)
        details_frame.pack(side='right', fill='both', expand=True)
        
        ttk.Label(details_frame, text="Entry Details", style='Header.TLabel').pack(anchor='w', pady=5)
        
        self.journal_details_text = scrolledtext.ScrolledText(details_frame, wrap=tk.WORD,
                                                              font=('Arial', 10))
        self.journal_details_text.pack(fill='both', expand=True)
        
        self.journal_details_text.tag_configure('title', font=('Arial', 14, 'bold'), foreground='#6F4E37')
        self.journal_details_text.tag_configure('header', font=('Arial', 11, 'bold'))
        self.journal_details_text.tag_configure('value', font=('Arial', 10))
        
        # Load journal entries
        self.load_journal_list()
    
    def create_guide_tab(self):
        """Create coffee guide tab"""
        guide_frame = ttk.Frame(self.notebook)
        self.notebook.add(guide_frame, text="📖 Coffee Guide")
        
        # Header with reload button
        header_frame = ttk.Frame(guide_frame)
        header_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(header_frame, text="Complete Coffee Guide",
                 style='Title.TLabel').pack(side='left')
        
        ttk.Button(header_frame, text="Reload",
                  command=self.load_guide).pack(side='right', padx=5)
        
        # Guide content
        self.guide_text = scrolledtext.ScrolledText(guide_frame, wrap=tk.WORD,
                                                    font=('Arial', 10))
        self.guide_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Configure text tags
        self.guide_text.tag_configure('title', font=('Arial', 16, 'bold'), foreground='#6F4E37')
        self.guide_text.tag_configure('heading', font=('Arial', 14, 'bold'), foreground='#4a4a4a')
        self.guide_text.tag_configure('subheading', font=('Arial', 12, 'bold'))
        
        # Load guide
        self.load_guide()
    
    def create_history_tab(self):
        """Create coffee history tab"""
        history_frame = ttk.Frame(self.notebook)
        self.notebook.add(history_frame, text="📜 Coffee History")
        
        # Header with reload button
        header_frame = ttk.Frame(history_frame)
        header_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(header_frame, text="The Complete History of Coffee",
                 style='Title.TLabel').pack(side='left')
        
        ttk.Button(header_frame, text="Reload",
                  command=self.load_history).pack(side='right', padx=5)
        
        # History content
        self.history_text = scrolledtext.ScrolledText(history_frame, wrap=tk.WORD,
                                                      font=('Arial', 10))
        self.history_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Configure text tags
        self.history_text.tag_configure('title', font=('Arial', 16, 'bold'), foreground='#6F4E37')
        self.history_text.tag_configure('heading', font=('Arial', 14, 'bold'), foreground='#4a4a4a')
        self.history_text.tag_configure('subheading', font=('Arial', 12, 'bold'))
        
        # Load history
        self.load_history()
    
    def create_map_tab(self):
        """Create world map of coffee regions"""
        map_frame = ttk.Frame(self.notebook)
        self.notebook.add(map_frame, text="🗺️ Coffee Regions")
        
        ttk.Label(map_frame, text="Coffee Growing Regions Around the World",
                 style='Title.TLabel').pack(pady=10)
        
        # Map canvas
        canvas_frame = ttk.Frame(map_frame)
        canvas_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.map_canvas = tk.Canvas(canvas_frame, bg='#d4e8f7')
        self.map_canvas.pack(fill='both', expand=True)
        
        # Store region markers
        self.map_regions = []
        
        # Create map
        self.create_world_map()
        
        # Bind events
        self.map_canvas.bind('<Button-1>', self.on_map_click)
        self.map_canvas.bind('<Motion>', self.on_map_hover)
    
    # ==============================================
    # DATABASE TAB FUNCTIONS
    # ==============================================
    
    def load_coffee_list(self, search_term='', roast='All'):
        """Load coffee list with filters"""
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
        """Handle search"""
        search_term = self.search_var.get()
        roast = self.roast_var.get()
        self.load_coffee_list(search_term, roast)
    
    def clear_search(self):
        """Clear all filters"""
        self.search_var.set('')
        self.roast_var.set('All')
        self.load_coffee_list()
    
    def on_coffee_select(self, event):
        """Handle coffee selection"""
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
        """Display coffee details"""
        self.details_text.delete('1.0', tk.END)
        
        self.details_text.insert(tk.END, f"{coffee['name']}\n", 'title')
        self.details_text.insert(tk.END, f"{coffee['origin_country']} - {coffee['origin_region']}\n\n", 'header')
        
        self.details_text.insert(tk.END, "🌱 Variety & Processing\n", 'header')
        self.details_text.insert(tk.END, f"Variety: {coffee['variety']}\n", 'value')
        self.details_text.insert(tk.END, f"Processing: {coffee['processing_method']}\n", 'value')
        self.details_text.insert(tk.END, f"Roast Level: {coffee['roast_level']}\n\n", 'value')
        
        self.details_text.insert(tk.END, "👃 Flavor Profile\n", 'header')
        self.details_text.insert(tk.END, f"{coffee['flavor_profile']}\n", 'value')
        self.details_text.insert(tk.END, f"Aroma: {coffee['aroma']}\n", 'value')
        self.details_text.insert(tk.END, f"Body: {coffee['body']}\n", 'value')
        self.details_text.insert(tk.END, f"Acidity: {coffee['acidity']}\n\n", 'value')
        
        self.details_text.insert(tk.END, "🏔️ Growing Conditions\n", 'header')
        self.details_text.insert(tk.END,
            f"Altitude: {coffee['altitude_min']}-{coffee['altitude_max']} meters\n", 'value')
        self.details_text.insert(tk.END, f"Harvest: {coffee['harvest_season']}\n", 'value')
        self.details_text.insert(tk.END, f"Caffeine: {coffee['caffeine_content']}\n\n", 'value')
        
        if coffee['cupping_score']:
            self.details_text.insert(tk.END, "⭐ Quality\n", 'header')
            self.details_text.insert(tk.END, f"Cupping Score: {coffee['cupping_score']}/100\n\n", 'value')
        
        self.details_text.insert(tk.END, "🔖 Tasting Notes\n", 'header')
        self.details_text.insert(tk.END, f"{coffee['tasting_notes']}\n\n", 'value')
        
        self.details_text.insert(tk.END, "📜 History\n", 'header')
        self.details_text.insert(tk.END, f"{coffee['history']}\n\n", 'value')
        
        self.details_text.insert(tk.END, "💰 Price Range\n", 'header')
        self.details_text.insert(tk.END, f"{coffee['price_range']}\n", 'value')
    
    # ==============================================
    # VARIETIES TAB FUNCTIONS
    # ==============================================
    
    def load_varieties(self):
        """Load coffee varieties"""
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
        """Handle variety selection"""
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
        """Display variety details"""
        self.variety_details_text.delete('1.0', tk.END)
        
        self.variety_details_text.insert(tk.END, f"{variety['name']}\n", 'title')
        self.variety_details_text.insert(tk.END, f"{variety['species']}\n\n", 'header')
        
        self.variety_details_text.insert(tk.END, "🌍 Origin\n", 'header')
        self.variety_details_text.insert(tk.END, f"Country: {variety['origin_country']}\n", 'value')
        self.variety_details_text.insert(tk.END, f"Discovered: {variety['discovered_year']}\n\n", 'value')
        
        self.variety_details_text.insert(tk.END, "🌱 Characteristics\n", 'header')
        self.variety_details_text.insert(tk.END, f"{variety['characteristics']}\n\n", 'value')
        
        self.variety_details_text.insert(tk.END, "☕ Flavor Notes\n", 'header')
        self.variety_details_text.insert(tk.END, f"{variety['flavor_notes']}\n\n", 'value')
        
        self.variety_details_text.insert(tk.END, "🛡️ Disease Resistance\n", 'header')
        self.variety_details_text.insert(tk.END, f"{variety['disease_resistance']}\n\n", 'value')
        
        self.variety_details_text.insert(tk.END, "📊 Yield\n", 'header')
        self.variety_details_text.insert(tk.END, f"{variety['yield']}\n\n", 'value')
        
        if variety['notes']:
            self.variety_details_text.insert(tk.END, "📝 Additional Notes\n", 'header')
            self.variety_details_text.insert(tk.END, f"{variety['notes']}\n", 'value')
    
    # ==============================================
    # ROASTERS TAB FUNCTIONS
    # ==============================================
    
    def load_roasters(self, search_term='', country='All', segment='All'):
        """Load roasters list with filters"""
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
                self.roaster_data.append({
                    'id': row['roaster_id'],
                    'name': row['roaster_name']
                })
            
            if rows:
                self.roasters_listbox.select_set(0)
                self.on_roaster_select(None)
        
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading roasters: {e}")
    
    def on_roaster_search(self, event=None):
        """Handle roaster search"""
        search_term = self.roaster_search_var.get()
        country = self.roaster_country_var.get()
        segment = self.roaster_segment_var.get()
        self.load_roasters(search_term, country, segment)
    
    def clear_roaster_filters(self):
        """Clear all roaster filters"""
        self.roaster_search_var.set('')
        self.roaster_country_var.set('All')
        self.roaster_segment_var.set('All')
        self.load_roasters()
    
    def on_roaster_select(self, event):
        """Handle roaster selection"""
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
        """Display roaster details"""
        self.roaster_details_text.delete('1.0', tk.END)
        
        self.roaster_details_text.insert(tk.END, f"{roaster['roaster_name']}\n", 'company')
        self.roaster_details_text.insert(tk.END, f"{roaster['market_segment'].title()} Roaster\n\n", 'header')
        
        self.roaster_details_text.insert(tk.END, "🏢 Company Information\n", 'header')
        if roaster['parent_company']:
            self.roaster_details_text.insert(tk.END, f"Parent: {roaster['parent_company']}\n", 'value')
        self.roaster_details_text.insert(tk.END, f"Founded: {roaster['founded_year']}\n", 'value')
        self.roaster_details_text.insert(tk.END,
            f"Headquarters: {roaster['headquarters_city']}, {roaster['country_of_origin']}\n", 'value')
        if roaster['website']:
            self.roaster_details_text.insert(tk.END, f"Website: {roaster['website']}\n", 'value')
        self.roaster_details_text.insert(tk.END, "\n")
        
        if roaster['roasting_style']:
            self.roaster_details_text.insert(tk.END, "☕ Roasting Style\n", 'header')
            self.roaster_details_text.insert(tk.END, f"{roaster['roasting_style']}\n\n", 'value')
        
        if roaster['certifications']:
            self.roaster_details_text.insert(tk.END, "✓ Certifications\n", 'header')
            self.roaster_details_text.insert(tk.END, f"{roaster['certifications']}\n\n", 'value')
        
        if roaster['description']:
            self.roaster_details_text.insert(tk.END, "📝 Description\n", 'header')
            self.roaster_details_text.insert(tk.END, f"{roaster['description']}\n", 'value')
    
    def load_roaster_products(self, roaster_id):
        """Load products for selected roaster"""
        self.products_listbox.delete(0, tk.END)
        self.current_products = []
        
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM products WHERE roaster_id = ? ORDER BY product_name",
                          (roaster_id,))
            products = cursor.fetchall()
            
            for product in products:
                price_str = f"{product['price_currency']} {product['price']:.2f}" if product['price'] else "N/A"
                display = f"{product['product_name']} - {product['roast_level']} - {price_str}"
                
                self.products_listbox.insert(tk.END, display)
                self.current_products.append(dict(product))
        
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Error loading products: {e}")
    
    def on_product_select(self, event):
        """Handle product selection"""
        selection = self.products_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        if index < len(self.current_products):
            product = self.current_products[index]
            
            # Show product details in popup
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
                details_text.insert(tk.END, f"Weight: {product['weight_oz']} oz ({product['weight_g']}g)\n\n", 'value')
            
            details_text.insert(tk.END, "Pricing & Availability\n", 'header')
            if product['price']:
                details_text.insert(tk.END, f"Price: {product['price_currency']} {product['price']:.2f}\n", 'value')
            details_text.insert(tk.END, f"Available in: {product['countries_available']}\n\n", 'value')
            
            details_text.insert(tk.END, "Certifications\n", 'header')
            details_text.insert(tk.END, f"Organic: {'Yes' if product['organic'] else 'No'}\n", 'value')
            details_text.insert(tk.END, f"Fair Trade: {'Yes' if product['fair_trade'] else 'No'}\n", 'value')
            details_text.insert(tk.END, f"Single Origin: {'Yes' if product['single_origin'] else 'No'}\n\n", 'value')
            
            if product['special_features']:
                details_text.insert(tk.END, "Special Features\n", 'header')
                details_text.insert(tk.END, f"{product['special_features']}\n", 'value')
            
            details_text.config(state='disabled')
            
            ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)
    
    # ==============================================
    # BREWING TAB FUNCTIONS
    # ==============================================
    
    def load_brewing_methods(self):
        """Load brewing methods"""
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
        """Handle brewing method selection"""
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
        """Display brewing method details"""
        self.method_details_text.delete('1.0', tk.END)
        
        self.method_details_text.insert(tk.END, f"{method['name']}\n", 'title')
        self.method_details_text.insert(tk.END, f"{method['category']} Brewing\n\n", 'header')
        
        self.method_details_text.insert(tk.END, "⚙️ Parameters\n", 'header')
        self.method_details_text.insert(tk.END, f"Grind Size: {method['grind_size']}\n", 'value')
        self.method_details_text.insert(tk.END,
            f"Water Temp: {method['water_temp_c']}°C ({method['water_temp_f']}°F)\n", 'value')
        self.method_details_text.insert(tk.END, f"Brew Time: {method['brew_time']}\n", 'value')
        self.method_details_text.insert(tk.END, f"Coffee:Water Ratio: {method['coffee_water_ratio']}\n\n", 'value')
        
        self.method_details_text.insert(tk.END, "🛠️ Equipment\n", 'header')
        self.method_details_text.insert(tk.END, f"{method['equipment_needed']}\n\n", 'value')
        
        self.method_details_text.insert(tk.END, "📊 Difficulty\n", 'header')
        self.method_details_text.insert(tk.END, f"{method['difficulty_level']}\n\n", 'value')
        
        self.method_details_text.insert(tk.END, "☕ Flavor Characteristics\n", 'header')
        self.method_details_text.insert(tk.END, f"{method['flavor_characteristics']}\n\n", 'value')
        
        self.method_details_text.insert(tk.END, "📝 Description\n", 'header')
        self.method_details_text.insert(tk.END, f"{method['description']}\n", 'value')
    
    def start_timer(self):
        """Start brewing timer"""
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
        """Pause brewing timer"""
        self.timer_running = False
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled')
    
    def reset_timer(self):
        """Reset brewing timer"""
        self.timer_running = False
        self.timer_seconds = 0
        self.timer_label.config(text="00:00")
        self.start_button.config(state='normal')
        self.pause_button.config(state='disabled')
    
    def run_timer(self):
        """Timer thread"""
        while self.timer_running and self.timer_seconds > 0:
            minutes = self.timer_seconds // 60
            seconds = self.timer_seconds % 60
            self.root.after(0, lambda m=minutes, s=seconds:
                          self.timer_label.config(text=f"{m:02d}:{s:02d}"))
            time.sleep(1)
            self.timer_seconds -= 1
        
        if self.timer_seconds == 0 and self.timer_running:
            self.root.after(0, lambda: self.timer_label.config(text="00:00"))
            self.root.after(0, lambda: messagebox.showinfo("Timer", "☕ Coffee is ready!"))
            self.root.after(0, self.reset_timer)
            try:
                self.root.bell()
            except:
                pass
    
    # ==============================================
    # JOURNAL FUNCTIONS
    # ==============================================
    
    def load_journal(self):
        """Load journal from file"""
        self.journal_entries = []
        if os.path.exists(self.journal_path):
            try:
                with open(self.journal_path, 'r', encoding='utf-8') as f:
                    self.journal_entries = json.load(f)
            except:
                self.journal_entries = []
    
    def save_journal(self):
        """Save journal to file"""
        try:
            with open(self.journal_path, 'w', encoding='utf-8') as f:
                json.dump(self.journal_entries, f, indent=2, ensure_ascii=False)
            self.update_status()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save journal: {e}")
    
    def load_journal_list(self):
        """Load journal entries"""
        self.journal_listbox.delete(0, tk.END)
        
        for entry in sorted(self.journal_entries, key=lambda x: x.get('date', ''), reverse=True):
            coffee_name = entry.get('coffee_name', 'Unknown')
            date = entry.get('date', '')
            rating = entry.get('rating', 0)
            stars = '⭐' * rating
            display = f"{date} - {coffee_name} {stars}"
            self.journal_listbox.insert(tk.END, display)
    
    def new_journal_entry(self):
        """Create new journal entry"""
        dialog = tk.Toplevel(self.root)
        dialog.title("New Tasting Entry")
        dialog.geometry("500x600")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Coffee selection
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
        except:
            pass
        
        # Rating
        ttk.Label(dialog, text="Rating:").pack(anchor='w', padx=10, pady=(10, 0))
        rating_var = tk.IntVar(value=3)
        rating_frame = ttk.Frame(dialog)
        rating_frame.pack(padx=10, pady=5)
        for i in range(1, 6):
            ttk.Radiobutton(rating_frame, text=f"{'⭐' * i}", variable=rating_var,
                           value=i).pack(side='left', padx=5)
        
        # Brewing details
        ttk.Label(dialog, text="Brewing Details:").pack(anchor='w', padx=10, pady=(10, 0))
        brewing_text = tk.Text(dialog, height=3, width=50)
        brewing_text.pack(padx=10, pady=5)
        brewing_text.insert('1.0', "Method: \nGrind: \nRatio: ")
        
        # Notes
        ttk.Label(dialog, text="Tasting Notes:").pack(anchor='w', padx=10, pady=(10, 0))
        notes_text = scrolledtext.ScrolledText(dialog, height=10, width=50)
        notes_text.pack(padx=10, pady=5, fill='both', expand=True)
        
        # Buttons
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
                'notes': notes_text.get('1.0', tk.END).strip()
            }
            
            self.journal_entries.append(entry)
            self.save_journal()
            self.load_journal_list()
            dialog.destroy()
        
        ttk.Button(button_frame, text="Save", command=save_entry,
                  style='Action.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side='left', padx=5)
    
    def on_journal_select(self, event):
        """Handle journal selection"""
        selection = self.journal_listbox.curselection()
        if not selection:
            return
        
        index = len(self.journal_entries) - 1 - selection[0]
        if 0 <= index < len(self.journal_entries):
            entry = sorted(self.journal_entries, key=lambda x: x.get('date', ''), reverse=True)[selection[0]]
            
            self.journal_details_text.delete('1.0', tk.END)
            
            self.journal_details_text.insert(tk.END, f"{entry['coffee_name']}\n", 'title')
            self.journal_details_text.insert(tk.END, f"{entry['date']}\n", 'header')
            self.journal_details_text.insert(tk.END, f"{'⭐' * entry['rating']}\n\n", 'value')
            
            self.journal_details_text.insert(tk.END, "Brewing Details\n", 'header')
            self.journal_details_text.insert(tk.END, f"{entry['brewing']}\n\n", 'value')
            
            self.journal_details_text.insert(tk.END, "Tasting Notes\n", 'header')
            self.journal_details_text.insert(tk.END, f"{entry['notes']}\n", 'value')
    
    def export_journal(self):
        """Export journal to JSON file"""
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
    
    # ==============================================
    # MAP FUNCTIONS
    # ==============================================
    
    def get_world_map_image(self, width, height):
        """Get or create world map image"""
        import os
        from pathlib import Path
        
        # Check if cached map exists
        cache_dir = Path.home() / '.coffee_explorer'
        cache_dir.mkdir(exist_ok=True)
        map_file = cache_dir / 'world_map.png'
        
        if map_file.exists():
            try:
                img = Image.open(map_file)
                if img.size == (width, height):
                    return img
            except:
                pass
        
        # Try to download or create map
        print("Attempting to create world map...")
        
        # Try GeoPandas first
        return self.create_geopandas_world_map(width, height, map_file)
    
    def create_geopandas_world_map(self, width, height, save_path):
        """Create a world map using GeoPandas with manually defined geometries"""
        try:
            import matplotlib
            matplotlib.use('Agg')  # Use non-interactive backend
            import matplotlib.pyplot as plt
            import geopandas as gpd
            from shapely.geometry import Polygon
            
            print("Creating world map with GeoPandas...")
            
            # Define continent polygons (longitude, latitude)
            continents_data = {
                'Asia': [
                    (26, 40), (35, 45), (45, 42), (55, 48), (75, 50), (90, 55),
                    (105, 50), (115, 48), (125, 53), (135, 48), (145, 50), (150, 45),
                    (145, 40), (142, 35), (138, 30), (130, 20), (125, 10), (120, 5),
                    (105, 0), (100, -5), (95, -10), (92, -8), (85, -5), (78, 0),
                    (68, 8), (60, 15), (55, 25), (48, 28), (42, 32), (35, 36), (26, 40)
                ],
                'Europe': [
                    (-10, 36), (-5, 43), (0, 48), (10, 50), (15, 54), (25, 58),
                    (30, 65), (28, 70), (20, 68), (10, 64), (5, 60), (0, 56),
                    (-5, 51), (-8, 46), (-10, 40), (-10, 36)
                ],
                'Africa': [
                    (-18, 28), (-10, 32), (10, 37), (25, 32), (35, 30), (40, 25),
                    (42, 15), (50, 12), (52, 5), (48, -5), (42, -10), (40, -15),
                    (35, -25), (30, -32), (22, -35), (18, -34), (12, -32),
                    (8, -28), (5, -20), (0, -10), (-5, 0), (-8, 10), (-12, 18),
                    (-15, 24), (-18, 28)
                ],
                'North America': [
                    (-170, 65), (-160, 68), (-145, 70), (-130, 70), (-110, 72),
                    (-95, 70), (-80, 68), (-70, 62), (-60, 50), (-65, 45),
                    (-75, 42), (-80, 38), (-85, 35), (-95, 30), (-105, 28),
                    (-110, 22), (-115, 18), (-105, 15), (-100, 18), (-95, 20),
                    (-88, 18), (-85, 15), (-82, 10), (-79, 8), (-95, 15),
                    (-110, 25), (-120, 32), (-125, 40), (-132, 52), (-145, 60),
                    (-160, 62), (-170, 65)
                ],
                'South America': [
                    (-80, 10), (-75, 8), (-70, 0), (-65, -5), (-60, -10),
                    (-55, -18), (-50, -25), (-45, -20), (-42, -15), (-38, -8),
                    (-35, 0), (-35, 5), (-40, 8), (-50, 10), (-60, 8),
                    (-70, 5), (-75, -2), (-78, -10), (-75, -20), (-70, -30),
                    (-68, -40), (-70, -48), (-72, -54), (-68, -55), (-58, -52),
                    (-52, -45), (-48, -35), (-46, -25), (-48, -15), (-52, -8),
                    (-58, -3), (-65, 0), (-72, 3), (-80, 10)
                ],
                'Australia': [
                    (113, -10), (125, -12), (135, -15), (142, -18), (148, -24),
                    (152, -32), (153, -38), (148, -42), (142, -40), (135, -36),
                    (128, -32), (120, -28), (115, -22), (112, -15), (113, -10)
                ],
                'Antarctica': [
                    (-180, -65), (-90, -68), (0, -70), (90, -68), (180, -65),
                    (180, -85), (-180, -85), (-180, -65)
                ]
            }
            
            # Create GeoDataFrame
            geometries = []
            names = []
            for name, coords in continents_data.items():
                geometries.append(Polygon(coords))
                names.append(name)
            
            world = gpd.GeoDataFrame({'name': names, 'geometry': geometries})
            
            # Create figure
            dpi = 100
            figsize = (width/dpi, height/dpi)
            fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
            
            # Plot the world map
            world.plot(
                ax=ax,
                color='#c8b896',  # Coffee-toned land
                edgecolor='#8b7355',
                linewidth=0.8,
                alpha=0.92
            )
            
            # Set ocean color
            ax.set_facecolor('#d4e8f7')
            fig.patch.set_facecolor('#d4e8f7')
            
            # Remove axis
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_visible(False)
            
            ax.set_xlim(-180, 180)
            ax.set_ylim(-90, 90)
            
            plt.tight_layout(pad=0)
            plt.savefig(save_path, dpi=dpi, bbox_inches='tight', pad_inches=0, facecolor='#d4e8f7')
            plt.close(fig)
            
            img = Image.open(save_path)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            img.save(save_path)
            
            print(f"✓ World map created successfully!")
            return img
        
        except Exception as e:
            print(f"Error creating GeoPandas map: {e}")
            return self.create_custom_world_map(width, height)
    
    def create_custom_world_map(self, width, height):
        """Create a custom world map with continent shapes"""
        img = Image.new('RGB', (width, height), color='#d4e8f7')
        draw = ImageDraw.Draw(img)
        
        # Africa
        africa_points = [
            (width*0.47, height*0.33), (width*0.54, height*0.32),
            (width*0.56, height*0.38), (width*0.57, height*0.50),
            (width*0.55, height*0.65), (width*0.52, height*0.70),
            (width*0.48, height*0.72), (width*0.45, height*0.68),
            (width*0.44, height*0.58), (width*0.43, height*0.48),
            (width*0.45, height*0.38), (width*0.47, height*0.33)
        ]
        draw.polygon(africa_points, fill='#c8b896', outline='#8b7355', width=2)
        
        # South America
        sa_points = [
            (width*0.24, height*0.48), (width*0.30, height*0.47),
            (width*0.32, height*0.52), (width*0.31, height*0.62),
            (width*0.28, height*0.72), (width*0.25, height*0.75),
            (width*0.22, height*0.72), (width*0.21, height*0.62),
            (width*0.22, height*0.52), (width*0.24, height*0.48)
        ]
        draw.polygon(sa_points, fill='#c8b896', outline='#8b7355', width=2)
        
        # Asia
        asia_points = [
            (width*0.55, height*0.15), (width*0.85, height*0.15),
            (width*0.90, height*0.25), (width*0.87, height*0.35),
            (width*0.82, height*0.42), (width*0.77, height*0.45),
            (width*0.70, height*0.45), (width*0.65, height*0.48),
            (width*0.60, height*0.52), (width*0.55, height*0.50),
            (width*0.52, height*0.45), (width*0.50, height*0.35),
            (width*0.52, height*0.25), (width*0.55, height*0.15)
        ]
        draw.polygon(asia_points, fill='#c8b896', outline='#8b7355', width=2)
        
        # North America
        na_points = [
            (width*0.15, height*0.20), (width*0.28, height*0.18),
            (width*0.32, height*0.25), (width*0.30, height*0.35),
            (width*0.25, height*0.42), (width*0.20, height*0.45),
            (width*0.15, height*0.42), (width*0.12, height*0.35),
            (width*0.13, height*0.25), (width*0.15, height*0.20)
        ]
        draw.polygon(na_points, fill='#c8b896', outline='#8b7355', width=2)
        
        # Australia
        australia_points = [
            (width*0.72, height*0.60), (width*0.82, height*0.58),
            (width*0.85, height*0.62), (width*0.84, height*0.68),
            (width*0.80, height*0.72), (width*0.75, height*0.73),
            (width*0.71, height*0.70), (width*0.70, height*0.64),
            (width*0.72, height*0.60)
        ]
        draw.polygon(australia_points, fill='#c8b896', outline='#8b7355', width=2)
        
        return img
    
    def create_world_map(self):
        """Create the interactive world map"""
        width = 1200
        height = 600
        
        # Get or create base map
        img = self.get_world_map_image(width, height)
        draw = ImageDraw.Draw(img)
        
        # Load coffee regions from database and plot markers
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM regions")
            regions = cursor.fetchall()
            
            for region in regions:
                # Convert lat/long to pixel coordinates
                x = int((region['longitude'] + 180) * (width / 360))
                y = int((90 - region['latitude']) * (height / 180))
                
                marker_size = 12
                
                # Draw outer glow/shadow for visibility
                for offset in range(4, 0, -1):
                    alpha = int(60 - offset * 10)
                    # Create temporary RGBA image for shadow
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    shadow_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                    shadow_draw = ImageDraw.Draw(shadow_layer)
                    shadow_draw.ellipse([x-marker_size-offset, y-marker_size-offset,
                                        x+marker_size+offset, y+marker_size+offset],
                                       fill=(111, 78, 55, alpha))  # Coffee brown with alpha
                    img = Image.alpha_composite(img, shadow_layer)
                
                # Convert back to RGB for drawing
                img = img.convert('RGB')
                draw = ImageDraw.Draw(img)
                
                # Draw main marker (coffee brown pin shape with border)
                # Outer border (white for contrast)
                draw.ellipse([x-marker_size-2, y-marker_size-2, x+marker_size+2, y+marker_size+2],
                           fill='white', outline='white')
                # Main pin body (coffee brown)
                draw.ellipse([x-marker_size, y-marker_size, x+marker_size, y+marker_size],
                           fill='#6F4E37', outline='#3E2723', width=3)
                # Pin highlight (lighter brown for 3D effect)
                draw.ellipse([x-marker_size//2, y-marker_size//2,
                            x+marker_size//2, y+marker_size//2],
                           fill='#8B5A3C')
                
                # Store region data
                self.map_regions.append({
                    'name': region['name'],
                    'country': region['country'],
                    'x': x,
                    'y': y,
                    'radius': marker_size + 4,
                    'data': dict(region)
                })
        
        except Exception as e:
            print(f"Error loading regions: {e}")
        
        # Add title and legend with backgrounds for visibility
        try:
            from PIL import ImageFont
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
                small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
            except:
                try:
                    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
                    small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 14)
                except:
                    font = ImageFont.load_default()
                    small_font = ImageFont.load_default()
        except:
            font = None
            small_font = None
        
        if font:
            # Title with background
            title_text = "Major Coffee-Growing Regions of the World"
            title_bbox = draw.textbbox((0, 0), title_text, font=font)
            title_width = title_bbox[2] - title_bbox[0]
            title_height = title_bbox[3] - title_bbox[1]
            title_x = width//2 - title_width//2
            title_y = 15
            
            # Draw semi-transparent background for title
            padding = 10
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            title_bg = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            title_bg_draw = ImageDraw.Draw(title_bg)
            title_bg_draw.rectangle([title_x - padding, title_y - padding,
                                     title_x + title_width + padding, title_y + title_height + padding],
                                    fill=(255, 255, 255, 220), outline=(111, 78, 55, 255), width=3)
            img = Image.alpha_composite(img, title_bg)
            img = img.convert('RGB')
            draw = ImageDraw.Draw(img)
            
            draw.text((title_x, title_y), title_text, fill='#6F4E37', font=font)
            
            # Legend with background
            legend_x = 40
            legend_y = height - 60
            legend_text = " = Coffee-growing region (click for details)"
            legend_bbox = draw.textbbox((0, 0), legend_text, font=small_font)
            legend_width = legend_bbox[2] - legend_bbox[0]
            legend_height = legend_bbox[3] - legend_bbox[1]
            
            # Draw legend background
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            legend_bg = Image.new('RGBA', (width, height), (0, 0, 0, 0))
            legend_bg_draw = ImageDraw.Draw(legend_bg)
            legend_bg_draw.rectangle([legend_x - 10, legend_y - 5,
                                     legend_x + 30 + legend_width + 10, legend_y + legend_height + 5],
                                    fill=(255, 255, 255, 200))
            img = Image.alpha_composite(img, legend_bg)
            img = img.convert('RGB')
            draw = ImageDraw.Draw(img)
            
            # Draw legend marker
            marker_x = legend_x + 10
            marker_y = legend_y + legend_height//2
            draw.ellipse([marker_x-8, marker_y-8, marker_x+8, marker_y+8],
                        fill='#6F4E37', outline='#3E2723', width=2)
            
            # Draw legend text
            draw.text((marker_x + 15, legend_y), legend_text, fill='#3E2723', font=small_font)
        
        # Convert to PhotoImage and display
        self.map_image = ImageTk.PhotoImage(img)
        self.map_canvas.create_image(0, 0, anchor=tk.NW, image=self.map_image)
        self.map_canvas.config(scrollregion=self.map_canvas.bbox(tk.ALL))
    
    def on_map_click(self, event):
        """Handle map click"""
        for region in self.map_regions:
            dx = event.x - region['x']
            dy = event.y - region['y']
            if dx*dx + dy*dy <= region['radius']*region['radius']:
                self.show_region_details(region['data'])
                break
    
    def on_map_hover(self, event):
        """Handle map hover"""
        for region in self.map_regions:
            dx = event.x - region['x']
            dy = event.y - region['y']
            if dx*dx + dy*dy <= region['radius']*region['radius']:
                self.map_canvas.config(cursor="hand2")
                return
        self.map_canvas.config(cursor="")
    
    def show_region_details(self, region_data):
        """Show region details in popup"""
        popup = tk.Toplevel(self.root)
        popup.title(f"Coffee Region - {region_data['name']}")
        popup.geometry("500x400")
        popup.transient(self.root)
        
        details_text = scrolledtext.ScrolledText(popup, wrap=tk.WORD, font=('Arial', 10))
        details_text.pack(fill='both', expand=True, padx=10, pady=10)
        
        details_text.tag_configure('title', font=('Arial', 14, 'bold'), foreground='#6F4E37')
        details_text.tag_configure('header', font=('Arial', 11, 'bold'))
        details_text.tag_configure('value', font=('Arial', 10))
        
        details_text.insert(tk.END, f"{region_data['name']}\n", 'title')
        details_text.insert(tk.END, f"{region_data['country']}\n\n", 'header')
        
        details_text.insert(tk.END, "📍 Location\n", 'header')
        details_text.insert(tk.END,
            f"Coordinates: {region_data['latitude']}°, {region_data['longitude']}°\n", 'value')
        details_text.insert(tk.END,
            f"Elevation: {region_data['elevation_min']}-{region_data['elevation_max']}m\n\n", 'value')
        
        details_text.insert(tk.END, "🌤️ Climate\n", 'header')
        details_text.insert(tk.END, f"{region_data['climate']}\n\n", 'value')
        
        details_text.insert(tk.END, "🌱 Soil Type\n", 'header')
        details_text.insert(tk.END, f"{region_data['soil_type']}\n\n", 'value')
        
        details_text.insert(tk.END, "☕ Famous Coffees\n", 'header')
        details_text.insert(tk.END, f"{region_data['famous_coffees']}\n\n", 'value')
        
        details_text.insert(tk.END, "📝 Description\n", 'header')
        details_text.insert(tk.END, f"{region_data['description']}\n", 'value')
        
        details_text.config(state='disabled')
        
        ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)
    
    # ==============================================
    # GUIDE AND HISTORY FUNCTIONS
    # ==============================================
    
    def load_guide(self):
        """Load coffee guide from markdown file"""
        self.guide_text.delete('1.0', tk.END)
        
        if os.path.exists(self.guide_path):
            try:
                with open(self.guide_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Simple markdown rendering
                for line in content.split('\n'):
                    if line.startswith('# '):
                        self.guide_text.insert(tk.END, line[2:] + '\n', 'title')
                    elif line.startswith('## '):
                        self.guide_text.insert(tk.END, '\n' + line[3:] + '\n', 'heading')
                    elif line.startswith('### '):
                        self.guide_text.insert(tk.END, '\n' + line[4:] + '\n', 'subheading')
                    else:
                        self.guide_text.insert(tk.END, line + '\n')
                
                self.guide_text.see('1.0')
            except Exception as e:
                self.guide_text.insert(tk.END, f"Error loading guide: {e}")
        else:
            self.guide_text.insert(tk.END, "Coffee guide file not found.\n\n")
            self.guide_text.insert(tk.END, "Please ensure coffee_guide.md is in the same directory as the application.")
    
    def load_history(self):
        """Load coffee history from markdown file"""
        self.history_text.delete('1.0', tk.END)
        
        if os.path.exists(self.history_path):
            try:
                with open(self.history_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Simple markdown rendering
                for line in content.split('\n'):
                    if line.startswith('# '):
                        self.history_text.insert(tk.END, line[2:] + '\n', 'title')
                    elif line.startswith('## '):
                        self.history_text.insert(tk.END, '\n' + line[3:] + '\n', 'heading')
                    elif line.startswith('### '):
                        self.history_text.insert(tk.END, '\n' + line[4:] + '\n', 'subheading')
                    else:
                        self.history_text.insert(tk.END, line + '\n')
                
                self.history_text.see('1.0')
            except Exception as e:
                self.history_text.insert(tk.END, f"Error loading history: {e}")
        else:
            self.history_text.insert(tk.END, "Coffee history file not found.\n\n")
            self.history_text.insert(tk.END, "Please ensure coffee_history.md is in the same directory as the application.")
    
    # ==============================================
    # MAP FUNCTIONS
    # ==============================================
    
    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About Coffee Collection Explorer",
            "Coffee Collection Explorer v1.1\n\n"
            "A comprehensive coffee database browser\n\n"
            "Features:\n"
            "• 29 coffee origins worldwide\n"
            "• 20 coffee varieties/cultivars\n"
            "• 28 coffee roasters & brands\n"
            "• 61 coffee products\n"
            "• 12 brewing methods with timer\n"
            "• Tasting journal\n"
            "• Complete coffee guide\n"
            "• Comprehensive coffee history\n"
            "• Interactive world map\n\n"
            "Explore the wonderful world of coffee!"
        )

def main():
    """Main entry point"""
    # Initialize database if needed
    if not os.path.exists("coffee_collection.db"):
        import coffee_database
        db = coffee_database.CoffeeDatabase()
        db.initialize_database()
    
    # Create and run GUI
    root = tk.Tk()
    app = CoffeeExplorerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
