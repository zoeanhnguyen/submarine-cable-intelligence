import pandas as pd
import json


bridge  = pd.read_csv("clean_data/cable_landingpoint_bridge.csv")
cables  = pd.read_csv("clean_data/cables.csv")
lp_sum  = pd.read_csv("clean_data/landing_points_summary.csv")


country_stats = (
    bridge.groupby("country")
    .agg(
        total_cables    =("cable_id",  "nunique"),
        total_lp        =("lp_id",     "nunique"),
    )
    .reset_index()
)

country_stats["redundancy_score"] = (
    country_stats["total_cables"] * 0.7 +
    country_stats["total_lp"]     * 0.3
).round(2)

country_stats["risk_level"] = pd.cut(
    country_stats["total_cables"],
    bins   =[0, 1, 3, 6, 999],
    labels =["CRITICAL", "HIGH", "MEDIUM", "LOW"]
)

country_stats = country_stats.sort_values("total_cables", ascending=False)
country_stats.to_csv("clean_data/country_risk.csv", index=False)
print(f"Saved: country_risk.csv — {len(country_stats)} countries")
print("\nTop 10 most connected countries:")
print(country_stats.head(10).to_string(index=False))
print("\nHighest risk countries (1 cable only):")
critical = country_stats[country_stats["risk_level"] == "CRITICAL"]
print(f"  {len(critical)} countries with only 1 cable")


big_tech_cols = ["is_google", "is_meta", "is_amazon", "is_microsoft", "is_china"]
tech_summary = []

labels = {
    "is_google"   : "Google",
    "is_meta"     : "Meta",
    "is_amazon"   : "Amazon",
    "is_microsoft": "Microsoft",
    "is_china"    : "China Telecom/Mobile/Unicom",
}

for col, label in labels.items():
    owned = cables[cables[col] == 1]
    tech_summary.append({
        "company"          : label,
        "cables_owned"     : len(owned),
        "pct_of_total"     : round(len(owned) / len(cables) * 100, 1),
        "active_cables"    : len(owned[owned["is_planned"] == False]),
        "planned_cables"   : len(owned[owned["is_planned"] == True]),
        "total_length_km"  : owned["length_km"].sum(),
        "avg_length_km"    : owned["length_km"].mean().round(0),
    })

df_tech = pd.DataFrame(tech_summary).sort_values("cables_owned", ascending=False)
df_tech.to_csv("clean_data/bigtech_ownership.csv", index=False)
print(f"\nSaved: bigtech_ownership.csv")
print(df_tech.to_string(index=False))


cables_clean = cables.dropna(subset=["rfs_year"]).copy()
cables_clean["rfs_year"] = cables_clean["rfs_year"].astype(int)
cables_clean["decade"] = (cables_clean["rfs_year"] // 10 * 10).astype(str) + "s"

timeline = (
    cables_clean[cables_clean["is_planned"] == False]
    .groupby("rfs_year")
    .agg(
        cables_launched =("cable_id", "count"),
        total_length_km =("length_km", "sum"),
    )
    .reset_index()
)
timeline["cumulative_cables"] = timeline["cables_launched"].cumsum()
timeline.to_csv("clean_data/timeline.csv", index=False)
print(f"\nSaved: timeline.csv — {len(timeline)} years")


vn_bridge = bridge[bridge["country"] == "Vietnam"]
vn_cables = cables[cables["cable_id"].isin(vn_bridge["cable_id"])].copy()


vn_owners = []
for _, row in vn_cables.iterrows():
    if pd.notna(row["owners_raw"]):
        for owner in row["owners_raw"].split(","):
            owner = owner.strip()
            if owner:
                vn_owners.append({
                    "cable_id"  : row["cable_id"],
                    "cable_name": row["cable_name"],
                    "owner"     : owner,
                    "rfs_year"  : row["rfs_year"],
                    "is_planned": row["is_planned"],
                })

df_vn_owners = pd.DataFrame(vn_owners)
df_vn_owners.to_csv("clean_data/vietnam_cable_owners.csv", index=False)


vn_lp_risk = (
    vn_bridge.groupby("lp_name")
    .agg(cables_through=("cable_id", "nunique"))
    .reset_index()
)
vn_lp_risk["pct_of_vn_cables"] = (
    vn_lp_risk["cables_through"] / vn_cables["cable_id"].nunique() * 100
).round(1)
vn_lp_risk.to_csv("clean_data/vietnam_lp_risk.csv", index=False)

print(f"\nSaved: vietnam_cable_owners.csv & vietnam_lp_risk.csv")
print("\n=== VIETNAM LANDING POINT RISK ===")
print(vn_lp_risk.sort_values("cables_through", ascending=False).to_string(index=False))

spof = lp_sum[lp_sum["cable_count"] >= 8].copy()
spof["spof_risk"] = pd.cut(
    spof["cable_count"],
    bins   =[7, 10, 15, 999],
    labels =["HIGH", "VERY HIGH", "CRITICAL"]
)
spof = spof.sort_values("cable_count", ascending=False)
spof.to_csv("clean_data/spof_global.csv", index=False)
print(f"\nSaved: spof_global.csv — {len(spof)} critical nodes")
print(spof[["lp_name", "country", "cable_count", "spof_risk"]].to_string(index=False))

print("\nALL TABLES READY FOR DASHBOARD")
print("\nFiles in clean_data/:")
import os
for f in sorted(os.listdir("clean_data")):
    size = os.path.getsize(f"clean_data/{f}") // 1024
    print(f"  {f:45s} {size:>4} KB")