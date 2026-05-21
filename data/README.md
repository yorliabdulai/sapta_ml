# Data

## Current demo data

The pipeline uses **synthetic** village data generated in code (`src/sapta/data/synthetic.py`). This is intentional for hackathon demos and reproducible tests.

Coordinates are centered near Northern Ghana (~10.3°N, -0.8°W). Rainfall uses a CHIRPS-style proxy (`forecast_mm`); real CHIRPS integration is planned.

## Column schema

| Column | Description |
|--------|-------------|
| `pit_id` | Unique pit identifier (e.g. PIT-001) |
| `lat`, `lon` | WGS84 coordinates |
| `fill_mm` | Current fill level (mm) |
| `pit_depth_mm` | Total pit depth (mm) |
| `dist_to_well` | Distance to nearest well (m) |
| `soil_leach_index` | Soil leaching risk (1–5) |
| `vadose_depth_m` | Vadose zone depth (m) |
| `latrine_cond_score` | Structural condition (1–5) |
| `forecast_mm` | Forecast rainfall (mm), CHIRPS proxy |

## Using real data

1. Place CSV files in `data/sample/` (not committed if large).
2. Ensure columns match the schema above (or add an adapter in `src/sapta/data/`).
3. Load in `scripts/run_pipeline.py` or the demo notebook instead of `generate_village_data()`.

Do not commit private or sensitive field data without consent.
