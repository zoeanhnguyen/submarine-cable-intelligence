# Submarine Cable Intelligence 
### *What keeps the internet alive — and who controls it?*

[![Tableau](https://img.shields.io/badge/Tableau-Public-blue)](https://public.tableau.com/app/profile/zoe.nguyen2497/viz/SubmarineCableIntelligenceWhatKeepstheInternetAlive/Dashboard2)
[![Python](https://img.shields.io/badge/Python-3.14-green)](https://python.org)
[![Data](https://img.shields.io/badge/Data-submarinecablemap.com-orange)](https://submarinecablemap.com)

---

## The Question That Started This

One day I was browsing the web and a question hit me:

> *"Why can millions of people around the world access the same website 
> at the same moment?"*

The answer isn't the cloud. It's not satellites.  
It's **691 physical cables** lying on the ocean floor — and most people 
have never heard of them.

So I decided to map all of them.

---

## What I Built

An interactive intelligence dashboard that answers 4 questions 
no one is asking — but everyone should be:

| Question | Key Finding |
|----------|-------------|
| Who controls the ocean floor? | Google owns 34 cables — more than Meta & Amazon combined |
| Where are the weakest points? | 33 nodes that could disconnect entire regions if they fail |
| How exposed is Vietnam? | 3 landing points. Vung Tau handles 50% alone. |
| How fast is this growing? | From 0 to 596 active cables in 30 years |

**[→ View Live Dashboard](https://public.tableau.com/app/profile/zoe.nguyen2497/viz/SubmarineCableIntelligenceWhatKeepstheInternetAlive/Dashboard2)**

---

## Tech Stack & Workflow
```
Chrome DevTools (use F12)
        ↓
    Extract 3 JSON files from submarinecablemap.com API
        ↓
    Python + Pandas — parse, clean, engineer features
        ↓
    7 CSV files (691 cables · 1,908 landing points · 186 countries)
        ↓
    Tableau Public — interactive dashboard
```

### Tools Used
- **Data Collection**: Chrome DevTools Network tab → JSON extraction
- **Data Processing**: Python 3.14, Pandas, Requests
- **Visualization**: Tableau Public
- **Environment**: VS Code, Jupyter Notebook

---

## Dataset

Self-collected via Chrome DevTools — no Kaggle, no pre-built datasets.

| File | Rows | Description |
|------|------|-------------|
| `cables.csv` | 691 | Cable metadata: name, owners, year, length |
| `cable_landingpoint_bridge.csv` | 3,157 | Cable ↔ landing point relationships |
| `landing_points_summary.csv` | 1,908 | Global landing points with cable counts |
| `country_risk.csv` | 186 | Redundancy score per country |
| `bigtech_ownership.csv` | 5 | Big Tech cable ownership breakdown |
| `spof_global.csv` | 33 | Single Point of Failure nodes |
| `vietnam_lp_risk.csv` | 3 | Vietnam landing point risk analysis |

---

## Key Insights

**🌐 Global Infrastructure**
- 99% of international internet traffic travels through submarine cables
- Batam, Indonesia is the #1 landing point globally with 20 cables
- 24 countries have only 1 cable — zero redundancy

** Big Tech Ocean Control**
- Google: 34 cables (4.9% of global total)
- China Telecom/Mobile/Unicom: 27 cables, averaging 10,615 km each
- Amazon: only 1 active cable today — but 4 more under construction

** Infrastructure Risk**
- 33 critical nodes identified as Single Points of Failure
- Batam failure = ~40% of Southeast Asia connectivity lost
- Marseille, Mumbai, and Singapore each carry 16 cables

** Vietnam Analysis**
- Only 3 landing points for 97 million people
- Vung Tau handles 50% of all cable capacity
- 2 of 8 cables still under construction (2027)
- Vietnam's landing points carry 3x fewer cables than SEA average

---

## Data Challenges (Interview-Ready Stories)

1. **API endpoint changed** — `cable.json` returned empty response. 
   Solved by inspecting Network tab and discovering `all.json` endpoint.

2. **Owners data not normalized** — same company listed as 
   "Google LLC", "Google", "Alphabet". Built regex mapping to standardize.

3. **691 individual API calls** — fetched detail for each cable separately 
   with rate limiting (0.2s delay) to avoid server blocks.

4. **LineString geometry** — cable route coordinates not usable directly 
   in Tableau. Used landing point coordinates instead.

---

## Project Structure
```
submarine_project/
├── raw_data/
│   ├── cable_meta.json
│   ├── cable_geo.json
│   ├── landing_points.json
│   └── cable_details_all.json
├── clean_data/
│   ├── cables.csv
│   ├── cable_landingpoint_bridge.csv
│   ├── landing_points_summary.csv
│   ├── country_risk.csv
│   ├── bigtech_ownership.csv
│   ├── spof_global.csv
│   └── vietnam_lp_risk.csv
├── download_data.py
├── fetch_cable_details.py
├── build_dataset.py
├── final_analysis.py
└── README.md
```

---

## How to Reproduce
```bash
# 1. Clone the repo
git clone https://github.com/[your-username]/submarine-cable-intelligence

# 2. Install dependencies
pip install requests pandas

# 3. Fetch raw data
python download_data.py
python fetch_cable_details.py

# 4. Build clean dataset
python build_dataset.py
python final_analysis.py

# 5. Open Tableau Public and import clean_data/ folder
```

---

## Skills Demonstrated

`Data Collection` `API Extraction` `Chrome DevTools` `Python` 
`Pandas` `Data Cleaning` `Data Modeling` `Tableau` 
`Dashboard Design` `Geospatial Analysis` `Storytelling`

---

*Data source: [Submarine Cable Map](https://submarinecablemap.com) 
by TeleGeography · Last updated: March 2026*
```

