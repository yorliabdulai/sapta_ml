# Models

There is **no trained ML artifact** in this repository yet.

SAPTA v0.1 uses a **domain-calibrated heuristic** priority index (`SaniFlowCore` in `src/sapta/scoring/engine.py`). Weights and thresholds live in `configs/default.yaml`.

## Future

- Learned weights from historical overflow / contamination events (e.g. gradient boosting)
- Serialized models saved here as `priority_model.json` or similar
- Versioned config alongside each artifact

Until then, `models/` remains a placeholder for hackathon judges to see where production artifacts would live.
