# Template: pre-registration + downgrade table (rules before results)

> Usage: fill in and freeze **before** the experiment/measurement starts; after results arrive you may only append an "errata / addenda" section — the original criteria must not be edited.

## 0. Proposition
- H1: 【claim, written in a refutable form】
- Criteria (frozen): 【threshold + verdict rule, e.g.: domain mean difference ≥−10 and ≥2/3 of tasks ≥−5; or: 95% one-sided lower bound > −5】

## 1. Materials and configuration (frozen)
- Tasks/data: 【list, fixed before results】
- Arms/conditions: 【how the control is set up】
- Runs: independent context per cell; ≥3 samples/arm; only transport failures may be retried; refusals/truncation kept as valid results.
- Scoring: 【dual judge / machine grading; anonymous; how disagreements are adjudicated】

## 2. Noise floor (must be measured)
The score-difference distribution of two arms under the same configuration (content exactly identical) = your floor. **Any "improvement ≥X" must clear the floor.**

## 3. Downgrade table (frozen)
| Failure signal | Disposition |
|---|---|
| Criteria pass only on some tasks/domains | narrow the claim to the passing domains, state the failure boundary honestly |
| Replication set does not support it | downgrade to "valid within a single task family / single dataset" |
| Noise band ≥ the claimed improvement | judge "no evidence", add samples or switch to mechanical criteria |
| Environment contaminated (tools / old files / charter) | void the whole batch and rerun; do not cherry-pick cells to replace |

## 4. Trivial-explanation exclusion (before starting)
【List 2-3 "this result might just be because of X" (task too easy / grader bias / mismatched definitions), and how to rule them out】

## Errata / addenda (leave empty for later)
