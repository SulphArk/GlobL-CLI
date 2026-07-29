#!/usr/bin/env python3
"""globe.py — 3d rotating ascii globe. gruvbox'd. no network needed.

    python3 globe.py
    python3 globe.py --speed 2
    python3 globe.py --country Japan
    python3 globe.py --no-labels

keys: q quit · space pause · [ ] speed · , . rotate (paused)
"""

import argparse
import math
import shutil
import sys
import time

try:
    import termios
    import tty
    import select
    POSIX = True
except ImportError:
    POSIX = False


class KeyboardReader:
    def __init__(self):
        self.available = POSIX and sys.stdin.isatty()
        self.saved_terminal = None

    def __enter__(self):
        if self.available:
            self.saved_terminal = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, *args):
        if self.available:
            termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.saved_terminal)

    def read_key(self):
        if not self.available:
            return None
        if select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1)


CONTINENTS = {
    "North America": [
        (-168,66),(-155,70),(-130,70),(-95,70),(-80,73),(-65,68),
        (-55,60),(-52,47),(-65,45),(-75,35),(-80,26),(-97,26),
        (-97,18),(-90,14),(-105,20),(-117,32),(-124,40),(-124,49),
        (-130,55),(-145,60),(-168,66),
    ],
    "South America": [
        (-80,8),(-77,1),(-79,-4),(-81,-15),(-71,-18),(-70,-30),
        (-72,-45),(-68,-55),(-65,-55),(-66,-45),(-58,-38),(-48,-25),
        (-35,-7),(-50,0),(-60,5),(-72,11),(-80,8),
    ],
    "Europe": [
        (-9,43),(-9,53),(-5,58),(5,61),(10,58),(18,59),(25,60),
        (30,60),(40,56),(38,47),(28,45),(20,40),(15,38),(5,43),
        (-2,38),(-9,43),
    ],
    "Africa": [
        (-17,21),(-17,14),(-10,9),(3,5),(9,4),(9,-3),(13,-8),
        (12,-18),(18,-34),(25,-34),(33,-28),(40,-16),(43,-3),
        (51,10),(43,12),(37,15),(32,22),(35,30),(25,32),(10,37),
        (0,35),(-6,35),(-9,30),(-17,21),
    ],
    "Asia": [
        (27,65),(40,66),(60,68),(80,73),(100,76),(140,73),
        (170,67),(180,65),(170,60),(160,55),(140,45),(130,35),
        (122,31),(110,18),(104,8),(95,5),(80,8),(76,10),(72,20),
        (68,24),(61,25),(50,25),(48,30),(35,36),(27,37),(27,45),
        (27,65),
    ],
    "Australia": [
        (113,-22),(122,-18),(130,-12),(137,-12),(142,-11),(148,-20),
        (153,-28),(150,-34),(146,-38),(140,-38),(135,-34),(129,-32),
        (122,-34),(114,-30),(113,-22),
    ],
    "Greenland": [
        (-45,60),(-25,70),(-20,78),(-35,83),(-55,78),(-58,65),
        (-45,60),
    ],
}

