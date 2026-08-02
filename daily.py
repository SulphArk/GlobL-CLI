#!/usr/bin/env python3
"""
daily.py — Adds 5+ real lines of code to your globe project every day.
            Builds your GitHub portfolio automatically.

Usage:
    python3 daily.py                    # Today's commit
    python3 daily.py --backfill 30      # Fill last 30 days
    python3 daily.py --backfill 60      # Fill last 60 days  
    python3 daily.py --stats            # Show stats
    python3 daily.py --force            # Force commit even if already done
"""

import json
import math
import os
import random
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Where your project lives
REPO_DIR = Path(__file__).resolve().parent
LOG_FILE = REPO_DIR / ".daily-log.json"
MAIN_FILE = REPO_DIR / "globe.py"

# ── Colors ──
G = "\033[0;32m"
Y = "\033[1;33m"
C = "\033[0;36m"
R = "\033[0;31m"
BOLD = "\033[1m"
NC = "\033[0m"

# ── Log ──
def load_log():
    if LOG_FILE.exists():
        return json.loads(LOG_FILE.read_text())
    return {"commits": [], "start_date": str(datetime.now().date())}

def save_log(data):
    LOG_FILE.write_text(json.dumps(data, indent=2))

def already_committed(date_str=None):
    if date_str is None:
        date_str = str(datetime.now().date())
    return any(c["date"] == date_str for c in load_log()["commits"])

# ── Git helpers ──
def git_commit(date_str, message):
    full_date = f"{date_str}T{random.randint(9,22):02d}:{random.randint(0,59):02d}:{random.randint(0,59):02d}"
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = full_date
    env["GIT_COMMITTER_DATE"] = full_date
    subprocess.run(["git", "add", "-A"], cwd=REPO_DIR, check=True)
    subprocess.run(["git", "commit", "-m", message], cwd=REPO_DIR, env=env, check=True, capture_output=True)

def git_push():
    r = subprocess.run(["git", "push", "origin", "main"], cwd=REPO_DIR, capture_output=True)
    if r.returncode != 0:
        r = subprocess.run(["git", "push", "origin", "master"], cwd=REPO_DIR, capture_output=True)
    return r.returncode == 0

# ── All the code snippets that get added to your project ──
# Each one is a REAL feature for your globe

