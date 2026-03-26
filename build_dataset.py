import requests
import json
import os
import time
import pandas as pd

HEADERS = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"}
BASE_URL = "https://www.submarinecablemap.com/api/v3/cable/{}.json"
os.makedirs("clean_data", exist_ok=True)

with open("raw_data/cable_meta.json") as f:
    cables = json.load(f)
print(f"Total cables to fetch: {len(cables)}")


all_details = []
failed = []

for i, cable in enumerate(cables):
    cable_id = cable["id"]
    url = BASE_URL.format(cable_id)

    try:
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        all_details.append(r.json())

        if (i + 1) % 50 == 0:
            print(f"  Progress: {i+1}/{len(cables)} cables fetched...")

        time.sleep(0.2)  # polite delay — avoid rate limiting

    except Exception as e:
        print(f"  FAILED: {cable_id} — {e}")
        failed.append(cable_id)

print(f"\nFetch complete: {len(all_details)} success, {len(failed)} failed")

with open("raw_data/cable_details_all.json", "w") as f:
    json.dump(all_details, f, ensure_ascii=False, indent=2)
print("Saved: raw_data/cable_details_all.json")

BIG_TECH = {
    "is_google" : ["Google"],
    "is_meta"   : ["Meta", "Facebook"],
    "is_amazon" : ["Amazon"],
    "is_microsoft": ["Microsoft"],
    "is_china"  : ["China Telecom", "China Mobile", "China Unicom", "Huawei", "CITIC"],
}

cable_rows = []
for c in all_details:
    owners = c.get("owners") or ""
    row = {
        "cable_id"    : c.get("id"),
        "cable_name"  : c.get("name"),
        "length_raw"  : c.get("length"),
        "length_km"   : None, 
        "rfs_year"    : c.get("rfs_year"),
        "is_planned"  : c.get("is_planned"),
        "owners_raw"  : owners,
        "num_owners"  : len([o.strip() for o in owners.split(",") if o.strip()]),
        "num_landing_points": len(c.get("landing_points") or []),
        "url"         : c.get("url"),
    }

    for flag, keywords in BIG_TECH.items():
        row[flag] = int(any(k.lower() in owners.lower() for k in keywords))

    if row["length_raw"]:
        cleaned = row["length_raw"].replace(",", "").replace("km", "").strip().split()[0]
        try:
            row["length_km"] = float(cleaned)
        except:
            row["length_km"] = None

    cable_rows.append(row)

df_cables = pd.DataFrame(cable_rows)
df_cables.to_csv("clean_data/cables.csv", index=False)
print(f"Saved: clean_data/cables.csv — {len(df_cables)} rows")

bridge_rows = []
for c in all_details:
    for lp in (c.get("landing_points") or []):
        bridge_rows.append({
            "cable_id"  : c.get("id"),
            "cable_name": c.get("name"),
            "lp_id"     : lp.get("id"),
            "lp_name"   : lp.get("name"),
            "country"   : lp.get("country"),
        })

df_bridge = pd.DataFrame(bridge_rows)
df_bridge.to_csv("clean_data/cable_landingpoint_bridge.csv", index=False)
print(f"Saved: clean_data/cable_landingpoint_bridge.csv — {len(df_bridge)} rows")

lp_summary = (
    df_bridge
    .groupby(["lp_id", "lp_name", "country"])
    .agg(cable_count=("cable_id", "nunique"))
    .reset_index()
    .sort_values("cable_count", ascending=False)
)
lp_summary.to_csv("clean_data/landing_points_summary.csv", index=False)
print(f"Saved: clean_data/landing_points_summary.csv — {len(lp_summary)} rows")

print("\n===== QUICK STATS =====")
print(f"Total cables       : {len(df_cables)}")
print(f"Active cables      : {(~df_cables['is_planned']).sum()}")
print(f"Planned cables     : {df_cables['is_planned'].sum()}")
print(f"Google cables      : {df_cables['is_google'].sum()}")
print(f"Meta cables        : {df_cables['is_meta'].sum()}")
print(f"Amazon cables      : {df_cables['is_amazon'].sum()}")
print(f"China cables       : {df_cables['is_china'].sum()}")
print(f"\nTop 10 landing points by cable count:")
print(lp_summary.head(10)[["lp_name", "country", "cable_count"]].to_string(index=False))