COUNTRIES = {
    "USA":(-98.6,39.8),"Canada":(-106.3,56.1),"Mexico":(-102.5,23.6),
    "Brazil":(-51.9,-14.2),"Argentina":(-63.6,-38.4),"Chile":(-71.5,-35.7),
    "Peru":(-75.0,-9.2),"Colombia":(-74.3,4.6),"Venezuela":(-66.6,6.4),
    "Bolivia":(-63.6,-16.3),"Ecuador":(-78.2,-1.8),"Paraguay":(-58.4,-23.4),
    "Uruguay":(-55.8,-32.5),"Cuba":(-77.8,21.5),
    "United Kingdom":(-3.4,55.4),"Ireland":(-8.2,53.4),"France":(2.2,46.6),
    "Spain":(-3.7,40.4),"Portugal":(-8.2,39.4),"Germany":(10.4,51.2),
    "Italy":(12.6,41.9),"Switzerland":(8.2,46.8),"Austria":(14.5,47.5),
    "Netherlands":(5.3,52.1),"Belgium":(4.5,50.5),"Poland":(19.1,51.9),
    "Sweden":(18.6,60.1),"Norway":(8.5,60.5),"Finland":(25.7,61.9),
    "Denmark":(9.5,56.3),"Greece":(21.8,39.1),"Ukraine":(31.2,48.4),
    "Romania":(25.0,45.9),"Iceland":(-19.0,64.9),"Russia":(90.0,61.5),
    "Turkey":(35.2,39.0),"Egypt":(30.8,26.8),"Nigeria":(8.7,9.1),
    "South Africa":(24.7,-30.6),"Kenya":(37.9,-0.0),"Ethiopia":(40.5,9.1),
    "Morocco":(-7.1,31.8),"Algeria":(1.7,28.0),"Libya":(17.2,26.3),
    "Sudan":(30.2,12.9),"Tanzania":(34.9,-6.4),"Ghana":(-1.0,7.9),
    "DR Congo":(21.8,-4.0),"Angola":(17.9,-11.2),"Zambia":(27.8,-13.1),
    "Madagascar":(46.9,-18.8),
    "China":(104.2,35.9),"India":(78.9,20.6),"Japan":(138.3,36.2),
    "South Korea":(127.8,36.5),"North Korea":(127.5,40.3),
    "Mongolia":(103.8,46.9),"Kazakhstan":(66.9,48.0),"Iran":(53.7,32.4),
    "Iraq":(43.7,33.2),"Saudi Arabia":(45.1,23.9),"Israel":(35.2,31.0),
    "Pakistan":(69.3,30.4),"Afghanistan":(67.7,33.9),"Nepal":(84.1,28.4),
    "Bangladesh":(90.4,23.7),"Myanmar":(95.9,21.9),"Thailand":(101.0,15.9),
    "Vietnam":(108.3,14.1),"Cambodia":(104.9,12.6),"Malaysia":(101.9,4.2),
    "Indonesia":(113.9,-0.8),"Philippines":(121.8,12.9),"Sri Lanka":(80.8,7.9),
    "Yemen":(48.5,15.6),"Syria":(38.9,34.8),"Jordan":(36.2,31.2),
    "UAE":(54.4,24.0),"Uzbekistan":(64.6,41.4),
    "Turkmenistan":(59.6,38.9),"Taiwan":(121.0,23.7),"Laos":(102.5,19.9),
    "Australia":(134.0,-25.3),"New Zealand":(174.9,-40.9),
    "Papua New Guinea":(147.2,-6.3),
}


DEG_TO_RAD = math.pi / 180.0


def lonlat_to_xyz(lon, lat):
    lon_rad = lon * DEG_TO_RAD
    lat_rad = lat * DEG_TO_RAD
    cos_lat = math.cos(lat_rad)
    return cos_lat * math.cos(lon_rad), math.sin(lat_rad), cos_lat * math.sin(lon_rad)


def rotate_y(x, y, z, angle):
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    return x * cos_a + z * sin_a, y, -x * sin_a + z * cos_a


def rotate_x(x, y, z, angle):
    cos_a, sin_a = math.cos(angle), math.sin(angle)
    return x, y * cos_a - z * sin_a, y * sin_a + z * cos_a


def point_in_polygon(lon, lat, polygon):
    n = len(polygon)
    
    inside = False
    j = n - 1
    for i in range(n):
        xi, yi = polygon[i]
        xj, yj = polygon[j]
        if (yi > lat) != (yj > lat):
            if lon < xi + (lat - yi) * (xj - xi) / (yj - yi + 1e-15):
                inside = not inside
        j = i
    return inside


def is_land(lon, lat):
    for polygon in CONTINENTS.values():
        if point_in_polygon(lon, lat, polygon):
            return True
    return False


GRID_STEP = 3
LAND_POINTS = None


def build_land_cache():
    global LAND_POINTS
    LAND_POINTS = set()
    for lat in range(-90, 91, GRID_STEP):
        for lon in range(-180, 181, GRID_STEP):
            if is_land(lon, lat):
                LAND_POINTS.add((lon, lat))


