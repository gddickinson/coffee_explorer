# Coffee Collection Explorer

A Python-based GUI application for exploring coffee varieties, brewing methods, roasters/brands, and coffee-growing regions around the world.

## Features

### 1. **Coffee Database Browser**
- Browse 29 meticulously documented coffee origins
- Search by name, country, flavor profile, or region
- Filter by roast level (Light, Medium, Dark)
- View detailed information including:
  - Origin (country and specific region)
  - Coffee variety and processing methods
  - Flavor profiles, aroma, body, and acidity
  - Growing altitude and harvest seasons
  - Cupping scores (specialty grade 80-95+)
  - Detailed tasting notes
  - Historical context
  - Price ranges

### 2. **Coffee Varieties/Cultivars**
- Explore 20 coffee varieties and cultivars
- Learn about Arabica varieties (Typica, Bourbon, Geisha, etc.)
- Understand Robusta characteristics
- Discover modern hybrids (Catimor, Castillo, etc.)
- View:
  - Origin and discovery year
  - Plant characteristics and flavor notes
  - Disease resistance profiles
  - Yield characteristics
  - Historical significance

### 3. **Coffee Roasters & Brands** 
- Browse 28 global coffee roasters and brands
- Search by company name, country, or market segment
- Filter by:
  - Country of origin (USA, Italy, UK, Japan, Australia, etc.)
  - Market segment (mass-market, premium, specialty, luxury)
  - Certifications (Organic, Fair Trade, Direct Trade, etc.)
- View detailed company information:
  - Company history and founding year
  - Parent company and ownership
  - Headquarters location
  - Roasting style and philosophy
  - Certifications
- Browse 61+ coffee products with details on:
  - Coffee type (single-origin, blend, espresso, etc.)
  - Roast level (light, medium, dark, espresso)
  - Weight and pricing in multiple currencies
  - Countries where available
  - Organic, Fair Trade, and Single Origin status

### 4. **Brewing Methods**
- Learn 12 professional brewing methods:
  - Espresso, Pour Over (V60), Chemex
  - French Press, AeroPress, Moka Pot
  - Cold Brew, Siphon, Turkish/Ibrik
  - Drip Coffee Maker, Clever Dripper, Vietnamese Phin
- For each method, view:
  - Grind size requirements
  - Water temperature (°C and °F)
  - Brew time
  - Coffee-to-water ratios
  - Required equipment
  - Difficulty level
  - Resulting flavor characteristics
  - Detailed brewing instructions

### 5. **Brewing Timer**
- Built-in timer for precise brewing
- Customizable minutes and seconds
- Audio alert when brewing is complete
- Linked to brewing method details

### 6. **Tasting Journal**
- Record your coffee tasting experiences
- 5-star rating system
- Document brewing parameters
- Save detailed tasting notes
- Export journal to JSON
- Track your coffee journey over time

### 7. **Complete Coffee Guide** (NEW!)
- Comprehensive guide to coffee species, varieties, and processing
- Detailed brewing guides for all methods
- Coffee cupping and tasting protocols
- Flavor wheel and sensory analysis
- Storage tips and best practices
- Health information and caffeine content
- Sustainable and ethical coffee certifications
- Coffee terminology and glossary
- Myths and facts about coffee

### 8. **Coffee History** (NEW!)
- Complete history from Ethiopian origins to modern day
- Ancient legends and early cultivation
- Spread through Islamic world and Europe
- Colonial expansion and plantation systems
- Coffee house culture worldwide
- Three waves of coffee (mass market, café culture, specialty)
- Modern innovations and fourth wave
- Regional coffee cultures (Italian, Scandinavian, Turkish, Ethiopian, Vietnamese, etc.)
- Coffee economics and global trade
- Climate change impacts and industry response
- The future of coffee

### 9. **Interactive World Map**
- Visual representation of 15 major coffee-growing regions
- Enhanced markers with shadows for visibility
- Professional map styling with title and legend
- Regions spanning:
  - Africa (Ethiopia, Kenya, Tanzania, Rwanda, Burundi)
  - Central/South America (Colombia, Guatemala, Costa Rica, Brazil, Peru, Nicaragua)
  - Asia (Indonesia, Yemen, Papua New Guinea)
  - Caribbean (Jamaica)
  - North America (Hawaii)
