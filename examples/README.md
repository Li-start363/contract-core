# examples: end-to-end 5-minute demo

Demonstrates the full selftune flow (uses a fake engine, costs none of your model quota):

```bash
cd examples
bash run_demo.sh
```

The script will:
1. run the 2 sample tasks in `tasks/` with a fake engine (`printf` standing in for the model), 2 arms × 3 samples;
2. use `scores.json` (pre-assumed scores) to demo the ΔQ report and noise-band comparison;
3. print the verdict format (including "below the noise band = judged no-evidence").

To hook up a real model: swap `--engine` in `run_demo.sh` for your own call command, e.g.:
- `--engine 'claude -p < {prompt}'`
- `--engine 'codex exec --sandbox read-only -m <model> < {prompt}'`

⚠️ Before real runs, read `../selftune/evaluation-environment.md` (empty cwd per cell, tools disabled, isolated agent config, ≥3 samples).