RESET = "\x1b[0m"


def fg_color(n, bold=False):
    return f"\x1b[{('1;' if bold else '')}38;5;{n}m"


COLOR_LAND_NEAR = fg_color(142)
COLOR_LAND_MID = fg_color(100)
COLOR_LAND_FAR = fg_color(243)
COLOR_OCEAN_NEAR = fg_color(66)
COLOR_OCEAN_FAR = fg_color(24)
COLOR_LIMB = fg_color(237)
COLOR_MARKER = fg_color(214)
COLOR_HIGHLIGHT = fg_color(167, True)
COLOR_TEXT = fg_color(223)
COLOR_DIM = fg_color(246)
COLOR_HEADER = fg_color(180)
COLOR_BG = "\x1b[48;5;0m"


class Globe:
    def __init__(self, width, height, tilt_degrees=15.0):
        self.width = width
        self.height = height
        self.tilt = tilt_degrees * DEG_TO_RAD

    def render_frame(self, angle, highlighted_country=None, show_labels=True):
        width, height = self.width, self.height
        buffer = [[' '] * width for _ in range(height)]
        zbuffer = [[-2.0] * width for _ in range(height)]
        center_x = width / 2.0
        center_y = height / 2.0
        radius_x = min(center_x, center_y * 2.0) - 2
        radius_y = radius_x / 2.0
        step = GRID_STEP

        lat = -90
        while lat <= 90:
            lon = -180
            while lon <= 180:
                x, y, z = lonlat_to_xyz(lon, lat)
                x, y, z = rotate_x(x, y, z, self.tilt)
                x, y, z = rotate_y(x, y, z, angle)
                if z > 0:
                    px = int(center_x + x * radius_x)
                    py = int(center_y - y * radius_y)
                    if 0 <= px < width and 0 <= py < height and z > zbuffer[py][px]:
                        zbuffer[py][px] = z
                        if (lon, lat) in LAND_POINTS:
                            buffer[py][px] = '█' if z > 0.6 else ('▓' if z > 0.25 else '░')
                        else:
                            buffer[py][px] = '~' if z > 0.5 else '.'
                lon += step
            lat += step

        labels = []
        for name, (lon, lat) in COUNTRIES.items():
            x, y, z = lonlat_to_xyz(lon, lat)
            x, y, z = rotate_x(x, y, z, self.tilt)
            x, y, z = rotate_y(x, y, z, angle)
            if z < 0.15:
                continue
            px = int(center_x + x * radius_x)
            py = int(center_y - y * radius_y)
            if 0 <= px < width and 0 <= py < height:
                buffer[py][px] = '●' if name == highlighted_country else '◆'
                if z > 0.5:
                    labels.append((px, py, name, name == highlighted_country))

        for i in range(720):
            t = i * math.pi / 360
            px = int(center_x + math.cos(t) * radius_x)
            py = int(center_y + math.sin(t) * radius_y)
            if 0 <= px < width and 0 <= py < height and buffer[py][px] == ' ':
                buffer[py][px] = '·'

        lines = [''.join(row) for row in buffer]

        if show_labels:
            labels.sort(key=lambda item: -1 if item[3] else 0)
            used_rows = set()
            count = 0
            for px, py, name, is_highlighted in labels:
                if count >= 10 and not is_highlighted:
                    continue
                if py in used_rows and not is_highlighted:
                    continue
                used_rows.add(py)
                text = f' {name}'
                line = lines[py]
                start = min(px + 1, width - 1)
                if start + len(text) <= width:
                    lines[py] = (line[:start] + text + line[start + len(text):])[:width]
                count += 1

        return lines


def paint_line(line):
    char_colors = {
        '█': COLOR_LAND_NEAR,
        '▓': COLOR_LAND_MID,
        '░': COLOR_LAND_FAR,
        '~': COLOR_OCEAN_NEAR,
        '.': COLOR_OCEAN_FAR,
        '·': COLOR_LIMB,
        '●': COLOR_HIGHLIGHT,
        '◆': COLOR_MARKER,
    }
    out = [COLOR_BG]
    current = COLOR_BG
    for ch in line:
        color = char_colors.get(ch, COLOR_TEXT)
        if color != current:
            out.append(color)
            current = color
        out.append(ch)
    out.append(RESET)
    return ''.join(out)


