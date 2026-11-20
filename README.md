# Contract Core — lift cheap LLMs to flagship level on creative tasks

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**A 5-clause prompt "contract" that makes cheap models think before they write — measured across ~200 controlled outputs, with a self-optimization kit and an honest failure map.**

One-liner: put a 5-clause "contract" in front of a cheap model (plan first / rule out trivial explanations / state what would falsify you / no fabrication / report honestly) and it gets close to a flagship model running bare on creative tasks — self-tuning kit and honest failure map included.

> Status: **experimental**. Evidence from ~200 controlled outputs (4-arm/5-arm × blind dual-judge, pre-registered). Not a guarantee — read the failure map below before use.

## Evidence (measured, 2026-11)

| Task domain | Cheap model + contract vs flagship bare | Mechanism gain (contract − bare, cheap model) | Verdict |
|---|---|---|---|
| Research / creative ideas | within ~2.5–12 pts (two independent task sets) | **+17.7 / +9.0** (both non-trivial) | direction consistent (claim scope & replication status: see failure map) |
| Engineering (code) | competitive (per-item spread −75.5…+92.5) | +6.0 (set A, below +10 threshold); code-task mechanical scores saturated at 100/100 | reliability insurance in restricted sandboxes (qualitative); mechanism gain **not established** |
| Writing | −9.3 / −7.5 (both sets) | −7.0 (set A) / +1.3 (set B) — **not reliable** | **failure boundary**: no reliable gain, and the lifted model still trails flagship bare on both sets |
| Data analysis | −4.7 (set A) / +7.3 (set B) | +1.7 / +3.3 (below +10 threshold) | no useful gain (the earlier ≈0 figure referred to information-synthesis tasks, old S-set, ≈0 there) |

- Diminishing gains (observation): the weaker the model, the more it benefits — cheap +6.25 / mid +3.25 / frontier +0.5 (pilot, n=2, exploratory only).

  ![Diminishing contract gain (pilot, n=2, exploratory): cheap +6.25 / mid +3.25 / frontier +0.5](assets/gain_curve.png)

```
┌─────────────────────────────────────────────┐
│  contracts/contract-core.md   ← the 5 clauses │
│        │                                      │
│        ▼                                      │
│  your agent runtime (hook / system prompt)    │
│        │                                      │
│        ▼                                      │
│  selftune/  ← measure, prune, inject pitfalls │
│    calibrate → A/B → prune → pitfalls → criteria│
└─────────────────────────────────────────────┘
```

## 30-second quick start

```bash
# 1) prepend contracts/contract-core.md to your task prompt
# 2) run one A/B (>=3 samples per arm)
python3 selftune/ab_runner.py --tasks my_tasks/ \
  --engine 'claude -p < {prompt}' --samples 3 --out runs/
# 3) score, then get the DeltaQ report (against the noise band)
python3 selftune/ab_runner.py --analyze runs/ --scores scores.json
```

End-to-end example (5 min): `examples/`.

## Self-tuning kit (selftune/, five pieces)

| Piece | File | What it does |
|---|---|---|
| Calibrator | `selftune/calibrate/` | 8 probes with difficulty gradient → capability profile + recommended clause config |
| A/B runner | `selftune/ab_runner.py` | paired bare/contract runs, >=3 samples/arm, DeltaQ with noise band |
| Pruning protocol | `selftune/pruning-protocol.md` | delete-clause rules with >=2-locatable-evidence threshold (judged before results) |
| Pitfall injector | `selftune/pitfall_inject.py` | your lessons → standard pitfall entries → hook injection |
| Criteria generator | `selftune/criteria-generator.md` | falsification-triple template (threshold / degradation plan / refuse-to-judge) |

**Three hard rules** (learned the hard way): the evaluation environment must be bare (`selftune/evaluation-environment.md`); always multi-sample against the noise band (**measured: same-prompt twin runs can differ at the ±50 level — single-sample conclusions are worthless**); pruning requires locatable evidence.

## Scope & safety

- MIT license; no telemetry; runs fully local against your own model endpoint.
- Contract text is model-agnostic: swap models without swapping the contract, and re-measure the gain after a swap (the kit includes calibration).

## Failure map (quick reference; full version in [docs/applicability-map.md](docs/applicability-map.md))

**Where it helps (measured):**

| Scenario | Finding |
|---|---|
| ✅ Ideas / plans / design / review (think-before-you-write) | real, non-trivial lift **+17.7 / +9.0** (two independent task sets); targets exactly this domain's failure modes (wishful reasoning, fabrication, unfalsifiable claims) |
| ✅ Delivery reliability in restricted sandboxes | "insurance" value (qualitative; behavioral evidence from an external 13-task code study) |
| ✅ Weaker models benefit more | diminishing gains (pilot n=2, observation-level; two warnings attached — score ceiling and difference-score coupling; not a promise) |

**Where it hurts / boundaries (all measured):**

| Boundary | Detail |
|---|---|
| ❌ Finished prose / deliverable writing | no reliable gain (−7.0 / +1.3 across two sets), and the lifted model still trails flagship bare (−9.3 / −7.5) — **don't use it there**; the scaffolding spends the deliverable's budget and reads as boilerplate |
| ❌ Data / computation tasks | no useful gain (+1.7 / +3.3, below the +10 threshold; information-synthesis ≈0) |
| ⚠️ Generality of the research lift | direction-consistent but **strict independent replication did not pass** (n=3/domain, CI very wide) — claims scoped accordingly |
| ⚠️ Self-optimization (clause pruning) | **not proven** (G≈+0.9 < noise floor) — pruning needs runnable tests, not text evidence |
| ⚠️ Noise | same-prompt twin runs can differ at the ±50 level: **single-sample conclusions are worthless**; >=3 samples per arm against the noise band |
| ⚠️ Validity | LLM-as-judge (cross-family dual judging mitigates, not removes), single cheap-model subject, 4 task domains, evaluation environment must be bare (learned after three full-batch reworks) |

**One-liner**: use it for think-before-you-write tasks (ideas / plans / design / review); don't use it for finished prose or pure computation; measure on your own tasks first (selftune, 30 min).

---

## Summary

A 5-clause "contract core" for cheap models: measured gains of +17.7/+9.0 on creative tasks (two independent task sets, blind dual-judge, pre-registered), approaching flagship-bare performance with consistent direction; no reliable gain on writing (−7.0/+1.3, still trails flagship bare) and no useful gain on data tasks (+1.7/+3.3, below threshold) — failure boundaries published in full. Ships with a self-tuning kit (calibration / A-B measurement / pruning protocol / pitfall injection / criteria generation) and an evaluation-environment spec. Measured warning: single-sample scoring noise can reach the ±50 level — any gain claim must multi-sample against the noise band.

## Provenance

The experiments were run with the Chinese-language originals of the contract, task materials and instruments; the files in this repository are faithful English translations. The exact as-tested bytes are preserved at git tag `pre-english-20261120`.
