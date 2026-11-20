# Applicability map: where the contract core helps / where it hurts

> Subject under test = the **5 contract-core clauses** (prompt-level mechanism). Evidence = two independent task sets (set A 12 tasks / set B 12 tasks, 4-5 arms, anonymous dual judging, pre-registration + errata on file), ≈200 controlled outputs. All numbers are measured; mechanism explanations are tagged 【speculation】.

## Summary

The contract layer is **not** a universal booster. It is a *scaffold against sloppy reasoning*, and scaffolding helps only where the failure mode is sloppy reasoning:

| Domain | Mechanism gain (contract − bare, cheap model) | Verdict |
|---|---|---|
| Research / creative design | **+17.7 / +9.0** (two independent sets) | use it |
| Engineering / code | +6 / +28 (highly noisy, environment-sensitive) | use as delivery-reliability insurance |
| Data analysis / computation | ≈ +2 | skip — no gain |
| Writing / final-deliverable prose | **−7.0 / +1.3** (direction consistent) | **do not use — it hurts** |

## 1. Gain zone (strong): research / creative / planning tasks

**Measured**: A−D (mechanism gain) +17.7 (set A) / +9.0 (set B), non-trivial (D−B ≈ −20 on both sets); non-inferior to flagship bare (set A passed the strict threshold; set B direction-consistent but did not pass the strict line).
**Why it works 【speculation】**: the failure mode of these tasks is "assuming without thinking, fabrication, ignoring trivial explanations, giving unfalsifiable conclusions" — the contract's plan-first / rule-out-trivial-explanations / no-fabrication / falsifiable clauses each hit exactly one of these. Thinking before writing when generating ideas gives a clear score lift.
**Boundary**: the magnitude swings widely across task families (on R1-type "predictive modeling proposal" tasks the cheap model's baseline is already weak, and the contract cannot fix a baseline gap); strict independent replication did not pass, one-sided 95% CI very wide (n=3/domain) — **the claim is "direction-consistent gain", not "confirmed to catch up with flagship"**.

## 2. Gain zone (weak / conditional): engineering / code

**Measured**: magnitude +6~+28, but highly noisy and inconsistent across the two sets; no strong claim.
**The real value is reliability insurance 【speculation】**: in restricted environments (read-only / no tools), a common bare-arm failure is "request an environment change" refusals (0 points), while the contract arm delivers anyway (the report-honestly clause makes it deliver what it can, honestly). Delivery failure drops from catastrophic to manageable.
**Boundary**: on routine coding tasks where both arms get full marks the contract adds nothing; once the evaluation environment is not bare (tools / old files / agent charter), the data gets contaminated — that lesson paid for `selftune/evaluation-environment.md`.

## 3. Neutral zone: data analysis / computation

**Measured**: A−D ≈ +2 (set A) / +3 (set B), D−B near the trivial line.
**Explanation 【speculation】**: right or wrong is decided by arithmetic; the contract does not change the numbers, it only adds a few boilerplate paragraphs. **Costs nothing but useless** — drop it, or keep only the "no fabrication" clause against invented numbers.

## 4. Negative-gain zone (stable): writing / finished-deliverable prose

**Measured**: all three writing tasks negative on set A (bare 91.5/87/86 vs contract 83.5/77/83, mean −7.0), set B −7.5 vs flagship — **two independent datasets pointing the same way, judged a stable failure boundary**.
**Why it gets worse 【speculation】**: the contract's structural overhead (plan paragraph / trivial-exclusion / stop-loss paragraph) is pure cost in tasks where the deliverable is everything: it eats the word budget and gives the deliverable a "wrapped-in-shell" feel, while grading only rewards the deliverable quality the task asked for. Stuff plan and stop-loss into a 180-character client note and what loses is the deliverable itself.
**Conclusion: do not wrap writing / announcement / abstract tasks in the contract**; if you only want to guard against fabrication, use just the "no fabrication + report honestly" pair, not the full set.

## 5. Boundaries of self-optimization (clause pruning)

Measured with simulated downloaders: **"deleting clauses makes it better" is not proven** (G≈+0.9, below the noise band; of two downloaders, one deleted and one kept, and the deleting one gained nothing either). Pruning itself is workable (the evidence rule functions), but any gain has to be shown by re-testing. **Conclusion: self-optimization depends on runnable verification signals (a tester)**; text-only evidence is not enough.

## 6. Limitations table (as they are)

1. **Small sample**: 3 tasks × 2 sets per domain; CI very wide, does not support "confirmed"-tier claims.
2. **Confirmation replication did not pass**: the R domain's strict threshold was not met on set B (short by 1.8 points); the claim has been downgraded per the pre-registration to "valid within a single task family + direction consistent".
3. **LLM-as-judge**: cross-family dual judging + anonymity + disagreement annotation mitigates family bias but does not remove it; domains without mechanical criteria (research/writing) retain grading subjectivity.
4. **Large noise floor**: score differences between two same-contract arms can reach the ±50 level, so single-sample conclusions are untrustworthy — every user must multi-sample against their own noise band.
5. **Single cheap-model subject**: main subject = MiMo-2.6 class; the diminishing gains (+6.25/+3.25/+0.5) are an n=2 pilot observation, not a verified conclusion.
6. **Environment-sensitive**: it took three full-batch reworks (tool contamination / old-file read leakage / agent-charter leakage) to get clean data — if the environment is not bare, the conclusions drift.
7. **Narrow domain coverage**: 4 domains, 24 tasks; other domains (e.g. pure translation, pure retrieval) untested.
8. **Self-optimization without a tester is not proven**, see section 5.

## 7. Usage advice (one-liner)

**Use**: generating ideas, writing plans, doing design, reviewing others' plans, planning — think-before-you-write tasks.
**Don't use**: finished prose (notes / abstracts / announcements), pure computation.
**Measure before use**: run the A/B in `selftune/` on your own 2 real tasks (≥3 samples, against your noise band); in 30 minutes you will know whether it helps you.
