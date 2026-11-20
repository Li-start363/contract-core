# Criteria Generator (falsification-triple draft)

Usage: fill in the template below and send it to your model (with or without the contract), and it will produce a criteria draft for your domain. **The draft needs your sign-off**; once finalized, freeze it before running experiments.

---
## Template (copy this block, replace 【】)

My domain/task: [e.g., feature selection for encrypted traffic classification]

What I plan to do: [e.g., compare two field-importance readings and pick the more stable one]

Please produce a "falsification triple" draft, each item concrete enough to execute:
1. **Threshold**: what number/phenomenon counts as "done right"? (must be measurable, e.g. "the new reading's top-10 overlaps the old reading's by ≥6" rather than "better")
2. **Degradation plan**: if the threshold is not met, what next? (at least two options, including a "narrow the claim" option — e.g. "claim validity only in scenario X")
3. **Refuse-to-judge rules**: under what circumstances must **no conclusion** be drawn? (e.g. "no significance call with <30 samples" / "judge disagreement >10 points goes to arbitration first")

Additional requirements:
- first list 2-3 "trivial explanations" (what might this result merely be due to? e.g. version mix-up / mismatched definitions / task too easy), and how to rule them out;
- state "what signal shows my approach failed" (failure signals; don't just describe what success looks like).
---

## Usage notes (earned by measurement)
- **Rules before results**: the triple is frozen before the data is seen; to change it, record errata — don't quietly change the threshold.
- **The threshold must clear the noise floor**: the score difference from two runs of the same config is your floor, and any "improvement" verdict must exceed it (measured: single-sample text-scoring noise can reach the ±50 level).
- **Refuse-to-judge rules are what save you**: better "insufficient evidence, no call" than "looks about right, so conclude".
