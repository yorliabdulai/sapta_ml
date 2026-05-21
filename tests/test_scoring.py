"""Tests for SaniFlowCore priority scoring."""

import numpy as np
import pandas as pd
import pytest

from sapta.data.synthetic import generate_village_data
from sapta.scoring.adapters import row_to_packets, score_dataframe, score_row
from sapta.scoring.engine import SaniFlowCore


def test_score_in_unit_interval():
    engine = SaniFlowCore()
    df = generate_village_data(n_pits=20, seed=0)
    scored = score_dataframe(df, engine)
    assert scored["priority_score"].min() >= 0.0
    assert scored["priority_score"].max() <= 1.0


def test_known_row_deterministic():
    engine = SaniFlowCore()
    row = pd.Series(
        {
            "fill_mm": 2000,
            "forecast_mm": 40,
            "pit_depth_mm": 2500,
            "dist_to_well": 20,
            "soil_leach_index": 3,
            "vadose_depth_m": 5,
            "latrine_cond_score": 4,
        }
    )
    s1 = score_row(row, engine)
    s2 = score_row(row, engine)
    assert s1 == pytest.approx(s2)
    assert 0 <= s1 <= 1


def test_adapter_packets_keys():
    row = generate_village_data(n_pits=1, seed=1).iloc[0]
    telemetry, static_data = row_to_packets(row)
    assert set(telemetry) == {"fill_mm", "forecast_mm"}
    assert "dist_to_well_m" in static_data
    engine = SaniFlowCore()
    assert engine.get_priority_index(telemetry, static_data) == pytest.approx(
        score_row(row, engine)
    )


def test_reproducible_with_seed():
    a = score_dataframe(generate_village_data(seed=42))["priority_score"].values
    b = score_dataframe(generate_village_data(seed=42))["priority_score"].values
    np.testing.assert_array_equal(a, b)
