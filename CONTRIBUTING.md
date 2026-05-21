# Contributing to SAPTA

Thank you for improving SAPTA. This project is hackathon-scoped: prefer small, clear changes over large refactors.

## Setup

```bash
pip install -r requirements.txt
pip install -e ".[dev]"
```

On Windows, use `py -m pytest -q` and `py scripts/run_pipeline.py` if bare `python` fails (Store alias).

## Before you open a PR

1. Run tests: `py -m pytest -q` (Windows) or `pytest -q`
2. Run the pipeline: `py scripts/run_pipeline.py` or `./scripts/run.ps1`
3. If you edit notebooks, clear outputs: `nbstripout notebooks/*.ipynb` (install `[dev]` extras)

## Code guidelines

- Core logic belongs in `src/sapta/`, not notebooks.
- Keep scoring weights in `configs/default.yaml`.
- Do not add ML dependencies unless there is a real training/inference path.
- Label synthetic vs real data in docs and code comments.

## Pull requests

- One logical change per PR when possible.
- Update README if CLI, config, or outputs change.
- Include a short test for new scoring or dispatch behavior.

## Questions

Open a GitHub issue on [yorliabdulai/sapta_ml](https://github.com/yorliabdulai/sapta_ml).
