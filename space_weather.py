import requests
import argparse

def fetch_json(url):
    resp = requests.get(url)
    resp.raise_for_status()
    return resp.json()

def get_solar_wind():
    url = 'https://services.swpc.noaa.gov/products/solar-wind/plasma-5-minute.json'
    data = fetch_json(url)
    latest = data[-1]
    print('--- Solar Wind (Plasma) ---')
    print(f"Time (UTC): {latest[0]}")
    print(f"Density (p/cm³): {latest[1]}")  # particle density
    print(f"Speed (km/s): {latest[2]}")
    print(f"Temperature (K): {latest[3]}")
    print()

def get_magnetic_field():
    url = 'https://services.swpc.noaa.gov/products/solar-wind/mag-5-minute.json'
    data = fetch_json(url)
    latest = data[-1]
    print('--- Interplanetary Magnetic Field (ACE) ---')
    print(f"Time (UTC): {latest[0]}")
    print(f"Bz (GSM, nT): {latest[3]}")  # southward component
    print()

def get_kp_index():
    url = 'https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json'
    data = fetch_json(url)
    latest = data[-1]
    print('--- Geomagnetic Indices (Kp) ---')
    print(f"Time (UTC): {latest[0]}")
    print(f"Kp Index: {latest[1]}")
    print(f"A Index (3-hr avg): {latest[3]}")
    print()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Fetch today's space weather data")
    parser.add_argument('--all', action='store_true', help='Include magnetic field and KP index')
    args = parser.parse_args()

    get_solar_wind()  # plasma-5-minute.json ([services.swpc.noaa.gov](https://services.swpc.noaa.gov/products/solar-wind/?utm_source=chatgpt.com))
    if args.all:
        get_magnetic_field()  # mag-5-minute.json ([services.swpc.noaa.gov](https://services.swpc.noaa.gov/products/solar-wind/?utm_source=chatgpt.com))
        get_kp_index()  # noaa-planetary-k-index.json ([reddit.com](https://www.reddit.com/r/pushcut/comments/130x8n1/widget_to_display_the_current_noaaplanetarykindex/?utm_source=chatgpt.com))
