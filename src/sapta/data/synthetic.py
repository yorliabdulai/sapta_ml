"""Synthetic village pit-latrine dataset for demos and tests."""

import numpy as np
import pandas as pd

from sapta.config import load_config


def generate_village_data(
    n_pits: int | None = None,
    seed: int | None = None,
    config: dict | None = None,
) -> pd.DataFrame:
    """
    Generate a simulated village dataset (Northern Ghana coordinates).

    Columns: pit_id, lat, lon, fill_mm, pit_depth_mm, dist_to_well,
    soil_leach_index, vadose_depth_m, latrine_cond_score, forecast_mm.
    """
    cfg = config or load_config()
    data_cfg = cfg["data"]
    n = n_pits if n_pits is not None else data_cfg["n_pits"]
    rng_seed = seed if seed is not None else data_cfg["seed"]

    np.random.seed(rng_seed)
    center_lat = data_cfg["center_lat"]
    center_lon = data_cfg["center_lon"]
    pit_depth = data_cfg["pit_depth_mm"]

    data = {
        "pit_id": [f"PIT-{i:03d}" for i in range(n)],
        "lat": center_lat + np.random.normal(0, 0.005, n),
        "lon": center_lon + np.random.normal(0, 0.005, n),
        "fill_mm": np.random.randint(500, 2500, n),
        "pit_depth_mm": pit_depth,
        "dist_to_well": np.random.uniform(5, 150, n),
        "soil_leach_index": np.random.randint(1, 6, n),
        "vadose_depth_m": np.random.uniform(2, 15, n),
        "latrine_cond_score": np.random.randint(1, 6, n),
        "forecast_mm": np.random.uniform(0, 60, n),
    }
    return pd.DataFrame(data)
