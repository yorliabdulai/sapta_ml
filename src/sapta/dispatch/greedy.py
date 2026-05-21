"""Greedy vacuum-truck dispatch by priority score."""

import pandas as pd

from sapta.config import load_config


def optimize_dispatch(
    df: pd.DataFrame,
    truck_capacity: int | None = None,
    hours_limit: float | None = None,
    service_time_hours: float | None = None,
    config: dict | None = None,
) -> pd.DataFrame:
    """
    Assign DISPATCHED or WAITING status by descending priority_score.

    Greedy: each pit takes service_time_hours until capacity or hours_limit.
    """
    cfg = config or load_config()
    d = cfg["dispatch"]
    capacity = truck_capacity if truck_capacity is not None else d["truck_capacity"]
    hours = hours_limit if hours_limit is not None else d["hours_limit"]
    service_time = (
        service_time_hours if service_time_hours is not None else d["service_time_hours"]
    )

    df_sorted = df.sort_values(by="priority_score", ascending=False).copy()
    total_time = 0.0
    dispatched: list[str] = []

    for idx, row in df_sorted.iterrows():
        if total_time + service_time <= hours and len(dispatched) < capacity:
            total_time += service_time
            dispatched.append(row["pit_id"])
            df_sorted.at[idx, "status"] = "DISPATCHED"
        else:
            df_sorted.at[idx, "status"] = "WAITING"

    return df_sorted
