# selftune: the self-tuning kit (five pieces for downloaders)

Lets any cheap model + "contract core" catch up to flagship — and lets you measure on your own tasks what that gain is worth.
All local, free (you only spend your own model calls), no subscription needed.

## User journey (up and running in ~30 minutes)
1. **Calibrate** `calibrate/` — 8 probes with a difficulty gradient, producing a capability profile (strengths/weaknesses) and a recommended clause config (~10 minutes)
2. **A/B measurement** `ab_runner.py` — run bare/contract arms on your own 2 real tasks, **≥3 samples per arm** (see "why multi-sample is mandatory" below), get a ΔQ report with noise band
3. **Prune** `pruning-protocol.md` — keep/drop clauses one by one per the ΔQ report (criteria are locked before running the A/B), then re-test
4. **Pitfall injection** `pitfall_inject.py` — feed your own pitfalls back into the mechanism so it reminds you automatically next time
5. **Criteria** `criteria-generator.md` — generate a "falsification triple" draft for your domain (threshold / degradation plan / refuse-to-judge rules)

## Three hard rules (learned the hard way; details in `evaluation-environment.md`)
1. **The evaluation environment must be bare**: empty working directory + tools disabled + isolated agent config (AGENTS/skills/hooks). Otherwise the model goes off "delegating / writing files / reading old answers", and what you measure is not the model itself.
2. **Multi-sample is mandatory**: score differences between two runs of the same prompt can reach the ±50 level (measured), so single-sample ΔQ is untrustworthy. ≥3 samples per arm, report mean ± band.
3. **Pruning requires locatable evidence**: a clause may only be deleted when a conflict/error/delivery loss with a locatable position can be found in ≥2 tasks; if no evidence can be found, keep it (that is a valid result).

## The five pieces
| Piece | File | Input | Output |
|---|---|---|---|
| Calibrator | `calibrate/` | 8 probes | capability profile + recommended clause config |
| A/B runner | `ab_runner.py` | your tasks + model command | ΔQ report (with noise band) |
| Pruning protocol | `pruning-protocol.md` | ΔQ report | pruning table + M1 contract |
| Pitfall injector | `pitfall_inject.py` | pitfall markdown | standard pitfall-library entry + hook injection snippet |
| Criteria generator | `criteria-generator.md` | domain Q&A | falsification-triple draft |

The contract core text lives in `../contracts/contract-core.md` (5 clauses: plan first / rule out trivial explanations / falsifiable·stop-loss / no fabrication / report honestly).
