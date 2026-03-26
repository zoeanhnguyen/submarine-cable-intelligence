import requests
import json
import os

os.makedirs("raw_data", exist_ok=True)

urls = {
    "cable_meta"    : "https://www.submarinecablemap.com/api/v3/cable/cable.json",
    "cable_geo"     : "https://www.submarinecablemap.com/api/v3/cable/cable-geo.json",
    "landing_points": "https://www.submarinecablemap.com/api/v3/landing-point/landing-point-geo.json"
}

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}

for name, url in urls.items():
    print(f"Downloading {name}...")
    try:
        r = requests.get(url, headers=headers, timeout=15)
        r.raise_for_status()
        filepath = f"raw_data/{name}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(r.json(), f, ensure_ascii=False, indent=2)
        size_kb = len(r.content) // 1024
        print(f"OK: {name}.json - {size_kb} KB")
    except Exception as e:
        print(f"LOI: {name} - {e}")

print("Done!Check raw data")