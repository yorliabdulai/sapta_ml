#!/usr/bin/env python3
"""End-to-end SAPTA demo: synthetic data -> score -> dispatch -> CSV + map."""

import argparse
import sys
from pathlib import Path

# Allow running without pip install -e .
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import matplotlib.pyplot as plt

from sapta.config import load_config
from sapta.data.synthetic import generate_village_data
from sapta.dispatch.greedy import optimize_dispatch
from sapta.scoring import score_dataframe
from sapta.viz.maps import create_pitch_map, save_map


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Run SAPTA priority and dispatch pipeline")
    p.add_argument("--seed", type=int, default=None, help="Random seed (default from config)")
    p.add_argument("--n-pits", type=int, default=None, help="Number of pits (default from config)")
    p.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "outputs",
        help="Directory for priorities.csv and map.html",
    )
    p.add_argument(
        "--assets-dir",
        type=Path,
        default=ROOT / "assets",
        help="Directory for sample_priority_hist.png",
    )
    p.add_argument("--config", type=Path, default=None, help="Path to YAML config")
    return p.parse_args()


def main() -> None:
    args = parse_args()
    config = load_config(args.config) if args.config else load_config()

    df = generate_village_data(n_pits=args.n_pits, seed=args.seed, config=config)
    df = score_dataframe(df)
    df = optimize_dispatch(df, config=config)

    out_dir = args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = out_dir / "priorities.csv"
    df.to_csv(csv_path, index=False)

    map_path = out_dir / "map.html"
    m = create_pitch_map(df)
    save_map(m, map_path)

    # Sample chart for README / assets
    assets_dir = args.assets_dir
    assets_dir.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.hist(df["priority_score"], bins=15, color="#2E86AB", edgecolor="white")
    ax.set_title("Distribution of Priority Scores")
    ax.set_xlabel("Priority score")
    ax.set_ylabel("Number of pits")
    fig.tight_layout()
    hist_path = assets_dir / "sample_priority_hist.png"
    fig.savefig(hist_path, dpi=120)
    plt.close(fig)

    dispatched = (df["status"] == "DISPATCHED").sum()
    print("SAPTA pipeline complete.")
    print(f"  Pits: {len(df)} | Dispatched: {dispatched} | Waiting: {len(df) - dispatched}")
    print(f"  CSV:  {csv_path}")
    print(f"  Map:  {map_path}")
    print(f"  Chart: {hist_path}")
    print("Open map.html in a browser to explore the demo.")


if __name__ == "__main__":
    main()
