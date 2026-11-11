"""
Coffee Explorer - Interactive world map tab.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
from pathlib import Path
from PIL import Image, ImageTk, ImageDraw

from world_shapes import CONTINENT_POLYGONS


class MapTabMixin:
    """Mixin providing the Coffee Regions world-map tab."""

    def create_map_tab(self):
        map_frame = ttk.Frame(self.notebook)
        self.notebook.add(map_frame, text="Coffee Regions")

        ttk.Label(map_frame, text="Coffee Growing Regions Around the World",
                  style='Title.TLabel').pack(pady=10)

        canvas_frame = ttk.Frame(map_frame)
        canvas_frame.pack(fill='both', expand=True, padx=10, pady=10)

        self.map_canvas = tk.Canvas(canvas_frame, bg='#d4e8f7')
        self.map_canvas.pack(fill='both', expand=True)

        self.map_regions = []

        self.create_world_map()

        self.map_canvas.bind('<Button-1>', self.on_map_click)
        self.map_canvas.bind('<Motion>', self.on_map_hover)

    # ── Map image creation ───────────────────────────────────────────

    def get_world_map_image(self, width, height):
        cache_dir = Path.home() / '.coffee_explorer'
        cache_dir.mkdir(exist_ok=True)
        map_file = cache_dir / 'world_map.png'

        if map_file.exists():
            try:
                img = Image.open(map_file)
                if img.size == (width, height):
                    return img
            except (IOError, OSError, Image.DecompressionBombError):
                pass

        print("Attempting to create world map...")
        return self._create_geopandas_world_map(width, height, map_file)

    def _create_geopandas_world_map(self, width, height, save_path):
        """Create a world map using GeoPandas with manual continent polygons."""
        try:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            import geopandas as gpd
            from shapely.geometry import Polygon

            continents_data = self._continent_polygons()

            geometries = []
            names = []
            for name, coords in continents_data.items():
                geometries.append(Polygon(coords))
                names.append(name)

            world = gpd.GeoDataFrame({'name': names, 'geometry': geometries})

            dpi = 100
            fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
            world.plot(ax=ax, color='#c8b896', edgecolor='#8b7355',
                       linewidth=0.8, alpha=0.92)
            ax.set_facecolor('#d4e8f7')
            fig.patch.set_facecolor('#d4e8f7')
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_visible(False)
            ax.set_xlim(-180, 180)
            ax.set_ylim(-90, 90)
            plt.tight_layout(pad=0)
            plt.savefig(save_path, dpi=dpi, bbox_inches='tight', pad_inches=0,
                        facecolor='#d4e8f7')
            plt.close(fig)

            img = Image.open(save_path)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            img.save(save_path)
            return img

        except Exception as e:
            print(f"Error creating GeoPandas map: {e}")
            return self._create_custom_world_map(width, height)

    @staticmethod
    def _continent_polygons():
        return CONTINENT_POLYGONS

    def _create_custom_world_map(self, width, height):
        """Fallback: draw a simple world map with PIL."""
        img = Image.new('RGB', (width, height), color='#d4e8f7')
        draw = ImageDraw.Draw(img)

        shapes = {
            'Africa': [
                (0.47, 0.33), (0.54, 0.32), (0.56, 0.38), (0.57, 0.50),
                (0.55, 0.65), (0.52, 0.70), (0.48, 0.72), (0.45, 0.68),
                (0.44, 0.58), (0.43, 0.48), (0.45, 0.38), (0.47, 0.33),
            ],
            'South America': [
                (0.24, 0.48), (0.30, 0.47), (0.32, 0.52), (0.31, 0.62),
                (0.28, 0.72), (0.25, 0.75), (0.22, 0.72), (0.21, 0.62),
                (0.22, 0.52), (0.24, 0.48),
            ],
            'Asia': [
                (0.55, 0.15), (0.85, 0.15), (0.90, 0.25), (0.87, 0.35),
                (0.82, 0.42), (0.77, 0.45), (0.70, 0.45), (0.65, 0.48),
                (0.60, 0.52), (0.55, 0.50), (0.52, 0.45), (0.50, 0.35),
                (0.52, 0.25), (0.55, 0.15),
            ],
            'North America': [
                (0.15, 0.20), (0.28, 0.18), (0.32, 0.25), (0.30, 0.35),
                (0.25, 0.42), (0.20, 0.45), (0.15, 0.42), (0.12, 0.35),
                (0.13, 0.25), (0.15, 0.20),
            ],
            'Australia': [
                (0.72, 0.60), (0.82, 0.58), (0.85, 0.62), (0.84, 0.68),
                (0.80, 0.72), (0.75, 0.73), (0.71, 0.70), (0.70, 0.64),
                (0.72, 0.60),
            ],
        }

        for pts in shapes.values():
            draw.polygon([(width * x, height * y) for x, y in pts],
                         fill='#c8b896', outline='#8b7355', width=2)
        return img

    # ── Map rendering with markers ───────────────────────────────────

    def create_world_map(self):
        width, height = 1200, 600
        img = self.get_world_map_image(width, height)
        draw = ImageDraw.Draw(img)

        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM regions")
            regions = cursor.fetchall()

            for region in regions:
                x = int((region['longitude'] + 180) * (width / 360))
                y = int((90 - region['latitude']) * (height / 180))
                marker_size = 12

                # Shadow / glow
                for offset in range(4, 0, -1):
                    alpha = int(60 - offset * 10)
                    if img.mode != 'RGBA':
                        img = img.convert('RGBA')
                    shadow_layer = Image.new('RGBA', (width, height), (0, 0, 0, 0))
                    shadow_draw = ImageDraw.Draw(shadow_layer)
                    shadow_draw.ellipse([x - marker_size - offset, y - marker_size - offset,
                                         x + marker_size + offset, y + marker_size + offset],
                                        fill=(111, 78, 55, alpha))
                    img = Image.alpha_composite(img, shadow_layer)

                img = img.convert('RGB')
                draw = ImageDraw.Draw(img)

                draw.ellipse([x - marker_size - 2, y - marker_size - 2,
                              x + marker_size + 2, y + marker_size + 2],
                             fill='white', outline='white')
                draw.ellipse([x - marker_size, y - marker_size,
                              x + marker_size, y + marker_size],
                             fill='#6F4E37', outline='#3E2723', width=3)
                draw.ellipse([x - marker_size // 2, y - marker_size // 2,
                              x + marker_size // 2, y + marker_size // 2],
                             fill='#8B5A3C')

                self.map_regions.append({
                    'name': region['name'],
                    'country': region['country'],
                    'x': x, 'y': y,
                    'radius': marker_size + 4,
                    'data': dict(region),
                })

        except Exception as e:
            print(f"Error loading regions: {e}")

        # Title and legend
        self._add_map_title_and_legend(img, draw, width, height)

        self.map_image = ImageTk.PhotoImage(img)
        self.map_canvas.create_image(0, 0, anchor=tk.NW, image=self.map_image)
        self.map_canvas.config(scrollregion=self.map_canvas.bbox(tk.ALL))

    def _add_map_title_and_legend(self, img, draw, width, height):
        try:
            from PIL import ImageFont
            try:
                font = ImageFont.truetype(
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
                small_font = ImageFont.truetype(
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 14)
            except (IOError, OSError):
                try:
                    font = ImageFont.truetype(
                        "/System/Library/Fonts/Helvetica.ttc", 24)
                    small_font = ImageFont.truetype(
                        "/System/Library/Fonts/Helvetica.ttc", 14)
                except (IOError, OSError):
                    font = ImageFont.load_default()
                    small_font = ImageFont.load_default()
        except ImportError:
            return  # cannot render title without ImageFont

        title_text = "Major Coffee-Growing Regions of the World"
        title_bbox = draw.textbbox((0, 0), title_text, font=font)
        title_width = title_bbox[2] - title_bbox[0]
        title_height = title_bbox[3] - title_bbox[1]
        title_x = width // 2 - title_width // 2
        title_y = 15
        padding = 10

        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        bg = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        bg_draw = ImageDraw.Draw(bg)
        bg_draw.rectangle([title_x - padding, title_y - padding,
                           title_x + title_width + padding,
                           title_y + title_height + padding],
                          fill=(255, 255, 255, 220),
                          outline=(111, 78, 55, 255), width=3)
        img = Image.alpha_composite(img, bg)
        img = img.convert('RGB')
        draw = ImageDraw.Draw(img)
        draw.text((title_x, title_y), title_text, fill='#6F4E37', font=font)

        legend_x = 40
        legend_y = height - 60
        legend_text = " = Coffee-growing region (click for details)"
        l_bbox = draw.textbbox((0, 0), legend_text, font=small_font)
        l_w = l_bbox[2] - l_bbox[0]
        l_h = l_bbox[3] - l_bbox[1]

        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        lbg = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        lbg_draw = ImageDraw.Draw(lbg)
        lbg_draw.rectangle([legend_x - 10, legend_y - 5,
                            legend_x + 30 + l_w + 10, legend_y + l_h + 5],
                           fill=(255, 255, 255, 200))
        img = Image.alpha_composite(img, lbg)
        img = img.convert('RGB')
        draw = ImageDraw.Draw(img)

        mx = legend_x + 10
        my = legend_y + l_h // 2
        draw.ellipse([mx - 8, my - 8, mx + 8, my + 8],
                     fill='#6F4E37', outline='#3E2723', width=2)
        draw.text((mx + 15, legend_y), legend_text, fill='#3E2723', font=small_font)

    # ── Map events ───────────────────────────────────────────────────

    def on_map_click(self, event):
        for region in self.map_regions:
            dx = event.x - region['x']
            dy = event.y - region['y']
            if dx * dx + dy * dy <= region['radius'] ** 2:
                self._show_region_popup(region['data'])
                break

    def on_map_hover(self, event):
        for region in self.map_regions:
            dx = event.x - region['x']
            dy = event.y - region['y']
            if dx * dx + dy * dy <= region['radius'] ** 2:
                self.map_canvas.config(cursor="hand2")
                return
        self.map_canvas.config(cursor="")

    def _show_region_popup(self, data):
        popup = tk.Toplevel(self.root)
        popup.title(f"Coffee Region - {data['name']}")
        popup.geometry("500x400")
        popup.transient(self.root)

        dt = scrolledtext.ScrolledText(popup, wrap=tk.WORD, font=('Arial', 10))
        dt.pack(fill='both', expand=True, padx=10, pady=10)
        dt.tag_configure('title', font=('Arial', 14, 'bold'), foreground='#6F4E37')
        dt.tag_configure('header', font=('Arial', 11, 'bold'))
        dt.tag_configure('value', font=('Arial', 10))

        dt.insert(tk.END, f"{data['name']}\n", 'title')
        dt.insert(tk.END, f"{data['country']}\n\n", 'header')
        dt.insert(tk.END, "Location\n", 'header')
        dt.insert(tk.END,
            f"Coordinates: {data['latitude']}, {data['longitude']}\n", 'value')
        dt.insert(tk.END,
            f"Elevation: {data['elevation_min']}-{data['elevation_max']}m\n\n", 'value')
        dt.insert(tk.END, "Climate\n", 'header')
        dt.insert(tk.END, f"{data['climate']}\n\n", 'value')
        dt.insert(tk.END, "Soil Type\n", 'header')
        dt.insert(tk.END, f"{data['soil_type']}\n\n", 'value')
        dt.insert(tk.END, "Famous Coffees\n", 'header')
        dt.insert(tk.END, f"{data['famous_coffees']}\n\n", 'value')
        dt.insert(tk.END, "Description\n", 'header')
        dt.insert(tk.END, f"{data['description']}\n", 'value')
        dt.config(state='disabled')

        ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)