- Clickable markers for detailed region information:
  - Geographic coordinates and elevation ranges
  - Climate and soil types
  - Famous coffees from each region
  - Regional descriptions

## Installation & Requirements

### Requirements
- Python 3.7 or higher
- Required packages:
  - tkinter (usually included with Python)
  - sqlite3 (usually included with Python)
  - Pillow (PIL)

### Installation

1. **Ensure Python packages are installed:**
   ```bash
   pip install Pillow
   ```

2. **Files included:**
   - `coffee_database.py` - Database creation and management
   - `coffee_explorer.py` - Main GUI application
   - `coffee_collection.db` - SQLite database (auto-created)
   - `run_coffee_explorer.py` - Application launcher
   - `coffee_journal.json` - Tasting journal data
   - `coffee_guide.md` - Complete coffee guide (species, brewing, cupping, etc.)
   - `coffee_history.md` - Comprehensive coffee history
   - `README.md` - This file

## Running the Application

### Option 1: Using the launcher (recommended)
```bash
python3 run_coffee_explorer.py
```

### Option 2: Direct execution
```bash
python3 coffee_explorer.py
```

The application will:
1. Initialize the database if needed
2. Load all coffee data
3. Open the GUI with 8 tabs

## Using the Application

### Coffee Database Tab
1. **Browse** all coffee origins in the left panel
2. **Search** using the search box at the top
3. **Filter** by roast level using the dropdown
4. **Click** on any coffee to see detailed information
5. **Clear** search to reset filters

### Coffee Varieties Tab
1. **Browse** 20 coffee varieties/cultivars
2. **Click** on any variety to learn about:
   - Plant characteristics and origin
   - Flavor profiles
   - Disease resistance
   - Yield characteristics
   - Historical significance

### Coffee Roasters Tab
1. **Browse** 28 coffee roasters worldwide
2. **Search** by company name
3. **Filter** by:
   - Country of origin
   - Market segment (mass-market, premium, specialty, luxury)
4. **Click** on any roaster to see:
   - Company details and history
   - Complete product catalog (61+ products)
5. **Click** on any product for detailed pricing and availability

### Brewing Methods Tab
1. **Browse** 12 professional brewing methods
2. **Click** on any method to see:
   - Detailed brewing parameters
   - Equipment requirements
   - Difficulty level
   - Flavor characteristics
3. **Use the built-in timer**:
   - Set minutes and seconds
   - Click "Start" to begin countdown
   - Get an alert when brewing is complete

### Tasting Journal Tab
1. **Click "New Entry"** to record a tasting
2. **Select coffee** from dropdown (or type custom name)
3. **Rate** with 1-5 stars
4. **Document** brewing details and tasting notes
5. **View** past entries in chronological order
6. **Export** journal to JSON file

### Coffee Guide Tab (NEW!)
- **Comprehensive reference** covering all aspects of coffee
- **Coffee species** - Arabica, Robusta, Liberica characteristics
- **Major coffee regions** - Detailed profiles of producing countries
- **Processing methods** - Natural, washed, honey, wet-hulled, experimental
- **Roast levels** - Light to dark roast characteristics
- **Brewing methods** - Detailed guides for 12+ methods
- **Cupping & tasting** - SCA protocols, flavor wheel, scoring
- **Storage tips** - Optimal storage for whole beans and ground coffee
- **Health information** - Benefits, caffeine content, considerations
- **Sustainability** - Fair Trade, Direct Trade, Organic, Rainforest Alliance
- **Terminology** - Complete coffee glossary
- **Myths & facts** - Common misconceptions debunked
- **Reload button** - Refresh content from markdown file