def main():
    parser = argparse.ArgumentParser(description='3d rotating globe — gruvbox edition')
    parser.add_argument('--speed', type=float, default=1.0, help='rotation speed')
    parser.add_argument('--tilt', type=float, default=15.0, help='axial tilt degrees')
    parser.add_argument('--no-labels', action='store_true', help='hide labels')
    parser.add_argument('--no-color', action='store_true', help='no colors')
    parser.add_argument('--country', type=str, default=None, help='highlight a country')
    parser.add_argument('--fps', type=float, default=15.0, help='target fps')
    args = parser.parse_args()

    if args.country and args.country not in COUNTRIES:
        matches = [c for c in COUNTRIES if args.country.lower() in c.lower()]
        if matches:
            args.country = matches[0]
        else:
            print(f"unknown country '{args.country}', try: {', '.join(sorted(COUNTRIES))}")
            sys.exit(1)

    term_width, term_height = shutil.get_terminal_size((120, 40))
    width = min(term_width - 2, 200)
    height = min(term_height - 5, 80)
    width, height = max(width, 40), max(height, 16)

    build_land_cache()

    globe = Globe(width, height, args.tilt)
    angle = 0.0
    speed = args.speed * 0.05
    paused = False
    show_labels = not args.no_labels
    use_color = not args.no_color and sys.stdout.isatty()
    frame_time = 1.0 / max(args.fps, 1.0)

    sys.stdout.write('\x1b[?25l\x1b[48;5;0m\x1b[2J\x1b[H')
    sys.stdout.flush()

    with KeyboardReader() as keyboard:
        try:
            while True:
                t0 = time.time()
                lines = globe.render_frame(angle, args.country, show_labels)

                header = ' ◆ globe — q quit · space pause · [ ] speed · , . rotate'
                if args.country:
                    header += f'  ● {args.country}'
                footer = f' {"paused" if paused else "spinning"}  {speed/0.05:.1f}x'

                output = ['\x1b[H']
                output.append(COLOR_HEADER + COLOR_BG + header + RESET + '\r\n')
                for line in lines:
                    output.append((paint_line(line) if use_color else COLOR_BG + line + RESET) + '\r\n')
                output.append(COLOR_DIM + COLOR_BG + footer + RESET + '\r\n')

                sys.stdout.write(''.join(output))
                sys.stdout.flush()

                key = keyboard.read_key()
                if key == 'q':
                    break
                if key == ' ':
                    paused = not paused
                if key == '[':
                    speed = max(0, speed - 0.01)
                if key == ']':
                    speed += 0.01
                if key == ',' and paused:
                    angle -= 0.1
                if key == '.' and paused:
                    angle += 0.1

                if not paused:
                    angle += speed

                remaining = frame_time - (time.time() - t0)
                if remaining > 0:
                    time.sleep(remaining)

        except KeyboardInterrupt:
            pass

    sys.stdout.write(RESET + '\x1b[?25h\x1b[48;5;0m\x1b[2J\x1b[H')
    sys.stdout.flush()
    print('  bye')


if __name__ == '__main__':
    main()
# BEGIN_haversine-distance

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

# END_haversine-distance

# BEGIN_timezone-overlay

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

# END_timezone-overlay

# BEGIN_more-countries

# Additional territories and small nations
EXTRA_PLACES = {
    "Fiji": (178.0, -17.8), "Samoa": (-172.0, -13.8),
    "Tonga": (-175.2, -21.2), "Maldives": (73.5, 3.2),
    "Bahrain": (50.6, 26.1), "Qatar": (51.2, 25.4),
    "Kuwait": (47.5, 29.4), "Oman": (55.9, 21.5),
    "Lebanon": (35.9, 33.9), "Georgia": (43.4, 42.3),
    "Armenia": (45.0, 40.1), "Azerbaijan": (47.6, 40.1),
}

# END_more-countries

# BEGIN_population-data

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

# END_population-data

