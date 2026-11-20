# Pruning Protocol (criteria before results)

When to use: you have finished an A/B (see `ab_runner.py`), have the ΔQ report in hand, and want the contract to fit your scenario better.
Iron rule: **the criteria below take effect before you see the re-test results, and must not be changed afterward**. Changing the criteria = that round is void, start over.

## 1. Pruning criteria (frozen)
1. **Deletable modules only**: plan first / rule out trivial explanations / falsifiable·stop-loss. "No fabrication" and "report honestly" are fixed and cannot be deleted.
2. **Evidence threshold for deletion**: for each candidate module, evidence with a locatable position must be given in **≥2 tasks**:
   - task conflict (the clause's requirement directly contradicts the task's requirement)
   - extra-action error (an error introduced by an extra action taken because of the clause)
   - delivery-budget loss (clause content squeezed out the length/structure the task required)
3. **Delete-only, no additions**: M1 must be exactly the full text of M0 with some clauses removed. Adding task answers, adding domain hints, rewording — all count as overreach; the round is void.
4. **No evidence → keep**; record "no pruning" in the pruning table. This is a **valid result**, not a failure.
5. **Re-test**: compare M1 against M0 on the same batch of fresh tasks (≥3 samples/arm), G = Q(M1)−Q(M0); **G must exceed your noise band** to count as an improvement. Getting better on the dev set alone does not count.

## 2. Pruning table template
```
| Module | Verdict (keep/drop) | Evidence (task id + position in the original text; write "none" if absent) |
|---|---|---|
| Plan first | | |
| Rule out trivial explanations | | |
| Falsifiable·stop-loss | | |
| No fabrication | keep (fixed) | — |
| Report honestly | keep (fixed) | — |
```

## 3. Failure signals (any one = the round is invalid)
- the pruning table is blank or no verdict was made;
- "no fabrication"/"report honestly" was deleted;
- new content outside the original contract appears in M1;
- criteria or M1 were changed after seeing the re-test scores;
- when self-scoring contradicts the mechanical test's conclusion, the test is taken as authoritative yet the conclusion follows the self-score.

## 4. Measured reference (2026-11-18)
Two unfamiliar models each ran one round: one found compliant evidence and deleted "falsifiable·stop-loss" (two out-of-scope "if the spec later…" assumptions ate into delivery space), re-test G≈+0.9 (below the noise band, no gain); the other ruled "no pruning". Conclusion: **pruning can be done, but the gain has to be shown by the re-test — don't expect deleting clauses to automatically make things better**.
