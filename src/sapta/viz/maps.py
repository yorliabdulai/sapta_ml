"""Folium map visualization for pit priorities and dispatch status."""

from pathlib import Path

import folium
import pandas as pd


def create_pitch_map(df: pd.DataFrame) -> folium.Map:
    """Build an interactive map colored by priority_score and dispatch status."""
    m = folium.Map(location=[df["lat"].mean(), df["lon"].mean()], zoom_start=15)

    for _, row in df.iterrows():
        color = (
            "red"
            if row["priority_score"] > 0.7
            else "orange"
            if row["priority_score"] > 0.4
            else "green"
        )
        icon = "truck" if row.get("status") == "DISPATCHED" else "info-sign"

        folium.Marker(
            location=[row["lat"], row["lon"]],
            popup=(
                f"ID: {row['pit_id']}<br>"
                f"Score: {row['priority_score']:.2f}<br>"
                f"Status: {row.get('status', 'N/A')}"
            ),
            icon=folium.Icon(color=color, icon=icon),
        ).add_to(m)

    return m


def save_map(m: folium.Map, path: str | Path) -> Path:
    """Write Folium map to HTML."""
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    m.save(str(out))
    return out