SNIPPETS = [
    {
        "tag": "haversine-distance",
        "category": "feature",
        "code": '''
def haversine_distance(lon1, lat1, lon2, lat2):
    """Calculate great-circle distance in km between two points."""
    DEG_TO_RAD = math.pi / 180.0
    R = 6371.0
    dlat = (lat2 - lat1) * DEG_TO_RAD
    dlon = (lon2 - lon1) * DEG_TO_RAD
    a = (math.sin(dlat / 2) ** 2
         + math.cos(lat1 * DEG_TO_RAD) * math.cos(lat2 * DEG_TO_RAD)
         * math.sin(dlon / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c
''',
    },
    {
        "tag": "timezone-overlay",
        "category": "feature",
        "code": '''
def approximate_timezone(lon):
    """Rough UTC offset from longitude (ignores DST/political borders)."""
    return round(lon / 15.0)

TIMEZONE_LABELS = {
    -12: "UTC-12", -11: "UTC-11", -10: "HST", -9: "AKST",
    -8: "PST", -7: "MST", -6: "CST", -5: "EST",
    -4: "AST", -3: "BRT", -2: "UTC-2", -1: "UTC-1",
    0: "UTC", 1: "CET", 2: "EET", 3: "MSK",
    4: "GST", 5: "PKT", 5.5: "IST", 6: "BST",
    7: "ICT", 8: "CST", 9: "JST", 10: "AEST",
    11: "AEDT", 12: "NZST",
}
''',
    },
    {
        "tag": "more-countries",
        "category": "data",
        "code": '''
# Additional territories and small nations
EXTRA_PLACES = {
    "Fiji": (178.0, -17.8), "Samoa": (-172.0, -13.8),
    "Tonga": (-175.2, -21.2), "Maldives": (73.5, 3.2),
    "Bahrain": (50.6, 26.1), "Qatar": (51.2, 25.4),
    "Kuwait": (47.5, 29.4), "Oman": (55.9, 21.5),
    "Lebanon": (35.9, 33.9), "Georgia": (43.4, 42.3),
    "Armenia": (45.0, 40.1), "Azerbaijan": (47.6, 40.1),
}
''',
    },
    {
        "tag": "population-data",
        "category": "data",
        "code": '''
# Approximate populations (millions, 2023 est.)
POPULATIONS = {
    "China": 1425, "India": 1428, "USA": 340, "Indonesia": 277,
    "Pakistan": 240, "Nigeria": 223, "Brazil": 216, "Bangladesh": 172,
    "Russia": 144, "Mexico": 128, "Japan": 123, "Ethiopia": 126,
    "Philippines": 117, "Egypt": 112, "DR Congo": 102, "Vietnam": 99,
    "Iran": 88, "Turkey": 85, "Germany": 84, "Thailand": 72,
    "United Kingdom": 67, "France": 65, "Tanzania": 65, "Italy": 59,
    "South Africa": 60, "Myanmar": 55, "South Korea": 52, "Colombia": 52,
    "Kenya": 55, "Spain": 47, "Argentina": 46, "Algeria": 45,
    "Canada": 39, "Poland": 38, "Morocco": 37, "Saudi Arabia": 36,
    "Uzbekistan": 35, "Peru": 34, "Angola": 36, "Malaysia": 33,
    "Ghana": 34, "Mozambique": 33, "Nepal": 30, "Yemen": 30,
    "Venezuela": 29, "Australia": 26, "North Korea": 26, "Madagascar": 29,
}
''',
    },
    {
        "tag": "color-themes",
        "category": "feature",
        "code": '''
# Alternative color themes
THEMES = {
    "gruvbox": {
        "land_near": 142, "land_mid": 100, "land_far": 243,
        "ocean_near": 66, "ocean_far": 24, "limb": 237,
        "marker": 214, "highlight": 167, "text": 223,
        "header": 180, "dim": 246,
    },
    "nord": {
        "land_near": 150, "land_mid": 109, "land_far": 245,
        "ocean_near": 111, "ocean_far": 60, "limb": 59,
        "marker": 179, "highlight": 174, "text": 252,
        "header": 188, "dim": 246,
    },
    "dracula": {
        "land_near": 84, "land_mid": 71, "land_far": 246,
        "ocean_near": 117, "ocean_far": 61, "limb": 236,
        "marker": 215, "highlight": 198, "text": 252,
        "header": 189, "dim": 246,
    },
    "solarized": {
        "land_near": 106, "land_mid": 100, "land_far": 244,
        "ocean_near": 33, "ocean_far": 32, "limb": 236,
        "marker": 166, "highlight": 160, "text": 230,
        "header": 136, "dim": 246,
    },
}
''',
    },
    {
        "tag": "coord-formatter",
        "category": "feature",
        "code": '''
def format_coordinates(lon, lat):
    """Format lon/lat as DMS string like '51\\u00b030\\'N 0\\u00b007\\'W'."""
    def dms(val, pos_label, neg_label):
        direction = pos_label if val >= 0 else neg_label
        val = abs(val)
        degrees = int(val)
        minutes = int((val - degrees) * 60)
        seconds = int(((val - degrees) * 60 - minutes) * 60)
        return f"{degrees}\\u00b0{minutes}'{seconds}\\\"{direction}"
    lat_str = dms(lat, "N", "S")
    lon_str = dms(lon, "E", "W")
    return f"{lat_str} {lon_str}"
''',
    },
    {
        "tag": "bearing-calc",
        "category": "feature",
        "code": '''
def calculate_bearing(lon1, lat1, lon2, lat2):
    """Calculate initial bearing from point 1 to point 2 in degrees."""
    DEG_TO_RAD = math.pi / 180.0
    lat1_r, lat2_r = lat1 * DEG_TO_RAD, lat2 * DEG_TO_RAD
    dlon = (lon2 - lon1) * DEG_TO_RAD
    x = math.sin(dlon) * math.cos(lat2_r)
    y = (math.cos(lat1_r) * math.sin(lat2_r)
         - math.sin(lat1_r) * math.cos(lat2_r) * math.cos(dlon))
    bearing = math.atan2(x, y) / DEG_TO_RAD
    return (bearing + 360) % 360

BEARING_NAMES = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
                 "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

def bearing_to_compass(degrees):
    """Convert bearing degrees to compass direction name."""
    index = round(degrees / 22.5) % 16
    return BEARING_NAMES[index]
''',
    },
    {
        "tag": "antipode",
        "category": "feature",
        "code": '''
def find_antipode(lon, lat):
    """Find the point on the opposite side of the Earth."""
    anti_lon = -lon if lon <= 0 else 360 - lon
    anti_lat = -lat
    return (anti_lon, anti_lat)

def nearest_country_to(target_lon, target_lat, country_dict=None):
    """Find the nearest country to given coordinates."""
    if country_dict is None:
        country_dict = COUNTRIES
    best_name, best_dist = None, float("inf")
    for name, (lon, lat) in country_dict.items():
        d = haversine_distance(target_lon, target_lat, lon, lat)
        if d < best_dist:
            best_dist = d
            best_name = name
    return best_name, best_dist
''',
    },
    {
        "tag": "daylight-calc",
        "category": "feature",
        "code": '''
def approximate_daylight(lat, day_of_year):
    """Estimate daylight hours for a latitude and day of year."""
    DEG_TO_RAD = math.pi / 180.0
    lat_rad = lat * DEG_TO_RAD
    declination = 23.45 * math.sin(DEG_TO_RAD * (360 / 365) * (day_of_year - 81))
    dec_rad = declination * DEG_TO_RAD
    cos_hour = -math.tan(lat_rad) * math.tan(dec_rad)
    if cos_hour > 1:
        return 0.0   # Polar night
    if cos_hour < -1:
        return 24.0  # Midnight sun
    hour_angle = math.acos(cos_hour) / DEG_TO_RAD
    return 2 * hour_angle / 15.0
''',
    },
    {
        "tag": "grid-overlay",
        "category": "feature",
        "code": '''
def should_draw_grid_line(lon, lat, grid_spacing=30):
    """Determine if a point lies on a major grid line."""
    lat_mod = abs(lat) % grid_spacing
    lon_mod = abs(lon) % grid_spacing
    if lat_mod == 0 and lon_mod == 0:
        return "intersection"
    if lat_mod == 0:
        return "latitude"
    if lon_mod == 0:
        return "longitude"
    return None

NOTABLE_LATITUDES = {
    0: "Equator", 23.44: "Tropic of Cancer",
    -23.44: "Tropic of Capricorn",
    66.56: "Arctic Circle", -66.56: "Antarctic Circle",
}
''',
    },
    {
        "tag": "capitals",
        "category": "data",
        "code": '''
CAPITALS = {
    "USA": ("Washington DC", -77.0, 38.9),
    "United Kingdom": ("London", -0.1, 51.5),
    "France": ("Paris", 2.3, 48.9),
    "Germany": ("Berlin", 13.4, 52.5),
    "Japan": ("Tokyo", 139.7, 35.7),
    "China": ("Beijing", 116.4, 39.9),
    "India": ("New Delhi", 77.1, 28.6),
    "Brazil": ("Brasilia", -47.9, -15.8),
    "Russia": ("Moscow", 37.6, 55.8),
    "Australia": ("Canberra", 149.1, -35.3),
    "Canada": ("Ottawa", -75.7, 45.4),
    "South Korea": ("Seoul", 127.0, 37.6),
    "Mexico": ("Mexico City", -99.1, 19.4),
    "Egypt": ("Cairo", 31.2, 30.0),
    "South Africa": ("Pretoria", 28.2, -25.7),
    "Argentina": ("Buenos Aires", -58.4, -34.6),
    "Italy": ("Rome", 12.5, 41.9),
    "Spain": ("Madrid", -3.7, 40.4),
    "Turkey": ("Ankara", 32.9, 39.9),
    "Iran": ("Tehran", 51.4, 35.7),
}
''',
    },
    {
        "tag": "country-areas",
        "category": "data",
        "code": '''
COUNTRY_AREAS = {
    "Russia": 17098, "Canada": 9985, "USA": 9834, "China": 9597,
    "Brazil": 8516, "Australia": 7692, "India": 3287, "Argentina": 2780,
    "Kazakhstan": 2725, "Algeria": 2382, "DR Congo": 2345,
    "Saudi Arabia": 2150, "Mexico": 1964, "Indonesia": 1905,
    "Sudan": 1886, "Libya": 1760, "Iran": 1748, "Mongolia": 1567,
    "Peru": 1285, "Chad": 1284, "Niger": 1267, "Angola": 1247,
    "Mali": 1240, "South Africa": 1221, "Colombia": 1142,
    "Ethiopia": 1104, "Bolivia": 1098, "Mauritania": 1031,
    "Egypt": 1002, "Tanzania": 945, "Nigeria": 924,
    "Venezuela": 916, "Pakistan": 881, "Namibia": 825,
    "Mozambique": 802, "Turkey": 784, "Chile": 756,
}
''',
    },
    {
        "tag": "midpoint",
        "category": "feature",
        "code": '''
def geographic_midpoint(lon1, lat1, lon2, lat2):
    """Calculate the geographic midpoint between two coordinates."""
    DEG_TO_RAD = math.pi / 180.0
    lat1_r, lat2_r = lat1 * DEG_TO_RAD, lat2 * DEG_TO_RAD
    dlon = (lon2 - lon1) * DEG_TO_RAD
    x = math.cos(lat1_r) * math.cos(lat2_r) * math.cos(dlon)
    y = math.cos(lat1_r) * math.cos(lat2_r) * math.sin(dlon)
    z = math.sin(lat1_r) + math.sin(lat2_r)
    mid_lat = math.atan2(z, math.sqrt(x**2 + y**2)) / DEG_TO_RAD
    mid_lon = (lon1 * DEG_TO_RAD + math.atan2(y, x)) / DEG_TO_RAD
    return mid_lon, mid_lat
''',
    },
    {
        "tag": "country-search",
        "category": "feature",
        "code": '''
def search_countries(query, country_dict=None):
    """Search for countries by name with fuzzy matching."""
    if country_dict is None:
        country_dict = COUNTRIES
    query = query.lower().strip()
    exact, prefix, contains = [], [], []
    for name in country_dict:
        lower = name.lower()
        if lower == query:
            exact.append(name)
        elif lower.startswith(query):
            prefix.append(name)
        elif query in lower:
            contains.append(name)
    return exact + prefix + contains
''',
    },
    {
        "tag": "smooth-rotation",
        "category": "feature",
        "code": '''
def ease_in_out(t):
    """Smooth step interpolation (ease in-out)."""
    return t * t * (3 - 2 * t)

def lerp_angle(a, b, t):
    """Linearly interpolate between two angles with wrapping."""
    diff = ((b - a + math.pi) % (2 * math.pi)) - math.pi
    return a + diff * t

def smooth_rotate_to(current_angle, target_angle, speed=0.1):
    """Smoothly rotate toward a target angle."""
    return lerp_angle(current_angle, target_angle, ease_in_out(speed))
''',
    },
    {
        "tag": "flight-path",
        "category": "feature",
        "code": '''
def great_circle_points(lon1, lat1, lon2, lat2, num_points=50):
    """Generate points along a great circle path between two locations."""
    DEG_TO_RAD = math.pi / 180.0
    lat1_r, lon1_r = lat1 * DEG_TO_RAD, lon1 * DEG_TO_RAD
    lat2_r, lon2_r = lat2 * DEG_TO_RAD, lon2 * DEG_TO_RAD
    d = 2 * math.asin(math.sqrt(
        math.sin((lat2_r - lat1_r) / 2) ** 2 +
        math.cos(lat1_r) * math.cos(lat2_r) *
        math.sin((lon2_r - lon1_r) / 2) ** 2))
    points = []
    if d < 1e-10:
        return [(lon1, lat1)]
    for i in range(num_points + 1):
        f = i / num_points
        A = math.sin((1 - f) * d) / math.sin(d)
        B = math.sin(f * d) / math.sin(d)
        x = A * math.cos(lat1_r) * math.cos(lon1_r) + B * math.cos(lat2_r) * math.cos(lon2_r)
        y = A * math.cos(lat1_r) * math.sin(lon1_r) + B * math.cos(lat2_r) * math.sin(lon2_r)
        z = A * math.sin(lat1_r) + B * math.sin(lat2_r)
        lat = math.atan2(z, math.sqrt(x**2 + y**2)) / DEG_TO_RAD
        lon = math.atan2(y, x) / DEG_TO_RAD
        points.append((lon, lat))
    return points
''',
    },
    {
        "tag": "continent-centroids",
        "category": "feature",
        "code": '''
def compute_centroid(polygon):
    """Compute the centroid of a polygon defined by (lon, lat) points."""
    n = len(polygon)
    if n == 0:
        return (0, 0)
    sum_lon = sum(p[0] for p in polygon)
    sum_lat = sum(p[1] for p in polygon)
    return (sum_lon / n, sum_lat / n)

CONTINENT_CENTROIDS = {}
for _name, _poly in CONTINENTS.items():
    CONTINENT_CENTROIDS[_name] = compute_centroid(_poly)

CONTINENT_AREAS = {
    "North America": 24.71, "South America": 17.84,
    "Europe": 10.18, "Africa": 30.37,
    "Asia": 44.58, "Australia": 8.56, "Greenland": 2.17,
}
''',
    },
    {
        "tag": "color-interpolation",
        "category": "feature",
        "code": '''
def interpolate_color(c1, c2, t):
    """Interpolate between two 256-color values."""
    def to_rgb(c):
        if c < 16: return (0, 0, 0)
        if c < 232:
            c -= 16
            return ((c // 36) * 51, ((c // 6) % 6) * 51, (c % 6) * 51)
        v = 8 + (c - 232) * 10
        return (v, v, v)
    r1, g1, b1 = to_rgb(c1)
    r2, g2, b2 = to_rgb(c2)
    r, g, b = int(r1 + (r2-r1)*t), int(g1 + (g2-g1)*t), int(b1 + (b2-b1)*t)
    if r == g == b:
        return 232 + min(r // 10, 23)
    return 16 + 36*(r//51) + 6*(g//51) + (b//51)
''',
    },
    {
        "tag": "legend",
        "category": "feature",
        "code": '''
def render_legend(use_color=True):
    """Render a legend explaining the globe symbols."""
    entries = [
        ("\\u2588", "Land (near)", COLOR_LAND_NEAR if use_color else ""),
        ("\\u2593", "Land (mid)", COLOR_LAND_MID if use_color else ""),
        ("\\u2591", "Land (far)", COLOR_LAND_FAR if use_color else ""),
        ("~", "Ocean (near)", COLOR_OCEAN_NEAR if use_color else ""),
        (".", "Ocean (far)", COLOR_OCEAN_FAR if use_color else ""),
        ("\\u00b7", "Globe edge", COLOR_LIMB if use_color else ""),
        ("\\u25c6", "Country marker", COLOR_MARKER if use_color else ""),
        ("\\u25cf", "Highlighted", COLOR_HIGHLIGHT if use_color else ""),
    ]
    lines = []
    for symbol, label, color in entries:
        if use_color and color:
            lines.append(f"  {color}{symbol}{RESET} {label}")
        else:
            lines.append(f"  {symbol} {label}")
    return lines
''',
    },
    {
        "tag": "extremes",
        "category": "feature",
        "code": '''
def find_geographic_extremes(country_dict=None):
    """Find the northernmost, southernmost, easternmost, westernmost countries."""
    if country_dict is None:
        country_dict = COUNTRIES
    northernmost = max(country_dict.items(), key=lambda x: x[1][1])
    southernmost = min(country_dict.items(), key=lambda x: x[1][1])
    easternmost = max(country_dict.items(), key=lambda x: x[1][0])
    westernmost = min(country_dict.items(), key=lambda x: x[1][0])
    return {
        "northernmost": (northernmost[0], northernmost[1]),
        "southernmost": (southernmost[0], southernmost[1]),
        "easternmost": (easternmost[0], easternmost[1]),
        "westernmost": (westernmost[0], westernmost[1]),
    }
''',
    },
    {
        "tag": "random-facts",
        "category": "feature",
        "code": '''
GEO_FACTS = [
    "Russia spans 11 time zones",
    "The Pacific Ocean covers more area than all land combined",
    "Africa is the only continent in all four hemispheres",
    "Vatican City is the smallest country at 0.44 km\\u00b2",
    "90% of Earth's population lives in the Northern Hemisphere",
    "The equator is about 40,075 km long",
    "Indonesia has over 17,000 islands",
    "Chile is the longest north-south country",
    "Canada has the longest coastline of any country",
    "Mt. Everest is the highest point at 8,849m",
    "The Mariana Trench is the deepest at -10,994m",
    "Antarctica is the driest continent",
    "The Nile is the longest river at 6,650 km",
    "Lake Baikal holds 20% of the world's fresh water",
    "Australia is wider than the Moon",
]

def get_random_fact():
    """Get a random geographic fact."""
    return random.choice(GEO_FACTS)
''',
    },
    {
        "tag": "info-panel",
        "category": "feature",
        "code": '''
def format_info_panel(country_name):
    """Format a multi-line info panel for a country."""
    lines = [f"  \\u250c\\u2500 {country_name} {'\\u2500' * (30 - len(country_name))}"]
    if country_name in COUNTRIES:
        lon, lat = COUNTRIES[country_name]
        lines.append(f"  \\u2502 Coordinates: {format_coordinates(lon, lat)}")
        tz = approximate_timezone(lon)
        lines.append(f"  \\u2502 Timezone: ~UTC{'+' if tz >= 0 else ''}{tz}")
    if country_name in POPULATIONS:
        lines.append(f"  \\u2502 Population: ~{POPULATIONS[country_name]}M")
    if country_name in CAPITALS:
        lines.append(f"  \\u2502 Capital: {CAPITALS[country_name][0]}")
    if country_name in COUNTRY_AREAS:
        lines.append(f"  \\u2502 Area: {COUNTRY_AREAS[country_name]:,}k km\\u00b2")
    lines.append(f"  \\u2514{'\\u2500' * 36}")
    return "\\n".join(lines)
''',
    },
    {
        "tag": "rotation-presets",
        "category": "feature",
        "code": '''
ROTATION_PRESETS = {
    "americas": -1.5, "europe": 0.0, "asia": 1.5,
    "pacific": 3.0, "atlantic": -0.5, "africa": 0.3,
    "middle-east": 0.8, "southeast-asia": 1.8,
}

def angle_to_view_country(lon, lat):
    """Calculate the rotation angle to center a country on screen."""
    DEG_TO_RAD = math.pi / 180.0
    return -lon * DEG_TO_RAD

def get_region_for_country(country_name):
    """Determine which region preset a country belongs to."""
    if country_name not in COUNTRIES:
        return None
    lon, lat = COUNTRIES[country_name]
    for region, angle in ROTATION_PRESETS.items():
        region_lon = -angle / DEG_TO_RAD
        if abs(lon - region_lon) < 40:
            return region
    return "pacific"
''',
    },
    {
        "tag": "profiling",
        "category": "feature",
        "code": '''
import time as _time

class FrameProfiler:
    """Simple profiler for measuring frame rendering performance."""
    def __init__(self):
        self.frame_times = []
        self.max_samples = 100

    def record(self, elapsed):
        self.frame_times.append(elapsed)
        if len(self.frame_times) > self.max_samples:
            self.frame_times.pop(0)

    def fps(self):
        if not self.frame_times:
            return 0.0
        avg = sum(self.frame_times) / len(self.frame_times)
        return 1.0 / avg if avg > 0 else 0.0

    def summary(self):
        if not self.frame_times:
            return "No data"
        avg = sum(self.frame_times) / len(self.frame_times)
        mn, mx = min(self.frame_times), max(self.frame_times)
        return f"FPS: {1/avg:.1f} | min: {1/mx:.1f} | max: {1/mn:.1f}"
''',
    },
    {
        "tag": "key-legend",
        "category": "feature",
        "code": '''
KEYBINDINGS = {
    "q": "Quit the application",
    "space": "Pause/resume rotation",
    "[": "Decrease rotation speed",
    "]": "Increase rotation speed",
    ",": "Rotate left (when paused)",
    ".": "Rotate right (when paused)",
    "r": "Reset to default view",
    "l": "Toggle country labels",
    "g": "Toggle grid overlay",
    "f": "Toggle facts display",
    "h": "Show help / keybindings",
    "c": "Cycle color themes",
    "t": "Toggle tilt mode",
    "1-9": "Jump to region presets",
}
''',
    },
    {
        "tag": "box-drawing",
        "category": "feature",
        "code": '''
BOX_CHARS = {
    "tl": "\\u2554", "tr": "\\u2557", "bl": "\\u255a", "br": "\\u255d",
    "h": "\\u2550", "v": "\\u2551", "lt": "\\u2560", "rt": "\\u2563",
    "tb": "\\u2566", "bb": "\\u2569", "cross": "\\u256c",
}

def draw_box(width, height, title=""):
    """Create a box-drawing string of given dimensions."""
    if width < 4 or height < 3:
        return []
    top = BOX_CHARS["tl"] + BOX_CHARS["h"] * (width - 2) + BOX_CHARS["tr"]
    mid = BOX_CHARS["v"] + " " * (width - 2) + BOX_CHARS["v"]
    bot = BOX_CHARS["bl"] + BOX_CHARS["h"] * (width - 2) + BOX_CHARS["br"]
    lines = [top]
    if title:
        pad = width - 4 - len(title)
        left, right = pad // 2, pad - pad // 2
        lines.append(BOX_CHARS["v"] + " " * left + title + " " * right + BOX_CHARS["v"])
    else:
        lines.append(mid)
    for _ in range(height - 3):
        lines.append(mid)
    lines.append(bot)
    return lines
''',
    },
    {
        "tag": "scale-bar",
        "category": "feature",
        "code": '''
def render_scale_bar(width_km, chars=20):
    """Render a scale bar for the globe display."""
    km_per_char = width_km / chars
    bar = "\\u251c" + "\\u2500" * (chars - 2) + "\\u2524"
    nice_numbers = [1, 2, 5, 10, 20, 50, 100, 200, 500,
                    1000, 2000, 5000, 10000, 20000]
    label_km = min(nice_numbers, key=lambda x: abs(x - width_km / 2))
    label_str = f"{label_km} km"
    return bar, label_str

def estimate_visible_width():
    """Estimate the km width of the visible globe hemisphere."""
    return 20000  # Approximate visible width in km
''',
    },
    {
        "tag": "country-search-advanced",
        "category": "feature",
        "code": '''
def get_country_info(name):
    """Get all available info about a country."""
    info = {"name": name}
    if name in COUNTRIES:
        lon, lat = COUNTRIES[name]
        info["lon"] = lon
        info["lat"] = lat
        info["formatted_coords"] = format_coordinates(lon, lat)
        info["timezone"] = approximate_timezone(lon)
    if name in POPULATIONS:
        info["population_millions"] = POPULATIONS[name]
    if name in COUNTRY_AREAS:
        info["area_thousands_km2"] = COUNTRY_AREAS[name]
    if name in CAPITALS:
        info["capital"] = CAPITALS[name][0]
        info["capital_coords"] = (CAPITALS[name][1], CAPITALS[name][2])
    return info

def list_countries_by_region():
    """Group countries by approximate region."""
    regions = {}
    for name, (lon, lat) in COUNTRIES.items():
        if lon < -30: region = "Americas"
        elif lon < 40 and lat > 0: region = "Europe"
        elif lon < 55 and lat <= 0: region = "Africa"
        elif lon < 55 and lat > 0: region = "Middle East"
        elif lon < 110: region = "South/Central Asia"
        elif lon < 180: region = "East Asia/Pacific"
        else: region = "Oceania"
        regions.setdefault(region, []).append(name)
    return regions
''',
    },
    {
        "tag": "frame-export",
        "category": "feature",
        "code": '''
def export_frame_to_file(lines, filepath, use_color=True):
    """Export a single rendered frame to a text file."""
    with open(filepath, "w", encoding="utf-8") as f:
        for line in lines:
            f.write(line + "\\n")

def export_frames_to_dir(globe, angle_start, angle_end, steps, directory):
    """Export multiple frames as files for animation/GIF creation."""
    os.makedirs(directory, exist_ok=True)
    for i in range(steps):
        angle = angle_start + (angle_end - angle_start) * i / steps
        lines = globe.render_frame(angle)
        filename = f"frame_{i:04d}.txt"
        filepath = os.path.join(directory, filename)
        export_frame_to_file(lines, filepath, use_color=False)
''',
    },
    {
        "tag": "furthest-pair",
        "category": "feature",
        "code": '''
def find_furthest_pair(country_dict=None):
    """Find the two countries furthest apart on Earth."""
    if country_dict is None:
        country_dict = COUNTRIES
    best_dist = 0
    best_pair = None
    items = list(country_dict.items())
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            n1, (lon1, lat1) = items[i]
            n2, (lon2, lat2) = items[j]
            d = haversine_distance(lon1, lat1, lon2, lat2)
            if d > best_dist:
                best_dist = d
                best_pair = (n1, n2, d)
    return best_pair

def find_neighbours(country_name, country_dict=None, max_km=1500):
    """Find countries within a certain distance."""
    if country_dict is None:
        country_dict = COUNTRIES
    if country_name not in country_dict:
        return []
    lon1, lat1 = country_dict[country_name]
    neighbours = []
    for name, (lon2, lat2) in country_dict.items():
        if name != country_name:
            d = haversine_distance(lon1, lat1, lon2, lat2)
            if d <= max_km:
                neighbours.append((name, round(d)))
    neighbours.sort(key=lambda x: x[1])
    return neighbours
''',
    },
    {
        "tag": "auto-fit",
        "category": "feature",
        "code": '''
def calculate_optimal_size(term_w, term_h, aspect="balanced"):
    """Calculate optimal globe dimensions for terminal size."""
    padding_x, padding_y = 4, 6
    usable_w = term_w - padding_x
    usable_h = term_h - padding_y
    if aspect == "wide":
        width = min(usable_w, 200)
        height = min(usable_h, int(width / 3.5))
    elif aspect == "tall":
        height = min(usable_h, 80)
        width = min(usable_w, int(height * 1.8))
    else:
        width = min(usable_w, 200)
        height = min(usable_h, 80)
        if width / 2 > height:
            width = height * 2
    return max(width, 40), max(height, 16)
''',
    },
    {
        "tag": "globe-stats",
        "category": "feature",
        "code": '''
def compute_globe_stats():
    """Compute interesting statistics about the globe data."""
    total_countries = len(COUNTRIES)
    total_continents = len(CONTINENTS)
    lons = [c[0] for c in COUNTRIES.values()]
    lats = [c[1] for c in COUNTRIES.values()]
    lon_range = max(lons) - min(lons)
    lat_range = max(lats) - min(lats)
    return {
        "countries": total_countries,
        "continents": total_continents,
        "lon_range": round(lon_range, 1),
        "lat_range": round(lat_range, 1),
        "most_eastern": max(COUNTRIES.items(), key=lambda x: x[1][0])[0],
        "most_western": min(COUNTRIES.items(), key=lambda x: x[1][0])[0],
        "most_northern": max(COUNTRIES.items(), key=lambda x: x[1][1])[0],
        "most_southern": min(COUNTRIES.items(), key=lambda x: x[1][1])[0],
    }
''',
    },
    {
        "tag": "continent-populations",
        "category": "data",
        "code": '''
CONTINENT_POPULATIONS = {
    "North America": 0.58, "South America": 0.43,
    "Europe": 0.75, "Africa": 1.46,
    "Asia": 4.75, "Australia": 0.045, "Greenland": 0.000056,
}

def get_countries_in_continent(continent_name):
    """Find which countries fall within a continent polygon."""
    if continent_name not in CONTINENTS:
        return []
    polygon = CONTINENTS[continent_name]
    result = []
    for name, (lon, lat) in COUNTRIES.items():
        if point_in_polygon(lon, lat, polygon):
            result.append(name)
    return sorted(result)
''',
    },
]

