# Calibration Probes (8 items, with difficulty gradient)

Purpose: in 10 minutes, map your model's strengths and weaknesses and produce a recommended clause config. **The difficulty gradient is deliberate** — all-right/all-wrong both mean the probes failed; just report "no discrimination" rather than forcing a profile.
Grading: against `scoring-key.json` (0/1 points per item + failure-mode tag). How to run: feed each item to the model in an independent context, take the answer text, grade manually/by machine against the scoring key.

## P1 (easy) fact checking
Material: a service's request volume Mar 1-3: 120/134/98, failures 2/1/5, v1.2 released Mar 2.
Q: answer in one sentence — which day had the highest failure rate? Show the calculation.
Key: Mar 3, 5/98≈5.1%, highest; don't confuse it with Mar 2 (1/134); **fabricating an "incident cause" from outside the material → tag FAB**.

## P2 (easy) boundary conditions
Write a function `first_even(nums)` returning the first even number; an empty list returns None.
Key: empty list / all odd / first element even / None or string raises TypeError (not silently); **failing to handle invalid input → tag BND**.

## P3 (easy) instruction following
"Introduce caching in exactly three sentences; you may not use the three words 'boost', 'empower', 'significant'; the third sentence must start with 'But'."
Key: sentence count = 3; zero occurrences of the three banned words; third sentence starts with "But"; **any violation → tag INS**.

## P4 (medium) statistical intuition
100 subjects each in A/B, A: 72 successes, B: 80 successes. Q: is A significantly worse? Give a conclusion and reasons (no need to compute a p-value).
Key: correct direction (8pp difference) but **must not claim significance** (no test/interval done); mention sample size or uncertainty; **claiming "significant" → tag STA**.

## P5 (medium) conflicting material
Material: ① 11/1 config sheet: backup daily, retain 7 days ② 11/10 production export: retain 3 days ③ goal: recovery ≤30 minutes ④ 11/12 drill: 47 minutes ⑤ proposal (not approved): hourly backups.
Q: state the status quo and the biggest risk in two sentences.
Key: keep "approved / actual / goal / proposal" distinct, don't mix them; point out the retention-period inconsistency or the recovery overtime; **treating the proposal as the status quo → tag CONF**.

## P6 (medium) code review
```python
def mean(xs):
    return sum(xs) / len(xs)
```
Q: point out two problems with this function in real use and give fixes.
Key: empty list ZeroDivisionError; non-numeric input; may raise mean semantics (integer division / floats); **only restating the code without problems → tag REV**.

## P7 (hard) confounded attribution
100 tasks each before/after an optimization launch: before (small 80×10ms, large 20×100ms), after (small 20×8ms, large 80×80ms). Q: did the optimization work?
Key: **must identify composition drift** (per-type means both down 20%, overall up 134% because the small/large proportion flipped); give a standardized figure (at original composition 22.4ms, down 20%); no causal/significance claims; **reporting only the overall number → tag SIMP (Simpson's trap)**.

## P8 (hard) falsifiability
"I propose: adding an 'outline first' prompt to the model will improve output quality." Q: design a minimal validation, and state what result would count as refuting it.
Key: control group (with/without outline) on the same tasks; scoring blind to condition; **predefine the refutation signal** (e.g. difference ≤0 or CI straddles 0); no falsifiable condition → tag FALS.

## Output profile format
```
Strengths: <P numbers and scores>
Weaknesses: <failure-mode tag distribution: FAB/BND/INS/STA/CONF/REV/SIMP/FALS>
Recommended clause config:
- Keep all clauses (default)
- If <tag> recurs -> add <corresponding reminder> to the task book (e.g. frequent STA: add "statistical conclusions must carry uncertainty" to the report-honestly clause)
Probe validity: whether the difficulty gradient separated (if all 8 right/wrong -> report "no discrimination", draw no profile conclusion)
```
