"""Tests for greedy dispatch."""

import pandas as pd

from sapta.data.synthetic import generate_village_data
from sapta.dispatch.greedy import optimize_dispatch
from sapta.scoring import score_dataframe


def _scored_df(n=30, seed=42):
    return score_dataframe(generate_village_data(n_pits=n, seed=seed))


def test_dispatch_respects_capacity():
    df = optimize_dispatch(_scored_df(), truck_capacity=10, hours_limit=999)
    assert (df["status"] == "DISPATCHED").sum() == 10


def test_dispatch_respects_hours():
    df = optimize_dispatch(
        _scored_df(),
        truck_capacity=100,
        hours_limit=48,
        service_time_hours=2,
    )
    assert (df["status"] == "DISPATCHED").sum() == 24


def test_dispatch_prioritizes_high_scores():
    df = optimize_dispatch(_scored_df(), truck_capacity=5, hours_limit=48)
    dispatched = df[df["status"] == "DISPATCHED"]["priority_score"]
    waiting = df[df["status"] == "WAITING"]["priority_score"]
    assert dispatched.min() >= waiting.max()


def test_all_rows_have_status():
    df = optimize_dispatch(_scored_df())
    assert set(df["status"].unique()) <= {"DISPATCHED", "WAITING"}