### Coffee History Tab (NEW!)
- **Ancient origins** - Ethiopian legends and early cultivation
- **Spread to Islamic world** - Ottoman coffee houses, religious debates
- **European arrival** - Coffee houses, Pope's coffee, social movements
- **Colonial expansion** - Dutch, French, and Portuguese coffee empires
- **Brazil's rise** - Becoming the coffee superpower
- **American revolution** - Coffee as patriotic drink
- **First wave** - Mass market and industrialization
- **Second wave** - Starbucks and café culture
- **Third wave** - Specialty coffee movement, Direct Trade
- **Fourth wave** - Science, sustainability, exotic varieties
- **Geisha phenomenon** - Record auction prices
- **Regional cultures** - Italian, Scandinavian, Turkish, Ethiopian, Vietnamese, etc.
- **Climate change** - Threats and industry response
- **The future** - Innovations and sustainability
- **Reload button** - Refresh content from markdown file

### Coffee Regions Map Tab
- **Enhanced world map** with professional styling
- **Title and legend** for easy navigation
- **Shadowed markers** for better visibility
- **Hover** over markers to see region names
- **Click** markers to open detailed information window
- View coordinates, elevation, climate, soil, and famous coffees
- Explore 15 major coffee-growing regions worldwide
- **GeoPandas-powered** map creation for accurate geography

## Database Structure

### Coffees Table
Detailed information about coffee origins:
- Name, country, region
- Variety and processing method
- Roast level recommendations
- Flavor profile, aroma, body, acidity
- Growing altitude and harvest seasons
- Caffeine content
- Cupping scores
- Tasting notes and history
- Price ranges

### Varieties Table
Coffee plant varieties and cultivars:
- Variety name and species
- Origin country and discovery year
- Plant characteristics
- Flavor notes
- Disease resistance
- Yield characteristics
- Additional notes

### Regions Table
Geographic and climate data for coffee-growing regions:
- Location coordinates
- Elevation ranges
- Climate descriptions
- Soil types
- Famous coffees from each region
- Regional descriptions

### Brewing Methods Table
Professional brewing techniques:
- Method name and category
- Grind size requirements
- Water temperature
- Brew time
- Coffee-to-water ratios
- Equipment needed
- Difficulty levels
- Flavor characteristics
- Detailed descriptions

### Roasters Table
Coffee roasters and brands worldwide:
- Company name and parent company
- Founded year and headquarters
- Country of origin
- Website and certifications
- Market segment (mass-market, premium, specialty, luxury)
- Roasting style
- Company description

### Products Table
Complete product catalog for each roaster:
- Product name and roaster
- Coffee type (single-origin, blend, espresso, etc.)
- Roast level
- Format and weight (oz and grams)
- Price and currency
- Countries available
- Organic, Fair Trade, and Single Origin status
- Special features

## Customization

### Adding New Coffees
Edit `coffee_database.py` and add entries to the `coffees_data` list in the `populate_coffees()` method.

### Adding New Varieties
Edit `coffee_database.py` and add entries to the `varieties_data` list in the `populate_varieties()` method.

### Adding New Regions
Edit `coffee_database.py` and add entries to the `regions_data` list in the `populate_regions()` method.

### Adding New Brewing Methods
Edit `coffee_database.py` and add entries to the `brewing_data` list in the `populate_brewing_methods()` method.

### Adding New Roasters
Edit `coffee_database.py` and add entries to the `roasters_data` list in the `populate_roasters()` method.

### Adding New Products
Edit `coffee_database.py` and add entries to the `products_data` list in the `populate_products()` method.

## Coffee Categories in Database

**By Origin Region:**
- **Africa**: Ethiopia, Kenya, Rwanda, Burundi, Tanzania (15 varieties)
- **Central America**: Guatemala, Costa Rica, Nicaragua, El Salvador, Honduras, Panama (9 varieties)
- **South America**: Colombia, Brazil, Peru (4 varieties)
- **Caribbean**: Jamaica (1 variety)
- **Asia**: Indonesia, Yemen, India (4 varieties)
- **North America**: Hawaii/Kona (1 variety)
- **Pacific**: Papua New Guinea (implicit)

