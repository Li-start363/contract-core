#!/usr/bin/env bash
# End-to-end demo: fake engine runs A/B -> fake scoring -> ΔQ report. Costs no model quota.
set -euo pipefail
cd "$(dirname "$0")"
SELF="../selftune/ab_runner.py"

# 1) run 2 arms x 3 samples (fake engine: just prints fixed text)
python3 "$SELF" --tasks tasks --engine 'printf "demo-answer"' --samples 3 --out runs_demo

# 2) demo the analysis with fake scores (swap in your own scoring JSON for real use)
python3 "$SELF" --analyze runs_demo --scores scores.json

echo ""
echo "Verdict format: ΔQ above the noise band (5 points) = evidence; below the noise band = judged 'no evidence', add samples or switch to mechanical criteria."
