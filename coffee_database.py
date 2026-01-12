"""
Coffee Database Creation and Management
Creates and populates a SQLite database with comprehensive coffee information

Includes:
- Coffee varieties and origins
- Processing methods and roast levels
- Growing regions worldwide
- Coffee roasters and brands
- Products and pricing
- Brewing methods
"""

import sqlite3
import os

class CoffeeDatabase:
    def __init__(self, db_path="coffee_collection.db"):
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """Establish database connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    def drop_tables(self):
        """Drop existing tables for fresh start"""
        self.cursor.execute('DROP TABLE IF EXISTS coffees')
        self.cursor.execute('DROP TABLE IF EXISTS regions')
        self.cursor.execute('DROP TABLE IF EXISTS varieties')
        self.cursor.execute('DROP TABLE IF EXISTS brewing_methods')
        self.cursor.execute('DROP TABLE IF EXISTS products')
        self.cursor.execute('DROP TABLE IF EXISTS distribution')
        self.cursor.execute('DROP TABLE IF EXISTS roasters')
        self.conn.commit()
    
    def create_tables(self):
        """Create database tables"""
        
        # Coffee varieties/origins table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS coffees (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                origin_country TEXT NOT NULL,
                origin_region TEXT,
                variety TEXT,
                processing_method TEXT,
                roast_level TEXT,
                flavor_profile TEXT,
                aroma TEXT,
                body TEXT,
                acidity TEXT,
                altitude_min INTEGER,
                altitude_max INTEGER,
                harvest_season TEXT,
                caffeine_content TEXT,
                cupping_score REAL,
                tasting_notes TEXT,
                history TEXT,
                price_range TEXT
            )
        ''')
        
        # Coffee growing regions table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS regions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                country TEXT NOT NULL,
                latitude REAL,
                longitude REAL,
                elevation_min INTEGER,
                elevation_max INTEGER,
                climate TEXT,
                soil_type TEXT,
                famous_coffees TEXT,
                description TEXT
            )
        ''')
        
        # Coffee varieties/cultivars table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS varieties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                species TEXT,
                origin_country TEXT,
                discovered_year INTEGER,
                characteristics TEXT,
                flavor_notes TEXT,
                disease_resistance TEXT,
                yield TEXT,
                notes TEXT
            )
        ''')
        
        # Brewing methods table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS brewing_methods (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                category TEXT,
                grind_size TEXT,
                water_temp_c INTEGER,
                water_temp_f INTEGER,
                brew_time TEXT,
                coffee_water_ratio TEXT,
                equipment_needed TEXT,
                difficulty_level TEXT,
                flavor_characteristics TEXT,
                description TEXT
            )
        ''')
        
        # Coffee roasters/brands table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS roasters (
                roaster_id INTEGER PRIMARY KEY AUTOINCREMENT,
                roaster_name TEXT NOT NULL,
                parent_company TEXT,
                founded_year INTEGER,
                headquarters_city TEXT,
                country_of_origin TEXT NOT NULL,
                website TEXT,
                certifications TEXT,
                market_segment TEXT CHECK(market_segment IN ('mass-market', 'premium', 'specialty', 'luxury')),
                roasting_style TEXT,
                description TEXT
            )
        ''')
        
        # Coffee products table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                roaster_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                coffee_type TEXT CHECK(coffee_type IN ('single-origin', 'blend', 'espresso', 'decaf', 'flavored', 'instant', 'cold-brew')),
                roast_level TEXT CHECK(roast_level IN ('light', 'medium-light', 'medium', 'medium-dark', 'dark', 'espresso')),
                format TEXT,
                weight_oz REAL,
                weight_g REAL,
                price REAL,
                price_currency TEXT CHECK(price_currency IN ('GBP', 'USD', 'EUR', 'AUD', 'CAD')),
                countries_available TEXT,
                organic BOOLEAN DEFAULT 0,
                fair_trade BOOLEAN DEFAULT 0,
                single_origin BOOLEAN DEFAULT 0,
                special_features TEXT,
                FOREIGN KEY (roaster_id) REFERENCES roasters(roaster_id)
            )
        ''')
        
        # Distribution table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS distribution (
                distribution_id INTEGER PRIMARY KEY AUTOINCREMENT,
                roaster_id INTEGER NOT NULL,
                country TEXT NOT NULL,
                distribution_type TEXT CHECK(distribution_type IN ('retail', 'online', 'wholesale', 'cafes')),
                retailers TEXT,
                FOREIGN KEY (roaster_id) REFERENCES roasters(roaster_id)
            )
        ''')
        
        self.conn.commit()
    
    def populate_coffees(self):
        """Populate coffee varieties and origins"""
        coffees_data = [
            # Ethiopian Coffees
            ("Yirgacheffe", "Ethiopia", "Gedeo Zone, Sidamo", "Heirloom varieties", "Washed",
             "Light to Medium", "Floral, citrus, tea-like, bergamot",
             "Jasmine, lemongrass, peach", "Light to medium, silky", "Bright, wine-like",
             1700, 2200, "October to January", "Medium (1.2-1.5%)", 86.5,
             "Bergamot, lemon, jasmine, peach, blueberry", 
             "One of the world's most distinctive coffees from the birthplace of coffee. Yirgacheffe is known for its floral, tea-like qualities.",
             "$$$"),
            
            ("Sidamo", "Ethiopia", "Sidamo Province", "Heirloom varieties", "Natural/Washed",
             "Light to Medium", "Berry, wine-like, chocolate, spice",
             "Blueberry, dark chocolate", "Medium, syrupy", "Moderate, balanced",
             1500, 2200, "October to January", "Medium (1.2-1.5%)", 85.0,
             "Blueberry, wine, dark chocolate, spice",
             "From the Sidamo highlands, producing coffees with complex berry notes and wine-like characteristics.",
             "$$$"),
            
            ("Harrar", "Ethiopia", "Eastern Highlands", "Heirloom varieties", "Natural (dry)",
             "Medium", "Blueberry, wine-like, earthy, mocha",
             "Blueberry, cocoa, wine", "Full, winey", "Moderate, winey",
             1400, 2000, "November to February", "Medium (1.2-1.5%)", 84.0,
             "Wild blueberry, dark chocolate, wine, apricot",
             "Dry-processed Ethiopian coffee with distinctive blueberry and wine notes, one of the oldest coffee-growing regions.",
             "$$$"),
            
            # Colombian Coffees
            ("Colombian Supremo", "Colombia", "Various regions", "Caturra, Castillo, Colombia", "Washed",
             "Medium", "Caramel, nuts, chocolate, balanced",
             "Caramel, toasted nuts", "Medium, smooth", "Bright, clean",
             1200, 2000, "September to December, April to June", "Medium (1.2-1.5%)", 84.0,
             "Caramel, nuts, milk chocolate, citrus",
             "Colombian Supremo refers to the largest bean size. Known for balanced, mild flavor and consistent quality.",
             "$$"),
            
            ("Huila", "Colombia", "Huila Department", "Caturra, Colombia, Castillo", "Washed",
             "Light to Medium", "Caramel, tropical fruit, citrus",
             "Caramel, red fruit, citrus", "Medium, creamy", "Bright, lively",
             1200, 2000, "April to June, October to December", "Medium (1.2-1.5%)", 86.0,
             "Caramel, orange, red apple, cane sugar",
             "Southern Colombian region producing some of the country's finest coffees with bright acidity and sweet caramel notes.",
             "$$$"),
            
            ("Nariño", "Colombia", "Nariño Department", "Caturra, Castillo", "Washed",
             "Light to Medium", "Citrus, floral, honey, complex",
             "Orange blossom, honey", "Light, delicate", "Very bright, citric",
             1700, 2300, "April to June", "Medium (1.2-1.5%)", 87.0,
             "Orange, honey, floral, apricot, brown sugar",
             "High-altitude Colombian region near Ecuador producing exceptionally bright, complex coffees.",
             "$$$$"),
            
            # Kenyan Coffees
            ("Kenya AA", "Kenya", "Central Highlands", "SL28, SL34, Ruiru 11", "Washed",
             "Light to Medium", "Blackcurrant, citrus, wine-like, complex",
             "Blackcurrant, grapefruit, tomato", "Full, juicy", "Very bright, intense",
             1400, 2000, "October to December, May to July", "Medium (1.2-1.5%)", 87.5,
             "Blackcurrant, grapefruit, wine, tomato, brown sugar",
             "AA grade refers to the largest bean size. Kenyan coffee is known for intense brightness and distinctive blackcurrant notes.",
             "$$$$"),
            
            # Costa Rican Coffees
            ("Tarrazú", "Costa Rica", "Tarrazú Region", "Caturra, Catuai", "Washed",
             "Medium", "Chocolate, citrus, honey, clean",
             "Chocolate, citrus, honey", "Full, creamy", "Bright, crisp",
             1200, 1900, "November to March", "Medium (1.2-1.5%)", 85.5,
             "Milk chocolate, orange, honey, almond",
             "From the slopes of the Poas and Barva volcanoes, known for clean, bright profile with chocolate notes.",
             "$$$"),
            
            # Guatemalan Coffees
            ("Antigua", "Guatemala", "Antigua Valley", "Bourbon, Caturra, Catuai", "Washed",
             "Medium", "Chocolate, spice, floral, balanced",
             "Cocoa, spice, floral", "Full, velvety", "Bright, balanced",
             1500, 1700, "December to March", "Medium (1.2-1.5%)", 85.0,
             "Dark chocolate, spice, smoke, floral",
             "Grown in volcanic soil near three volcanoes, produces coffee with distinctive spicy, smoky chocolate notes.",
             "$$$"),
            
            ("Huehuetenango", "Guatemala", "Huehuetenango Region", "Bourbon, Caturra, Catuai", "Washed",
             "Light to Medium", "Fruit, wine, chocolate, floral",
             "Red fruit, wine, cocoa", "Medium, silky", "Bright, lively",
             1500, 2000, "January to April", "Medium (1.2-1.5%)", 86.0,
             "Red fruit, wine, chocolate, floral, citrus",
             "Highest and most remote region in Guatemala, protected from frost and producing exceptional quality.",
             "$$$"),
            
            # Brazilian Coffees
            ("Santos", "Brazil", "São Paulo State", "Bourbon, Mundo Novo", "Natural/Pulped Natural",
             "Medium to Dark", "Chocolate, nuts, caramel, low acidity",
             "Chocolate, peanut, caramel", "Heavy, creamy", "Low, mellow",
             600, 1200, "May to September", "Medium (1.2-1.5%)", 82.0,
             "Chocolate, peanuts, caramel, brown sugar",
             "Brazil's most famous coffee export, known for chocolate and nutty notes with low acidity. Ideal for espresso.",
             "$$"),
            
            ("Cerrado", "Brazil", "Cerrado Region, Minas Gerais", "Catuai, Mundo Novo", "Natural/Pulped Natural",
             "Medium", "Chocolate, caramel, nuts, sweet",
             "Chocolate, caramel, nuts", "Medium-full, smooth", "Low-medium, sweet",
             800, 1300, "May to September", "Medium (1.2-1.5%)", 83.5,
             "Chocolate, caramel, hazelnut, sweet",
             "First Brazilian region to receive PDO status, known for consistent quality and sweet, chocolatey profile.",
             "$$"),
            
            # Jamaican Coffee
            ("Jamaica Blue Mountain", "Jamaica", "Blue Mountain Region", "Typica", "Washed",
             "Light to Medium", "Mild, sweet, floral, clean",
             "Floral, herbal, sweet", "Light, smooth", "Low, mild",
             900, 1700, "September to April", "Low-Medium (1.0-1.2%)", 86.0,
             "Floral, mild, sweet, herbal, chocolate",
             "One of the world's most expensive coffees, grown in the Blue Mountains. Exceptionally smooth and mild with no bitterness.",
             "$$$$$"),
            
            # Hawaiian Coffee
            ("Kona", "USA (Hawaii)", "Kona District, Big Island", "Typica", "Washed",
             "Medium", "Smooth, sweet, nutty, mild",
             "Nuts, spice, brown sugar", "Medium, smooth", "Low-medium, gentle",
             150, 900, "September to January", "Medium (1.2-1.5%)", 84.0,
             "Nuts, brown sugar, chocolate, mild fruit",
             "Grown on the volcanic slopes of Mauna Loa. One of the most expensive coffees due to high labor costs and limited supply.",
             "$$$$"),
            
            # Indonesian Coffees
            ("Sumatra Mandheling", "Indonesia", "North Sumatra", "Typica, Catimor", "Giling Basah (wet-hulled)",
             "Dark", "Earthy, herbal, low acidity, full body",
             "Earth, cedar, herbs, dark chocolate", "Very full, syrupy", "Very low, mellow",
             750, 1500, "September to December, June to July", "Medium (1.2-1.5%)", 82.0,
             "Earth, cedar, herbs, dark chocolate, tobacco",
             "Unique wet-hulled processing creates distinctive earthy, full-bodied profile. Named after Mandailing people.",
             "$$"),
            
            ("Java", "Indonesia", "Java Island", "Typica, S795", "Washed/Semi-washed",
             "Medium to Dark", "Earthy, spicy, chocolate, full body",
             "Spice, earth, chocolate", "Heavy, syrupy", "Low, mellow",
             900, 1800, "May to September", "Medium (1.2-1.5%)", 81.0,
             "Earthy, spicy, chocolate, tobacco",
             "One of the original coffee islands, giving its name to the slang term for coffee. Rich and full-bodied.",
             "$$"),
            
            ("Sulawesi Toraja", "Indonesia", "Toraja Region, Sulawesi", "S795, Typica", "Washed/Semi-washed",
             "Medium to Dark", "Earthy, herbal, dark fruit, full body",
             "Earth, dark fruit, spice", "Full, creamy", "Low, smooth",
             1200, 1800, "May to November", "Medium (1.2-1.5%)", 83.0,
             "Earthy, dark fruit, spice, chocolate",
             "Grown in the Toraja highlands, known for full body and complex earthy flavors.",
             "$$$"),
            
            # Vietnamese Coffee
            ("Vietnamese Robusta", "Vietnam", "Central Highlands", "Robusta", "Natural",
             "Dark", "Chocolate, bitter, nutty, strong",
             "Dark chocolate, roasted nuts", "Very heavy, thick", "Low",
             500, 800, "October to April", "High (2.2-2.7%)", 78.0,
             "Dark chocolate, bitter, nutty, earthy",
             "Vietnam is the world's largest Robusta producer. Strong, bitter, ideal for Vietnamese iced coffee with condensed milk.",
             "$"),
            
            # Panamanian Coffee
            ("Geisha (Panama)", "Panama", "Boquete Region", "Geisha/Gesha", "Washed",
             "Light", "Floral, jasmine, bergamot, tea-like, complex",
             "Jasmine, bergamot, tropical fruit", "Light, tea-like", "Bright, delicate",
             1400, 1900, "December to March", "Medium (1.2-1.5%)", 92.0,
             "Jasmine, bergamot, tropical fruit, peach, mango",
             "One of the world's most expensive and sought-after coffees. Extraordinary floral complexity, often scoring 90+.",
             "$$$$$"),
            
            # Rwandan Coffee
            ("Rwanda Bourbon", "Rwanda", "Various regions", "Red Bourbon", "Washed",
             "Light to Medium", "Citrus, floral, red fruit, tea-like",
             "Citrus, red fruit, floral", "Medium, silky", "Bright, clean",
             1700, 2000, "March to July", "Medium (1.2-1.5%)", 85.5,
             "Citrus, red fruit, floral, caramel",
             "Rwandan coffee has rapidly gained recognition for quality. Bourbon variety produces bright, clean cups.",
             "$$$"),
            
            # Burundi Coffee
            ("Burundi Bourbon", "Burundi", "Various regions", "Red Bourbon", "Washed",
             "Light to Medium", "Citrus, red fruit, floral, complex",
             "Red fruit, citrus, floral", "Medium, juicy", "Bright, lively",
             1250, 2000, "March to July", "Medium (1.2-1.5%)", 85.0,
             "Red fruit, citrus, floral, brown sugar",
             "Neighbor to Rwanda with similar terroir. Produces bright, fruity coffees with excellent acidity.",
             "$$$"),
            
            # Tanzanian Coffee
            ("Tanzania Peaberry", "Tanzania", "Mount Kilimanjaro, Arusha", "Kent, Bourbon", "Washed",
             "Medium", "Wine-like, citrus, black currant, full body",
             "Wine, blackcurrant, citrus", "Full, rich", "Bright, winey",
             1050, 1800, "July to December", "Medium (1.2-1.5%)", 84.5,
             "Wine, blackcurrant, citrus, chocolate",
             "Peaberry is a natural mutation (single round bean). Similar to Kenyan coffee with wine-like characteristics.",
             "$$$"),
            
            # Nicaraguan Coffee
            ("Matagalpa", "Nicaragua", "Matagalpa Region", "Caturra, Bourbon, Catuai", "Washed",
             "Medium", "Chocolate, caramel, fruit, balanced",
             "Chocolate, caramel, red fruit", "Medium, smooth", "Moderate, balanced",
             900, 1700, "November to March", "Medium (1.2-1.5%)", 84.0,
             "Chocolate, caramel, red fruit, nuts",
             "Northern Nicaraguan region producing balanced, chocolatey coffees with good body.",
             "$$"),
            
            # Mexican Coffee
            ("Chiapas", "Mexico", "Chiapas State", "Bourbon, Typica, Mundo Novo", "Washed",
             "Medium", "Chocolate, nuts, mild fruit, gentle",
             "Chocolate, nuts, mild", "Medium, smooth", "Moderate, gentle",
             900, 1700, "November to March", "Medium (1.2-1.5%)", 83.0,
             "Chocolate, nuts, caramel, mild",
             "Southern Mexican coffee region near Guatemala, producing mild, chocolatey coffees.",
             "$$"),
            
            # Peruvian Coffee
            ("Chanchamayo", "Peru", "Chanchamayo Valley", "Typica, Caturra, Bourbon", "Washed",
             "Medium", "Chocolate, nuts, citrus, balanced",
             "Chocolate, nuts, citrus", "Medium, smooth", "Moderate, bright",
             1000, 1800, "April to September", "Medium (1.2-1.5%)", 83.5,
             "Chocolate, nuts, citrus, floral",
             "Central Peruvian region producing balanced, chocolatey coffees often grown organically.",
             "$$"),
            
            # Honduran Coffee
            ("Marcala", "Honduras", "La Paz Department", "Bourbon, Catuai, Caturra, Pacas", "Washed",
             "Medium", "Chocolate, caramel, fruit, balanced",
             "Chocolate, caramel, fruit", "Medium, creamy", "Moderate, bright",
             1000, 1600, "November to March", "Medium (1.2-1.5%)", 84.0,
             "Chocolate, caramel, stone fruit, citrus",
             "First Honduran region to receive PDO status. Produces balanced, sweet coffees.",
             "$$"),
            
            # El Salvador Coffee
            ("Pacamara (El Salvador)", "El Salvador", "Santa Ana, Ahuachapan", "Pacamara", "Washed",
             "Light to Medium", "Floral, fruit, chocolate, complex",
             "Floral, tropical fruit, chocolate", "Full, creamy", "Bright, complex",
             1200, 1800, "November to March", "Medium (1.2-1.5%)", 86.0,
             "Floral, tropical fruit, chocolate, citrus",
             "Pacamara is a hybrid of Pacas and Maragogipe. Large beans with complex, fruity profile.",
             "$$$"),
            
            # Yemen Coffee
            ("Yemen Mocha", "Yemen", "Various regions", "Typica variants", "Natural (dry)",
             "Medium to Dark", "Wine-like, chocolate, spice, wild",
             "Wine, chocolate, spice, earth", "Full, winey", "Moderate, winey",
             1000, 2400, "October to December", "Medium (1.2-1.5%)", 83.0,
             "Wine, chocolate, spice, wild berry, earth",
             "Birthplace of commercial coffee cultivation. Mocha (Al Mukha) was the port of export. Complex, wild, wine-like.",
             "$$$$"),
            
            # Indian Coffee
            ("Monsooned Malabar", "India", "Malabar Coast, Karnataka/Kerala", "Kent, S795", "Monsooned",
             "Medium to Dark", "Low acidity, musty, earthy, spice",
             "Musty, earth, spice, wood", "Very heavy, syrupy", "Very low",
             800, 1200, "December to February", "Medium (1.2-1.5%)", 80.0,
             "Musty, earthy, spice, wood, chocolate",
             "Unique monsoon processing exposes beans to monsoon winds, creating distinctive low-acid, heavy-bodied profile.",
             "$$"),
        ]
        
        self.cursor.executemany('''
            INSERT INTO coffees (name, origin_country, origin_region, variety, processing_method,
                               roast_level, flavor_profile, aroma, body, acidity,
                               altitude_min, altitude_max, harvest_season, caffeine_content, cupping_score,
                               tasting_notes, history, price_range)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', coffees_data)
        
        self.conn.commit()
        print(f"✓ Inserted {len(coffees_data)} coffee varieties")
    
    def populate_varieties(self):
        """Populate coffee varieties/cultivars"""
        varieties_data = [
            ("Typica", "Arabica", "Yemen/Ethiopia", 1600,
             "Original Arabica variety, tall plants, low yield, excellent quality",
             "Sweet, clean, complex", "Susceptible to diseases", "Low",
             "Foundation variety from which many others derive"),
            
            ("Bourbon", "Arabica", "Yemen (via Bourbon Island)", 1700,
             "Natural mutation of Typica, higher yield, excellent quality",
             "Sweet, complex, balanced", "Susceptible to diseases", "Medium",
             "Named after Bourbon Island (Réunion), basis for many quality coffees"),
            
            ("Geisha/Gesha", "Arabica", "Ethiopia (Gesha village)", 1930,
             "Discovered in Ethiopia, popularized in Panama, extraordinary quality",
             "Floral, jasmine, bergamot, tea-like", "Good disease resistance", "Low-Medium",
             "Can score 90+ in competitions, fetches record auction prices"),
            
            ("SL28", "Arabica", "Kenya", 1930,
             "Selected by Scott Labs in Kenya, drought tolerant, exceptional quality",
             "Blackcurrant, citrus, complex", "Moderate", "Medium",
             "One of Kenya's signature varieties, distinctive blackcurrant notes"),
            
            ("SL34", "Arabica", "Kenya", 1930,
             "Selected by Scott Labs, excellent in high rainfall areas",
             "Complex, wine-like, citrus", "Moderate", "Medium",
             "Complementary to SL28 in Kenyan blends"),
            
            ("Caturra", "Arabica", "Brazil", 1937,
             "Natural mutation of Bourbon, compact size, good yield",
             "Bright acidity, sweet", "Susceptible to diseases", "Medium-High",
             "Popular in Latin America, easier to harvest due to compact size"),
            
            ("Catuai", "Arabica", "Brazil", 1950,
             "Hybrid of Mundo Novo and Caturra, compact, productive",
             "Sweet, mild, balanced", "Moderate", "High",
             "Popular commercial variety, stable cherry attachment"),
            
            ("Mundo Novo", "Arabica", "Brazil", 1940,
             "Natural hybrid of Typica and Bourbon, vigorous, high yield",
             "Sweet, chocolate, nutty", "Moderate", "High",
             "Important Brazilian variety, foundation for many hybrids"),
            
            ("Pacamara", "Arabica", "El Salvador", 1958,
             "Hybrid of Pacas and Maragogipe, large beans, complex",
             "Floral, fruit, chocolate, complex", "Moderate", "Medium",
             "Large bean size, capable of exceptional quality"),
            
            ("Castillo", "Arabica", "Colombia", 2005,
             "Developed for disease resistance, maintains quality",
             "Balanced, chocolate, caramel", "Excellent (rust resistant)", "High",
             "Modern variety replacing traditional Colombian types"),
            
            ("Timor Hybrid", "Arabica-Robusta hybrid", "Timor", 1940,
             "Natural hybrid with Robusta genes, disease resistant",
             "Variable, depends on cross", "Excellent (rust resistant)", "High",
             "Foundation for many modern disease-resistant varieties"),
            
            ("Catimor", "Arabica-Robusta hybrid", "Portugal", 1959,
             "Cross of Caturra and Timor Hybrid, disease resistant",
             "Variable, sometimes neutral", "Excellent (rust resistant)", "Very High",
             "High yield but sometimes compromised quality"),
            
            ("Ruiru 11", "Arabica-Robusta hybrid", "Kenya", 1985,
             "Disease resistant variety developed in Kenya",
             "Good but not exceptional", "Excellent (disease resistant)", "High",
             "CBD and rust resistant, compact plant"),
            
            ("Maragogipe", "Arabica", "Brazil", 1870,
             "Natural mutation of Typica, very large beans",
             "Mild, smooth, low acidity", "Susceptible", "Low",
             "Elephant bean, largest coffee bean, mild flavor"),
            
            ("Pacas", "Arabica", "El Salvador", 1949,
             "Natural mutation of Bourbon, compact size",
             "Sweet, balanced", "Susceptible", "Medium",
             "Important in El Salvador coffee industry"),
            
            ("Kent", "Arabica", "India", 1920,
             "Selected for disease resistance in India",
             "Balanced, moderate quality", "Good (rust tolerant)", "Medium",
             "Historical importance in Indian coffee"),
            
            ("S795", "Arabica", "India", 1940,
             "Cross of Kent and S228, disease resistant",
             "Balanced, moderate quality", "Good", "Medium-High",
             "Popular in India and Indonesia"),
            
            ("Villa Sarchi", "Arabica", "Costa Rica", 1950,
             "Natural mutation of Bourbon, compact",
             "Bright, sweet, complex", "Moderate", "Medium",
             "Boutique variety in Central America"),
            
            ("Colombia", "Arabica", "Colombia", 1982,
             "Cross involving Caturra, disease resistant",
             "Balanced, chocolate, caramel", "Good (rust resistant)", "High",
             "Widely planted in Colombia, replacing traditional varieties"),
            
            ("Robusta (Coffea canephora)", "Robusta", "Central/West Africa", 1800,
             "Separate species, hardy, high caffeine, lower quality",
             "Bitter, earthy, neutral", "Excellent (very hardy)", "Very High",
             "40% of world production, used in espresso blends and instant coffee"),
        ]
        
        self.cursor.executemany('''
            INSERT INTO varieties (name, species, origin_country, discovered_year,
                                 characteristics, flavor_notes, disease_resistance, yield, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', varieties_data)
        
        self.conn.commit()
        print(f"✓ Inserted {len(varieties_data)} coffee varieties/cultivars")
    
    def populate_regions(self):
        """Populate coffee-growing regions"""
        regions_data = [
            ("Sidamo/Gedeo", "Ethiopia", 6.0, 38.5, 1500, 2200,
             "Tropical highland, wet/dry seasons", "Volcanic loam",
             "Yirgacheffe, Sidamo", "Birthplace of Arabica coffee, home to Yirgacheffe"),
            
            ("Huila", "Colombia", 2.5, -75.9, 1200, 2000,
             "Tropical mountain", "Volcanic",
             "Huila, Colombian Supremo", "Southern Colombia, produces award-winning coffees"),
            
            ("Antigua Valley", "Guatemala", 14.6, -90.7, 1500, 1700,
             "Subtropical highland, volcanic", "Rich volcanic soil",
             "Antigua", "Surrounded by three volcanoes, unique microclimate"),
            
            ("Tarrazú", "Costa Rica", 9.5, -84.0, 1200, 1900,
             "Tropical highland", "Volcanic",
             "Tarrazú", "Famous Costa Rican region, Poas and Barva volcanoes"),
            
            ("Central Highlands (Kenya)", "Kenya", -0.5, 37.0, 1400, 2000,
             "Tropical highland", "Rich red volcanic",
             "Kenya AA, Kenya Peaberry", "Kiambu, Nyeri, Kirinyaga counties, known for brightness"),
            
            ("Kona District", "United States (Hawaii)", 19.6, -155.9, 150, 900,
             "Tropical volcanic", "Volcanic",
             "Kona", "Big Island slopes of Mauna Loa and Hualalai"),
            
            ("Blue Mountain", "Jamaica", 18.1, -76.7, 900, 1700,
             "Tropical mountain, frequent mist", "Volcanic loam",
             "Jamaica Blue Mountain", "Strict geographical designation, produces world's most expensive coffee"),
            
            ("Aceh/North Sumatra", "Indonesia", 4.5, 96.5, 750, 1500,
             "Tropical equatorial", "Volcanic",
             "Mandheling, Gayo Mountain", "Unique wet-hulling process, earthy characteristics"),
            
            ("Minas Gerais", "Brazil", -18.5, -44.0, 800, 1300,
             "Tropical savanna", "Red laterite clay",
             "Cerrado, Santos", "Largest coffee producing state in Brazil"),
            
            ("Boquete", "Panama", 8.8, -82.4, 1400, 1900,
             "Tropical highland", "Volcanic",
             "Geisha, Boquete", "Home to world-record Geisha auctions"),
            
            ("Western Highlands", "Papua New Guinea", -5.5, 144.5, 1200, 1800,
             "Tropical highland", "Volcanic",
             "PNG Highland", "Organic by default, similar profile to Indonesian coffees"),
            
            ("Kilimanjaro/Arusha", "Tanzania", -3.4, 37.2, 1050, 1800,
             "Tropical highland", "Volcanic",
             "Tanzania Peaberry", "Slopes of Mt. Kilimanjaro and Mt. Meru"),
            
            ("Chiapas", "Mexico", 16.5, -92.5, 900, 1700,
             "Tropical highland", "Volcanic",
             "Chiapas", "Southern Mexico near Guatemala border"),
            
            ("Jinotega/Matagalpa", "Nicaragua", 13.1, -86.0, 900, 1700,
             "Tropical highland", "Volcanic",
             "Matagalpa, Jinotega", "Northern Nicaragua, quality coffee regions"),
            
            ("Haraz Mountains", "Yemen", 15.5, 44.0, 1000, 2400,
             "Arid mountain", "Terraced mountainsides",
             "Yemen Mocha", "Birthplace of commercial coffee, ancient terraced farms"),
        ]
        
        self.cursor.executemany('''
            INSERT INTO regions (name, country, latitude, longitude, elevation_min, elevation_max,
                               climate, soil_type, famous_coffees, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', regions_data)
        
        self.conn.commit()
        print(f"✓ Inserted {len(regions_data)} coffee regions")
    
    def populate_brewing_methods(self):
        """Populate brewing methods"""
        brewing_data = [
            ("Espresso", "Pressure", "Fine", 93, 200, "25-30 seconds", "1:2 (18g coffee to 36g water)",
             "Espresso machine", "Moderate-High",
             "Concentrated, intense, crema, full body",
             "High pressure extraction creating concentrated shot with crema. Foundation for cappuccino, latte, etc."),
            
            ("Pour Over (V60)", "Filter", "Medium-fine", 92, 198, "2.5-3 minutes", "1:16 (15g to 240ml)",
             "V60 dripper, filters, kettle, scale", "Moderate",
             "Clean, bright, highlights acidity and complexity",
             "Japanese cone-shaped dripper with spiral ribs. Allows for precise control and clean extraction."),
            
            ("Chemex", "Filter", "Medium-coarse", 93, 200, "4-5 minutes", "1:15 (42g to 630ml)",
             "Chemex brewer, Chemex filters, kettle, scale", "Moderate",
             "Very clean, tea-like, delicate, bright",
             "Hourglass-shaped glass brewer with thick proprietary filters, produces exceptionally clean cup."),
            
            ("French Press", "Immersion", "Coarse", 93, 200, "4 minutes", "1:15 (30g to 450ml)",
             "French press, kettle, timer", "Easy",
             "Full body, rich, textured, some sediment",
             "Full immersion brewing with metal mesh filter. Allows oils and fine particles through for rich body."),
            
            ("AeroPress", "Immersion/Pressure", "Fine to medium", 80, 176, "1-2 minutes", "1:16 (17g to 272ml)",
             "AeroPress, filters, kettle, scale", "Easy-Moderate",
             "Versatile, clean to full body depending on method",
             "Portable brewer using air pressure. Extremely versatile with multiple brewing methods possible."),
            
            ("Moka Pot", "Pressure", "Fine", 100, 212, "4-5 minutes", "Fill to line (depends on size)",
             "Moka pot, stove", "Easy",
             "Strong, concentrated, espresso-like but different",
             "Stovetop brewer popular in Italy. Creates strong coffee through steam pressure, not true espresso."),
            
            ("Cold Brew", "Immersion", "Coarse", "Room temp/Cold", "Room temp", "12-24 hours", "1:8 (100g to 800ml)",
             "Container, filter, patience", "Easy (but slow)",
             "Smooth, low acidity, sweet, concentrated",
             "Long steep in cold water extracts different compounds, resulting in smooth, low-acid concentrate."),
            
            ("Siphon/Vacuum Pot", "Vacuum", "Medium", 90, 194, "1-3 minutes", "1:15 (30g to 450ml)",
             "Siphon brewer, heat source, filters", "High",
             "Clean, complex, full flavor, theatrical",
             "Uses vapor pressure and vacuum to brew. Theatrical and produces clean, complex cup."),
            
            ("Turkish/Ibrik", "Boiled", "Extra fine (powder)", 93, 200, "3-4 minutes", "1:9 (10g to 90ml)",
             "Ibrik/cezve, very fine grind", "Moderate",
             "Very strong, thick, unfiltered, sweet",
             "Ancient method boiling ultra-fine coffee with sugar. Traditional in Middle East and Eastern Europe."),
            
            ("Drip Coffee Maker", "Filter", "Medium", 93, 200, "5-6 minutes", "1:17 (60g to 1L)",
             "Automatic drip machine", "Very Easy",
             "Varies by machine, generally clean and balanced",
             "Automatic electric brewer. Convenient but quality varies significantly by machine."),
            
            ("Clever Dripper", "Immersion + Filter", "Medium-fine", 93, 200, "2.5-3 minutes", "1:16 (22g to 352ml)",
             "Clever dripper, filters, kettle", "Easy",
             "Clean but full-bodied, best of both methods",
             "Combines immersion brewing with paper filter. Easier than pour over, cleaner than French press."),
            
            ("Vietnamese Phin", "Drip", "Medium-fine", 93, 200, "4-5 minutes", "1:8 to 1:10 (15g to 150ml)",
             "Phin filter, condensed milk optional", "Easy",
             "Strong, sweet (with condensed milk), concentrated",
             "Small metal filter that slowly drips concentrated coffee. Traditionally served with condensed milk."),
        ]
        
        self.cursor.executemany('''
            INSERT INTO brewing_methods (name, category, grind_size, water_temp_c, water_temp_f,
                                       brew_time, coffee_water_ratio, equipment_needed, difficulty_level,
                                       flavor_characteristics, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', brewing_data)
        
        self.conn.commit()
        print(f"✓ Inserted {len(brewing_data)} brewing methods")
    
    def populate_roasters(self):
        """Populate coffee roasters and brands"""
        roasters_data = [
            # Major Commercial Brands
            ("Starbucks", "Starbucks Corporation", 1971, "Seattle", "USA", "starbucks.com",
             "C.A.F.E. Practices, Fairtrade (select)", "mass-market", "Dark roast focused",
             "World's largest coffee chain, Seattle-based, known for dark roasts and espresso drinks"),
            
            ("Dunkin'", "Inspire Brands", 1950, "Canton", "USA", "dunkindonuts.com",
             "Rainforest Alliance", "mass-market", "Medium roast focused",
             "Major US coffee and donut chain, emphasis on drip coffee and value"),
            
            ("Peet's Coffee", "JAB Holding Company", 1966, "Emeryville", "USA", "peets.com",
             "Organic (select), Rainforest Alliance", "premium", "Dark roast focused",
             "Founded by Alfred Peet, inspired Starbucks founders, known for dark roasts"),
            
            ("Lavazza", "Luigi Lavazza S.p.A.", 1895, "Turin", "Italy", "lavazza.com",
             "Rainforest Alliance, ¡Tierra! project", "premium", "Italian espresso style",
             "Italy's favorite coffee, family-owned, pioneer in blending and sustainability"),
            
            ("illy", "illycaffè S.p.A.", 1933, "Trieste", "Italy", "illy.com",
             "Direct trade, sustainability partnerships", "premium", "Medium espresso roast",
             "Premium Italian brand, single blend philosophy, pressurized packaging innovation"),
            
            ("Nescafé", "Nestlé", 1938, "Vevey", "Switzerland", "nescafe.com",
             "Rainforest Alliance (select)", "mass-market", "Instant coffee focused",
             "World's largest instant coffee brand, Nestlé's coffee division"),
            
            ("Folgers", "The J.M. Smucker Company", 1850, "Orrville", "USA", "folgers.com",
             "Rainforest Alliance (select)", "mass-market", "Medium roast",
             "America's best-selling coffee brand, known for slogan 'The Best Part of Waking Up'"),
            
            # Specialty Roasters
            ("Blue Bottle Coffee", "Nestlé (via JAB Holding)", 2002, "Oakland", "USA", "bluebottlecoffee.com",
             "Organic (select), Direct trade", "specialty", "Light to medium roasts",
             "Third-wave pioneer, emphasis on freshness and single-origin, acquired by Nestlé 2017"),
            
            ("Intelligentsia", "Peet's Coffee (JAB Holding)", 1995, "Chicago", "USA", "intelligentsiacoffee.com",
             "Direct Trade certified, Organic (select)", "specialty", "Light to medium roasts",
             "Third-wave pioneer, Direct Trade program, multiple US locations"),
            
            ("Counter Culture Coffee", "Independent", 1995, "Durham", "USA", "counterculturecoffee.com",
             "Organic, Direct Trade, B Corp", "specialty", "Light to medium roasts",
             "Specialty pioneer, transparency, sustainability, B Corp certified since 2009"),
            
            ("Stumptown Coffee Roasters", "Peet's Coffee (JAB Holding)", 1999, "Portland", "USA", "stumptowncoffee.com",
             "Direct Trade, Organic (select)", "specialty", "Light to medium roasts",
             "Portland-based third-wave pioneer, direct trade relationships, cold brew innovation"),
            
            ("La Colombe", "Independent", 1994, "Philadelphia", "USA", "lacolombe.com",
             "Direct Trade, B Corp", "specialty", "Medium roasts",
             "East Coast specialty leader, draft latte innovation, multiple cafes"),
            
            ("Verve Coffee Roasters", "Independent", 2007, "Santa Cruz", "USA", "vervecoffee.com",
             "Direct Trade, Organic (select), B Corp", "specialty", "Light roasts",
             "California-based specialty roaster, multiple locations, emphasis on direct relationships"),
            
            # International Specialty
            ("Tim Wendelboe", "Independent", 2007, "Oslo", "Norway", "timwendelboe.no",
             "Direct Trade, Sustainability focused", "specialty", "Light roasts",
             "World Barista Champion, micro-roaster, direct sourcing, education focused"),
            
            ("Square Mile Coffee Roasters", "Independent", 2008, "London", "UK", "squaremilecoffee.com",
             "Direct Trade, Relationship coffee", "specialty", "Light to medium roasts",
             "Founded by James Hoffmann (World Barista Champion), focus on quality and education"),
            
            ("Has Bean Coffee", "Independent", 2001, "Stafford", "UK", "hasbean.co.uk",
             "Direct Trade, In My Mug program", "specialty", "Light to medium roasts",
             "UK specialty pioneer, subscription model innovation, transparency"),
            
            ("Koppi", "Independent", 2007, "Helsingborg", "Sweden", "koppicoffee.se",
             "Direct Trade", "specialty", "Light roasts",
             "Scandinavian specialty leader, micro-lots, Nordic roasting style"),
            
            ("Coffee Collective", "Independent", 2007, "Copenhagen", "Denmark", "coffeecollective.dk",
             "Direct Trade, Organic (select)", "specialty", "Light roasts",
             "Copenhagen-based, democratic ownership, World Barista Championship titles"),
            
            ("Onibus Coffee", "Independent", 2012, "Tokyo", "Japan", "onibuscoffee.com",
             "Direct Trade, Relationship focused", "specialty", "Light to medium roasts",
             "Tokyo specialty leader, multiple locations, Japanese precision"),
            
            # Australian/NZ Specialty
            ("Five Senses Coffee", "Independent", 2000, "Perth", "Australia", "fivesenses.com.au",
             "Direct Trade, Organic (select)", "specialty", "Light to medium roasts",
             "Australian specialty pioneer, roasting education, multiple state presence"),
            
            ("Campos Coffee", "Independent", 2002, "Sydney", "Australia", "camposcoffee.com",
             "Direct Trade, Organic (select)", "specialty", "Medium roasts",
             "Sydney-based, large Australian presence, cafe culture leader"),
            
            ("Allpress Espresso", "Independent", 1986, "Auckland", "New Zealand", "allpressespresso.com",
             "Direct Trade, Organic (select)", "specialty", "Medium roasts",
             "New Zealand heritage, international expansion, consistent quality"),
            
            # Budget/Value Brands
            ("Eight O'Clock Coffee", "Tata Consumer Products", 1859, "Montvale", "USA", "eightoclock.com",
             "Rainforest Alliance (select)", "mass-market", "Medium roast",
             "America's original whole bean coffee, value-focused, grocery staple"),
            
            ("Maxwell House", "Kraft Heinz", 1892, "Chicago", "USA", "maxwellhousecoffee.com",
             "Rainforest Alliance (select)", "mass-market", "Medium roast",
             "Historic American brand, 'Good to the Last Drop' slogan since 1915"),
            
            # Instant/Ready-to-Drink
            ("Starbucks VIA", "Starbucks Corporation", 2009, "Seattle", "USA", "starbucks.com",
             "Various certifications", "premium", "Instant coffee",
             "Premium instant coffee line, single-serve packets"),
            
            ("Café Bustelo", "The J.M. Smucker Company", 1928, "New York", "USA", "cafebustelo.com",
             "Rainforest Alliance (select)", "mass-market", "Dark espresso roast",
             "Cuban-style coffee, strong espresso-style blend, Latino market leader"),
            
            ("Medaglia d'Oro", "Massimo Zanetti Beverage USA", 1920, "New York", "USA", "medagliadoro.com",
             "", "premium", "Italian espresso style",
             "Italian-American espresso brand, New York heritage"),
            
            ("Death Wish Coffee", "Independent", 2012, "Round Lake", "USA", "deathwishcoffee.com",
             "USDA Organic, Fairtrade", "specialty", "Dark roast",
             "World's strongest coffee claim, high caffeine, online-focused brand"),
        ]
        
        self.cursor.executemany('''
            INSERT INTO roasters (roaster_name, parent_company, founded_year, headquarters_city,
                                country_of_origin, website, certifications, market_segment,
                                roasting_style, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', roasters_data)
        
        self.conn.commit()
        print(f"✓ Inserted {len(roasters_data)} coffee roasters/brands")
    
    def populate_products(self):
        """Populate coffee products"""
        products_data = [
            # Starbucks products (roaster_id=1)
            (1, "Pike Place Roast", "blend", "medium", "Whole Bean", 12, 340, 11.95, "USD", "USA, Canada, Global", 0, 0, 0, "Signature blend, smooth and balanced"),
            (1, "Espresso Roast", "espresso", "dark", "Whole Bean", 12, 340, 11.95, "USD", "USA, Canada, Global", 0, 0, 0, "Rich and caramelly"),
            (1, "French Roast", "blend", "dark", "Whole Bean", 12, 340, 11.95, "USD", "USA, Canada, Global", 0, 0, 0, "Intense and smoky"),
            (1, "Veranda Blend", "blend", "light", "Whole Bean", 12, 340, 11.95, "USD", "USA, Canada, Global", 0, 0, 0, "Mellow and soft"),
            (1, "Kenya", "single-origin", "medium", "Whole Bean", 9, 255, 13.95, "USD", "USA, Canada, Global", 0, 0, 1, "Juicy and complex"),
            (1, "Colombia", "single-origin", "medium", "Whole Bean", 12, 340, 13.95, "USD", "USA, Canada, Global", 0, 0, 1, "Balanced and nutty"),
            (1, "VIA Instant Pike Place", "instant", "medium", "Instant packets", 0.11, 3.1, 9.95, "USD", "Global", 0, 0, 0, "8-count box"),
            (1, "Cold Brew Concentrate", "cold-brew", "medium", "Liquid", 32, 946, 12.95, "USD", "USA, Canada", 0, 0, 0, "RTD concentrate"),
            
            # Dunkin' products (roaster_id=2)
            (2, "Original Blend", "blend", "medium", "Ground", 12, 340, 8.99, "USD", "USA, Canada", 0, 0, 0, "America runs on it"),
            (2, "Original Blend", "blend", "medium", "Whole Bean", 12, 340, 9.99, "USD", "USA, Canada", 0, 0, 0, "America runs on it"),
            (2, "Dark Roast", "blend", "dark", "Ground", 12, 340, 8.99, "USD", "USA, Canada", 0, 0, 0, "Bold and smooth"),
            (2, "Decaf", "decaf", "medium", "Ground", 12, 340, 9.49, "USD", "USA, Canada", 0, 0, 0, "Decaffeinated"),
            
            # Peet's Coffee products (roaster_id=3)
            (3, "Major Dickason's Blend", "blend", "dark", "Whole Bean", 12, 340, 12.95, "USD", "USA", 0, 0, 0, "Peet's most iconic blend"),
            (3, "Big Bang", "blend", "medium", "Whole Bean", 12, 340, 12.95, "USD", "USA", 0, 0, 0, "Lively and complex"),
            (3, "Ethiopia Supernatural", "single-origin", "medium-light", "Whole Bean", 12, 340, 16.95, "USD", "USA", 0, 0, 1, "Blueberry notes"),
            (3, "French Roast", "blend", "dark", "Whole Bean", 12, 340, 11.95, "USD", "USA", 0, 0, 0, "Vigorous and smoky"),
            (3, "Decaf Major Dickason's", "decaf", "dark", "Whole Bean", 12, 340, 13.95, "USD", "USA", 0, 0, 0, "Decaf version"),
            
            # Lavazza products (roaster_id=4)
            (4, "Super Crema", "espresso", "medium", "Whole Bean", 2.2, 1000, 25.99, "USD", "Global", 0, 0, 0, "Creamy espresso blend"),
            (4, "Qualità Rossa", "blend", "medium-dark", "Ground", 8.8, 250, 8.99, "EUR", "Europe, Global", 0, 0, 0, "Classic Italian blend"),
            (4, "Qualità Oro", "blend", "medium", "Whole Bean", 8.8, 250, 9.99, "EUR", "Europe, Global", 0, 0, 0, "100% Arabica"),
            (4, "Tierra", "blend", "medium", "Whole Bean", 2.2, 1000, 28.99, "USD", "Global", 1, 1, 0, "Organic, Rainforest Alliance"),
            (4, "Espresso Italiano", "espresso", "dark", "Ground", 8.8, 250, 8.49, "EUR", "Europe, Global", 0, 0, 0, "Traditional Italian"),
            
            # illy products (roaster_id=5)
            (5, "Classico Medium Roast", "blend", "medium", "Whole Bean", 8.8, 250, 13.99, "USD", "Global", 0, 0, 0, "Signature blend"),
            (5, "Intenso Dark Roast", "espresso", "dark", "Whole Bean", 8.8, 250, 13.99, "USD", "Global", 0, 0, 0, "Bold espresso"),
            (5, "Decaffeinated", "decaf", "medium", "Whole Bean", 8.8, 250, 14.99, "USD", "Global", 0, 0, 0, "Swiss water process"),
            (5, "Ethiopia Single Origin", "single-origin", "medium", "Whole Bean", 8.8, 250, 16.99, "USD", "Global", 0, 0, 1, "Floral and fruity"),
            (5, "Guatemala Single Origin", "single-origin", "medium", "Whole Bean", 8.8, 250, 16.99, "USD", "Global", 0, 0, 1, "Chocolate notes"),
            
            # Blue Bottle products (roaster_id=8)
            (8, "Three Africas", "blend", "light", "Whole Bean", 12, 340, 16.00, "USD", "USA, Japan", 0, 0, 0, "Bright and fruity blend"),
            (8, "Bella Donovan", "espresso", "medium", "Whole Bean", 12, 340, 16.00, "USD", "USA, Japan", 0, 0, 0, "Espresso blend"),
            (8, "Giant Steps", "blend", "medium", "Whole Bean", 12, 340, 16.00, "USD", "USA, Japan", 1, 0, 0, "Organic blend"),
            (8, "Ethiopia Yirgacheffe", "single-origin", "light", "Whole Bean", 6, 170, 17.00, "USD", "USA, Japan", 0, 0, 1, "Seasonal single-origin"),
            (8, "Hayes Valley Espresso", "espresso", "medium", "Whole Bean", 12, 340, 17.00, "USD", "USA, Japan", 0, 0, 0, "SF cafe blend"),
            
            # Intelligentsia products (roaster_id=9)
            (9, "Black Cat Classic Espresso", "espresso", "medium", "Whole Bean", 12, 340, 17.00, "USD", "USA", 0, 0, 0, "Signature espresso"),
            (9, "House Blend", "blend", "medium", "Whole Bean", 12, 340, 16.00, "USD", "USA", 0, 0, 0, "Balanced and sweet"),
            (9, "Frequency Blend", "espresso", "medium-dark", "Whole Bean", 12, 340, 16.00, "USD", "USA", 1, 0, 0, "Organic espresso"),
            (9, "Ethiopia Yirgacheffe", "single-origin", "light", "Whole Bean", 12, 340, 19.00, "USD", "USA", 0, 0, 1, "Direct Trade"),
            (9, "Colombia La Palma", "single-origin", "light", "Whole Bean", 12, 340, 18.00, "USD", "USA", 0, 0, 1, "Direct Trade"),
            
            # Counter Culture products (roaster_id=10)
            (10, "Hologram", "espresso", "medium", "Whole Bean", 12, 340, 16.50, "USD", "USA", 0, 0, 0, "Balanced espresso"),
            (10, "Big Trouble", "blend", "medium", "Whole Bean", 12, 340, 15.50, "USD", "USA", 1, 0, 0, "Organic, everyday"),
            (10, "Forty-Six", "blend", "medium", "Whole Bean", 12, 340, 15.50, "USD", "USA", 0, 0, 0, "Approachable blend"),
            (10, "Ethiopia Sidama", "single-origin", "light", "Whole Bean", 12, 340, 18.50, "USD", "USA", 0, 0, 1, "Single-origin"),
            (10, "Apollo", "espresso", "medium", "Whole Bean", 12, 340, 16.50, "USD", "USA", 0, 0, 0, "Milk chocolate espresso"),
            
            # Stumptown products (roaster_id=11)
            (11, "Hair Bender", "espresso", "medium", "Whole Bean", 12, 340, 16.00, "USD", "USA", 0, 0, 0, "Signature espresso blend"),
            (11, "Holler Mountain", "blend", "medium", "Whole Bean", 12, 340, 15.00, "USD", "USA", 1, 0, 0, "Organic, everyday"),
            (11, "Founders Blend", "blend", "medium-dark", "Whole Bean", 12, 340, 15.00, "USD", "USA", 0, 0, 0, "Bold and balanced"),
            (11, "Colombia Huila", "single-origin", "light", "Whole Bean", 12, 340, 17.00, "USD", "USA", 0, 0, 1, "Single-origin"),
            (11, "Cold Brew", "cold-brew", "medium", "RTD Can", 10.5, 311, 3.50, "USD", "USA", 0, 0, 0, "Ready to drink"),
            
            # Lavazza products continued
            (4, "¡Tierra! Organic", "blend", "medium", "Whole Bean", 2.2, 1000, 27.99, "USD", "Global", 1, 1, 0, "100% Arabica organic"),
            
            # Additional specialty products
            (12, "The Everyday", "blend", "medium", "Whole Bean", 12, 340, 17.00, "USD", "USA", 0, 0, 0, "Approachable blend"),
            (12, "Nizza", "espresso", "medium-dark", "Whole Bean", 12, 340, 17.00, "USD", "USA", 0, 0, 0, "Italian-inspired espresso"),
            
            # International specialty
            (14, "Kenya Kamwangi AA", "single-origin", "light", "Whole Bean", 8.8, 250, 18.00, "GBP", "UK, Europe", 0, 0, 1, "Direct Trade Kenya"),
            (14, "Red Brick Seasonal Espresso", "espresso", "medium", "Whole Bean", 12, 340, 16.00, "GBP", "UK, Europe", 0, 0, 0, "Rotating blend"),
            
            # Budget brands
            (22, "Original Ground", "blend", "medium", "Ground", 11.5, 326, 6.99, "USD", "USA", 0, 0, 0, "Classic American coffee"),
            (22, "Original Ground", "blend", "medium", "Ground", 30.5, 865, 14.99, "USD", "USA", 0, 0, 0, "Large canister"),
            
            (23, "Original Roast", "blend", "medium", "Ground", 11.5, 326, 6.49, "USD", "USA", 0, 0, 0, "Good to the Last Drop"),
            (23, "Original Roast", "blend", "medium", "Ground", 30.5, 865, 13.99, "USD", "USA", 0, 0, 0, "Large size"),
            
            # Café Bustelo
            (26, "Supreme Espresso", "espresso", "dark", "Ground", 10, 283, 5.99, "USD", "USA, Latin America", 0, 0, 0, "Cuban-style espresso"),
            (26, "Supreme Espresso", "espresso", "dark", "Ground", 36, 1020, 16.99, "USD", "USA, Latin America", 0, 0, 0, "Large brick"),
            
            # Death Wish
            (28, "Death Wish Ground", "blend", "dark", "Ground", 16, 454, 19.99, "USD", "USA, Online", 1, 1, 0, "World's strongest coffee"),
            (28, "Death Wish Whole Bean", "blend", "dark", "Whole Bean", 16, 454, 19.99, "USD", "USA, Online", 1, 1, 0, "Whole bean version"),
            (28, "Valhalla Java", "blend", "medium-dark", "Whole Bean", 12, 340, 19.99, "USD", "USA, Online", 1, 1, 0, "Smooth and strong"),
        ]
        
        self.cursor.executemany('''
            INSERT INTO products (roaster_id, product_name, coffee_type, roast_level, format,
                                weight_oz, weight_g, price, price_currency, countries_available,
                                organic, fair_trade, single_origin, special_features)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', products_data)
        
        self.conn.commit()
        print(f"✓ Inserted {len(products_data)} coffee products")
    
    def initialize_database(self, force_rebuild=False):
        """Create and populate the entire database"""
        self.connect()
        
        if force_rebuild:
            print("Rebuilding database from scratch...")
            self.drop_tables()
        
        self.create_tables()
        
        # Check if already populated
        self.cursor.execute("SELECT COUNT(*) FROM coffees")
        coffee_count = self.cursor.fetchone()[0]
        
        if coffee_count == 0 or force_rebuild:
            print("Populating database with coffee data...")
            self.populate_coffees()
            self.populate_varieties()
            self.populate_regions()
            self.populate_brewing_methods()
            self.populate_roasters()
            self.populate_products()
            print("\n✓ Database initialization complete!")
            print(f"  Total coffees: {len([1 for _ in self.cursor.execute('SELECT * FROM coffees')])} origins")
            print(f"  Total varieties: {len([1 for _ in self.cursor.execute('SELECT * FROM varieties')])} varieties")
            print(f"  Total regions: {len([1 for _ in self.cursor.execute('SELECT * FROM regions')])} regions")
            print(f"  Total brewing methods: {len([1 for _ in self.cursor.execute('SELECT * FROM brewing_methods')])} methods")
            print(f"  Total roasters: {len([1 for _ in self.cursor.execute('SELECT * FROM roasters')])} roasters")
            print(f"  Total products: {len([1 for _ in self.cursor.execute('SELECT * FROM products')])} products")
        else:
            print(f"Database already contains {coffee_count} coffees")
            print("Use force_rebuild=True to recreate database")
        
        self.close()

def main():
    """Initialize the coffee database"""
    import sys
    force = '--force' in sys.argv or '-f' in sys.argv
    
    db = CoffeeDatabase()
    db.initialize_database(force_rebuild=force)
    
    if not force:
        print("\nTo force rebuild database, run: python coffee_database.py --force")

if __name__ == "__main__":
    main()
