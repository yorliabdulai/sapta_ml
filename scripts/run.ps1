# SAPTA pipeline (Windows). Uses the py launcher when "python" is not on PATH.
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

if (Get-Command py -ErrorAction SilentlyContinue) {
    py scripts/run_pipeline.py @args
} else {
    python scripts/run_pipeline.py @args
}
