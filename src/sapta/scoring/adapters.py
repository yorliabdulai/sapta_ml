"""Adapters between DataFrame rows and SaniFlowCore I/O schema."""

import pandas as pd

from sapta.scoring.engine import SaniFlowCore


def row_to_packets(row: pd.Series) -> tuple[dict, dict]:
    """Map a village DataFrame row to telemetry and static_data dicts."""
    telemetry = {
        "fill_mm": row["fill_mm"],
        "forecast_mm": row["forecast_mm"],
    }
    static_data = {
        "pit_depth_mm": row["pit_depth_mm"],
        "dist_to_well_m": row["dist_to_well"],
        "leach_index": row["soil_leach_index"],
        "vadose_depth_m": row["vadose_depth_m"],
        "condition_index": row["latrine_cond_score"],
    }
    return telemetry, static_data


def score_row(row: pd.Series, engine: SaniFlowCore) -> float:
    """Score a single pit row."""
    telemetry, static_data = row_to_packets(row)
    return engine.get_priority_index(telemetry, static_data)


def score_dataframe(df: pd.DataFrame, engine: SaniFlowCore | None = None) -> pd.DataFrame:
    """Add priority_score column to a village DataFrame."""
    engine = engine or SaniFlowCore()
    out = df.copy()
    out["priority_score"] = out.apply(lambda row: score_row(row, engine), axis=1)
    return out
