# Evaluation Environment Spec (why and how to stay "bare")

Lesson from measurement (2026-11-18, earned by two full reworks): **one extra thing in the environment, one different result**.

## 1. Four contamination sources that must be isolated
| Contamination source | Measured symptom | Fix |
|---|---|---|
| Tools (write files / run commands) | Deliverable written to a file, grader sees only fragments → subjective misgrading, 0 points | Disable all tools for evaluation calls (e.g. `--disallowedTools ...`); deliverable = the answer text |
| Readable old files | Model reads back the previous output to "deliver", even claims "already verified in testing" | A brand-new empty working directory per cell |
| Agent charter / skills / hooks | Model follows a "don't write implementation" charter and goes to delegate → refusal, 0 points; output carries its own banner | Isolate the agent config directory (e.g. keep only login credentials in `CODEX_HOME`) |
| Shared cwd collisions | Cells overwrite each other's deliverable files | Independent empty directory per cell |

## 2. Refusal classification (score separately)
In restricted environments (read-only / no tools), failures come in two kinds and **must not be conflated**:
- **Environment-induced refusal**: "give me a writable environment / I cannot write to disk" — counts as delivery failure, but listed separately in the report and draws no capability conclusion;
- **Capability failure**: wrong content, missing main artifact, hallucinated delivery — scored normally.

## 3. Multi-sampling rule
Take ≥3 independent samples per arm for the same prompt. Report **mean ± same-contract noise band**. How to measure the noise band: run two arms with the identical contract text (content exactly the same); the distribution of score differences between the two arms is your floor; **any "improvement ≥10 points" verdict must clear the floor**.

## 4. Acceptance self-check (run these five before looking at scores)
- [ ] grep deliverables for refusal strings ("cannot write to disk / switch environment / delegate") = 0 hits or already listed separately
- [ ] grep deliverables for own banner / config paths = 0 hits
- [ ] no stray files in each cell directory besides the deliverable
- [ ] every anonymized item in the scoring JSON has a total (guards against "placeholder stub" sneaking in; occurred once in measurement)
- [ ] ΔQ conclusion compared against the noise band (no comparison = conclusion invalid)