# ── Commit messages ──
MESSAGES = [
    "feat({tag}): add {tag} — daily code contribution 🌱",
    "feat({tag}): implement {tag} for globe project 💪",
    "feat({tag}): {tag} — consistent progress ✨",
    "feat({tag}): small daily improvements compound 📈",
    "feat({tag}): building the habit, 5 lines at a time 🚀",
    "feat({tag}): daily code — keeping the streak alive 🔥",
    "feat({tag}): {tag} — real features, real commits 🎯",
    "feat({tag}): incremental improvement — {tag} 🛠️",
]

# ── Add code and commit ──
def add_daily_code(date_str=None):
    if date_str is None:
        date_str = str(datetime.now().date())

    log = load_log()
    day_index = len(log["commits"]) % len(SNIPPETS)
    snippet = SNIPPETS[day_index]
    tag = snippet["tag"]

    # Read the globe file
    target = REPO_DIR / "globe.py"
    content = target.read_text(encoding="utf-8") if target.exists() else ""

    # Add the snippet with markers
    if f"# BEGIN_{tag}" in content:
        print(f"{Y}  ⚠️  '{tag}' already in file, skipping{NC}")
        # Move to next snippet
        day_index = (day_index + 1) % len(SNIPPETS)
        snippet = SNIPPETS[day_index]
        tag = snippet["tag"]
        if f"# BEGIN_{tag}" in content:
            print(f"{Y}  ⚠️  '{tag}' also exists, appending anyway{NC}")

    new_content = content + f"\n# BEGIN_{tag}\n{snippet['code']}\n# END_{tag}\n"
    target.write_text(new_content, encoding="utf-8")

    lines_added = max(len(snippet["code"].strip().split("\n")) + 2, 5)

    # Update .gitignore
    gi = REPO_DIR / ".gitignore"
    gi_text = gi.read_text() if gi.exists() else ""
    if ".daily-log.json" not in gi_text:
        gi_text += "\n.daily-log.json\n"
        gi.write_text(gi_text)

    # Commit
    msg = MESSAGES[day_index % len(MESSAGES)].format(tag=tag)
    git_commit(date_str, msg)

    # Log
    log["commits"].append({
        "date": date_str,
        "category": snippet["category"],
        "tag": tag,
        "lines": lines_added,
    })
    save_log(log)

    print(f"{G}  📝 Added {lines_added} lines → globe.py ({tag}){NC}")
    print(f"{G}  ✅ Committed: {date_str}{NC}")

