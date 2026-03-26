import requests
import json
import os
import time

with open("raw_data/cable_meta.json") as f:
    cables = json.load(f)

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
os.makedirs("raw_data", exist_ok=True)

test_cables = cables[:3]
results = []

for i, cable in enumerate(test_cables):
    cable_id = cable["id"]
    url = f"https://www.submarinecablemap.com/api/v3/cable/{cable_id}.json"
    
    try:
        r = requests.get(url, headers=headers, timeout=10)
        r.raise_for_status()
        detail = r.json()
        results.append(detail)
        print(f"[{i+1}/3] OK: {cable_id}")
        print(json.dumps(detail, indent=2, ensure_ascii=False))
        print("---")
        time.sleep(0.3)  # polite delay
    except Exception as e:
        print(f"[{i+1}/3] ERROR: {cable_id} - {e}")

print("\nDone! Check the fields above.")