# BEGIN_color-themes

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

# END_color-themes

# BEGIN_coord-formatter

def format_coordinates(lon, lat):
    """Format lon/lat as DMS string like '51\u00b030\'N 0\u00b007\'W'."""
    def dms(val, pos_label, neg_label):
        direction = pos_label if val >= 0 else neg_label
        val = abs(val)
        degrees = int(val)
        minutes = int((val - degrees) * 60)
        seconds = int(((val - degrees) * 60 - minutes) * 60)
        return f"{degrees}\u00b0{minutes}'{seconds}\"{direction}"
    lat_str = dms(lat, "N", "S")
    lon_str = dms(lon, "E", "W")
    return f"{lat_str} {lon_str}"

# END_coord-formatter

# BEGIN_bearing-calc

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

# END_bearing-calc

# BEGIN_antipode

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

# END_antipode

# BEGIN_daylight-calc

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

# END_daylight-calc

# BEGIN_grid-overlay

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

# END_grid-overlay

# BEGIN_capitals

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

# END_capitals

# BEGIN_country-areas

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

# END_country-areas

# BEGIN_midpoint

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

# END_midpoint

# BEGIN_country-search

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

# END_country-search

# BEGIN_smooth-rotation

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

# END_smooth-rotation

# BEGIN_flight-path

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

# END_flight-path

# BEGIN_continent-centroids

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

# END_continent-centroids

# BEGIN_color-interpolation

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

# END_color-interpolation

# BEGIN_legend

def render_legend(use_color=True):
    """Render a legend explaining the globe symbols."""
    entries = [
        ("\u2588", "Land (near)", COLOR_LAND_NEAR if use_color else ""),
        ("\u2593", "Land (mid)", COLOR_LAND_MID if use_color else ""),
        ("\u2591", "Land (far)", COLOR_LAND_FAR if use_color else ""),
        ("~", "Ocean (near)", COLOR_OCEAN_NEAR if use_color else ""),
        (".", "Ocean (far)", COLOR_OCEAN_FAR if use_color else ""),
        ("\u00b7", "Globe edge", COLOR_LIMB if use_color else ""),
        ("\u25c6", "Country marker", COLOR_MARKER if use_color else ""),
        ("\u25cf", "Highlighted", COLOR_HIGHLIGHT if use_color else ""),
    ]
    lines = []
    for symbol, label, color in entries:
        if use_color and color:
            lines.append(f"  {color}{symbol}{RESET} {label}")
        else:
            lines.append(f"  {symbol} {label}")
    return lines

# END_legend

# BEGIN_extremes

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

# END_extremes

# BEGIN_random-facts

GEO_FACTS = [
    "Russia spans 11 time zones",
    "The Pacific Ocean covers more area than all land combined",
    "Africa is the only continent in all four hemispheres",
    "Vatican City is the smallest country at 0.44 km\u00b2",
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

# END_random-facts

# BEGIN_info-panel

def format_info_panel(country_name):
    """Format a multi-line info panel for a country."""
    lines = [f"  \u250c\u2500 {country_name} {'\u2500' * (30 - len(country_name))}"]
    if country_name in COUNTRIES:
        lon, lat = COUNTRIES[country_name]
        lines.append(f"  \u2502 Coordinates: {format_coordinates(lon, lat)}")
        tz = approximate_timezone(lon)
        lines.append(f"  \u2502 Timezone: ~UTC{'+' if tz >= 0 else ''}{tz}")
    if country_name in POPULATIONS:
        lines.append(f"  \u2502 Population: ~{POPULATIONS[country_name]}M")
    if country_name in CAPITALS:
        lines.append(f"  \u2502 Capital: {CAPITALS[country_name][0]}")
    if country_name in COUNTRY_AREAS:
        lines.append(f"  \u2502 Area: {COUNTRY_AREAS[country_name]:,}k km\u00b2")
    lines.append(f"  \u2514{'\u2500' * 36}")
    return "\n".join(lines)

# END_info-panel

# BEGIN_rotation-presets

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

# END_rotation-presets

# BEGIN_profiling

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

# END_profiling
