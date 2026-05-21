"""Calibrated heuristic priority index for pit latrine servicing."""

import numpy as np

from sapta.config import load_config


class SaniFlowCore:
    """
    SAPTA scoring engine (SaniFlow brain layer).

    Computes a normalized priority index (0.0–1.0) from telemetry and static
    asset data using domain-calibrated weights.
    """

    def __init__(
        self,
        weights: dict[str, float] | None = None,
        rain_cap_mm: float | None = None,
        distance_decay_m: float | None = None,
        vadose_max_m: float | None = None,
        ordinal_scale_max: float | None = None,
        config: dict | None = None,
    ):
        cfg = config or load_config()
        scoring = cfg["scoring"]
        self.weights = weights or scoring["weights"]
        self.rain_cap_mm = rain_cap_mm if rain_cap_mm is not None else scoring["rain_cap_mm"]
        self.distance_decay_m = (
            distance_decay_m if distance_decay_m is not None else scoring["distance_decay_m"]
        )
        self.vadose_max_m = vadose_max_m if vadose_max_m is not None else scoring["vadose_max_m"]
        self.ordinal_scale_max = (
            ordinal_scale_max if ordinal_scale_max is not None else scoring["ordinal_scale_max"]
        )

    def get_priority_index(self, telemetry: dict, static_data: dict) -> float:
        """
        Calculate normalized priority score in [0, 1].

        telemetry: fill_mm, forecast_mm
        static_data: pit_depth_mm, dist_to_well_m, leach_index,
                     vadose_depth_m, condition_index
        """
        f_fill = telemetry["fill_mm"] / static_data["pit_depth_mm"]
        f_rain = np.clip(telemetry["forecast_mm"] / self.rain_cap_mm, 0, 1)
        f_dist = np.exp(-static_data["dist_to_well_m"] / self.distance_decay_m)
        f_leach = static_data["leach_index"] / self.ordinal_scale_max
        f_vadose = 1 - (static_data["vadose_depth_m"] / self.vadose_max_m)
        f_cond = static_data["condition_index"] / self.ordinal_scale_max

        score = (
            self.weights["fill"] * f_fill
            + self.weights["rain"] * f_rain
            + self.weights["dist"] * f_dist
            + self.weights["leach"] * f_leach
            + self.weights["vadose"] * f_vadose
            + self.weights["cond"] * f_cond
        )
        return float(np.clip(score, 0, 1))