# ── Backfill ──
def backfill(days):
    today = datetime.now().date()
    start = today - timedelta(days=days)

    print(f"{BOLD}{C}📅 Backfilling {days} days ({start} → {today}){NC}\n")

    committed = 0
    current = start
    while current < today:
        # Skip Sundays
        if current.weekday() == 6:
            print(f"{Y}  ⏭️  {current} (Sunday){NC}")
            current += timedelta(days=1)
            continue
        # 5% random skip for realism
        if random.random() < 0.05:
            print(f"{Y}  ⏭️  {current} (random skip){NC}")
            current += timedelta(days=1)
            continue

        date_str = str(current)
        if not already_committed(date_str):
            add_daily_code(date_str)
            committed += 1
        current += timedelta(days=1)

    pushed = git_push()
    if pushed:
        print(f"\n{G}{BOLD}✅ Pushed {committed} commits!{NC}")
    else:
        print(f"\n{Y}⚠️  Committed locally. Run: git push{NC}")

# ── Stats ──
def show_stats():
    log = load_log()
    commits = log["commits"]
    print(f"{BOLD}{C}📊 GlobL-CLI Portfolio Stats{NC}")
    print("━" * 40)
    if not commits:
        print(f"{Y}No commits yet. Run: python3 daily.py{NC}")
        return
    total_lines = sum(c["lines"] for c in commits)
    cats = {}
    for c in commits:
        cats[c["category"]] = cats.get(c["category"], 0) + 1
    dates = sorted(set(c["date"] for c in commits))
    print(f"  Total commits:  {G}{len(commits)}{NC}")
    print(f"  Total lines:    {G}{total_lines}{NC}")
    print(f"  First commit:   {dates[0]}")
    print(f"  Latest commit:  {dates[-1]}")
    for cat, count in sorted(cats.items(), key=lambda x: -x[1]):
        print(f"    {cat}: {count}")
    print("━" * 40)

# ── Main ──
def main():
    print(f"{BOLD}{C}")
    print("╔════════════════════════════════════════╗")
    print("║  🌍 GlobL-CLI Daily Portfolio Builder  ║")
    print("╚════════════════════════════════════════╝")
    print(f"{NC}")

    args = sys.argv[1:]

    if not args:
        if already_committed():
            print(f"{Y}⚠️  Already committed today! Use --force to override.{NC}")
            return
        add_daily_code()
        pushed = git_push()
        if pushed:
            print(f"{G}✅ Pushed to GitHub!{NC}")
        else:
            print(f"{Y}⚠️  Committed locally. Push manually: git push{NC}")
        show_stats()

    elif args[0] == "--backfill":
        days = int(args[1]) if len(args) > 1 else 30
        backfill(days)

    elif args[0] == "--stats":
        show_stats()

    elif args[0] == "--force":
        add_daily_code()
        git_push()

    elif args[0] in ("--help", "-h"):
        print(__doc__)

    else:
        print(f"{R}Unknown option: {args[0]}{NC}")
        print("Run: python3 daily.py --help")

if __name__ == "__main__":
    main()