**By Processing Method:**
- Washed/Wet Processed
- Natural/Dry Processed
- Honey Processed
- Pulped Natural
- Wet-Hulled (Giling Basah)
- Monsooned

**By Roast Level:**
- Light Roast
- Medium-Light Roast
- Medium Roast
- Medium-Dark Roast
- Dark Roast
- Espresso Roast

## Roaster Categories

**Mass-Market Brands**: Starbucks, Dunkin', Nescafé, Folgers, Maxwell House, Eight O'Clock, Café Bustelo

**Premium Brands**: Peet's Coffee, Lavazza, illy, Intelligentsia (owned by Peet's), Stumptown (owned by Peet's), Medaglia d'Oro, Campos, Allpress, Five Senses

**Specialty Roasters**: Blue Bottle (Nestlé), Counter Culture, La Colombe, Verve, Square Mile, Has Bean, Tim Wendelboe, Koppi, Coffee Collective, Onibus

**International**: Italian (Lavazza, illy), Japanese (Onibus), Norwegian (Tim Wendelboe), UK (Square Mile, Has Bean), Danish (Coffee Collective), Swedish (Koppi), Australian (Campos, Five Senses, Allpress)

## Keyboard Shortcuts

- **Tab Navigation**: Use mouse or keyboard to navigate between tabs
- **Search Boxes**: Start typing to search immediately
- **Clear Buttons**: Reset all filters with one click

## Troubleshooting

### Database Issues
If you encounter database errors:
```bash
rm coffee_collection.db
python3 coffee_database.py --force
```

### Display Issues
- Ensure your screen resolution is at least 1200x800
- The application is resizable - adjust window size as needed
- Map regions scale automatically with window size

### Dependencies
If you encounter import errors:
```bash
pip install Pillow
```

Tkinter usually comes with Python. If missing:
- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **macOS**: Included with Python installation
- **Windows**: Included with Python installation

## Technical Details

### Database: SQLite3
- Lightweight, file-based database
- No server required
- Fast queries for coffee varieties, roasters, and regions

### GUI Framework: Tkinter
- Cross-platform (Windows, Mac, Linux)
- Native look and feel
- Included with Python

### Image Processing: Pillow (PIL)
- Generates interactive world map
- Handles image scaling and display
- Creates clickable regions

## Geographic Regions Covered

- **Ethiopia**: Sidamo/Gedeo, Yirgacheffe, Harrar
- **Kenya**: Central Highlands
- **Colombia**: Huila, Nariño, Various regions
- **Guatemala**: Antigua Valley, Huehuetenango
- **Costa Rica**: Tarrazú
- **Brazil**: Minas Gerais, São Paulo
- **Jamaica**: Blue Mountain
- **Hawaii**: Kona District
- **Indonesia**: Sumatra, Java, Sulawesi
- **Yemen**: Haraz Mountains
- **Panama**: Boquete
- **Tanzania**: Kilimanjaro/Arusha
- **Nicaragua**: Jinotega/Matagalpa
- **Mexico**: Chiapas
- **Papua New Guinea**: Western Highlands

## Future Enhancements

Potential improvements for future versions:
- Export coffee database to CSV/Excel
- Print coffee information
- More detailed roasting profiles
- Cupping form templates
- Coffee pairing suggestions
- Advanced comparison tool
- Photos of coffee varieties and regions
- Vendor price comparisons
- Subscription tracking
- Coffee freshness calculator
- Home roasting guides

## Credits

**Database Content**: Compiled from extensive research including:
- Specialty Coffee Association standards
- World coffee competition results
- Coffee quality grading systems
- Roaster websites and product catalogs
- Coffee research publications
- Industry trade publications

**Application Development**: Built with Python, Tkinter, SQLite, and Pillow

## License

This application is provided for educational and personal use.

Coffee data compiled from public domain sources and general knowledge.
Product and company information synthesized from publicly available sources.

---

**Version**: 1.0
**Last Updated**: January 2026

Enjoy exploring the wonderful world of coffee! ☕


---
*Built with AI assistance from [Claude (Anthropic)](https://claude.com/).*
