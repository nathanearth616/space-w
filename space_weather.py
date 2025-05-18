import requests
import argparse
import time
from datetime import datetime, timezone
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLOR = True
except ImportError:
    COLOR = False

# NOAA SWPC endpoints
ENDPOINTS = {
    'plasma': 'https://services.swpc.noaa.gov/products/solar-wind/plasma-5-minute.json',
    'mag': 'https://services.swpc.noaa.gov/products/solar-wind/mag-5-minute.json',
    'kp': 'https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json',
    # Continuous GOES X-ray flux (last 7 days)
    'xray': 'https://services.swpc.noaa.gov/json/goes/primary/xrays-7-day.json',
}

ALERT_THRESHOLDS = {
    'kp': 5,
    'speed': 600,
    'bz': -5,
    'xray': 1e-6,
}

def fetch_json(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def color_text(label, value, threshold, higher_worse=True):
    if not COLOR:
        return f"{label}: {value}"
    val = float(value)
    alert = val >= threshold if higher_worse else val <= threshold
    color = Fore.RED if alert else Fore.GREEN
    return f"{label}: {color}{value}{Style.RESET_ALL}"

def get_latest(endpoint):
    data = fetch_json(ENDPOINTS[endpoint])
    return data[-1]

def display(show_xray=False):
    # Solar wind plasma
    t, density, speed, temp = get_latest('plasma')
    print('--- Solar Wind (Plasma) ---')
    print(f"Time (UTC): {t}")
    print(color_text('Density p/cm³', density, 5, higher_worse=True))
    print(color_text('Speed km/s', speed, ALERT_THRESHOLDS['speed'], higher_worse=True))
    print(f"Temperature K: {temp}\n")

    # Magnetic field (ACE)
    mag_row = get_latest('mag')
    t2 = mag_row[0]
    bz = mag_row[3]
    print('--- Interplanetary Magnetic Field (ACE) ---')
    print(f"Time (UTC): {t2}")
    print(color_text('Bz GSM (nT)', bz, ALERT_THRESHOLDS['bz'], higher_worse=False))
    print()

    # Kp index
    kp_row = get_latest('kp')
    t3, kp_val, _, a_index = kp_row[:4]
    print('--- Geomagnetic Indices (Kp) ---')
    print(f"Time (UTC): {t3}")
    print(color_text('Kp Index', kp_val, ALERT_THRESHOLDS['kp']))
    print(f"A Index (3-hr avg): {a_index}\n")

    # X-ray flux
    if show_xray:
        x_row = get_latest('xray')
        # NOAA GOES X-ray JSON: dict with keys like 'time_tag', 'flux'
        t4 = x_row.get('time_tag', 'N/A')
        flux = x_row.get('flux', 'N/A')
        print('--- GOES X-ray Flux (1–8Å, last week) ---')
        print(f"Time (UTC): {t4}")
        print(color_text('Flux W/m²', flux, ALERT_THRESHOLDS['xray']))
        print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Enhanced Space Weather CLI")
    parser.add_argument('-a', '--all', action='store_true', dest='show_xray', help='Show all data including X-ray flux')
    parser.add_argument('-w', '--watch', type=int, metavar='SEC', help='Refresh every SEC seconds')
    args = parser.parse_args()

    if args.watch:
        try:
            while True:
                print(f"=== {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')} ===\n")
                display(show_xray=args.show_xray)
                time.sleep(args.watch)
        except KeyboardInterrupt:
            print('Exiting watch mode.')
    else:
        display(show_xray=args.show_xray)