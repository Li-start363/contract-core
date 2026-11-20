# General engineering pitfall library (28 entries, sanitized)

> Distilled from hundreds of measured runs; when dispatching a task book / ruleset, pick 3~8 entries by topic and inject them. Each entry = symptom + how to prevent it.

## Machine runs / batch execution
1. Scripts must never contain any form of auto-shutdown / scheduled shutdown / shutdown fallback — when done, just report "ready to shut down"; a human decides when.
2. Size concurrency on a 0.75 VRAM budget and on peak, not steady state; small parameter count ≠ low VRAM use (activations can differ 4×).
3. Extrapolate ETA from measurements, not theory; editing a script mid-run = mixed old/new runs — stop first, then edit.
4. File transfer: globs expand on the remote side and silently drop files; always double-check both sides after transfer (e.g. md5); speed-test before uploading instead of memorizing a fixed number.

## Shell / scripts
5. Backgrounding a heredoc loses its content; in `A && B & C` the precedence eats the cd/file write.
6. pkill/pgrep -f self-matching kills your own process — use exact PIDs or the [m]atch bracket trick only.
7. Quote breakpoints: for complex inline scripts, write to a file instead; module-level constants are fixed at import time, so changing environment variables mid-run has no effect.
8. Never edit a running script (the in-memory version and the disk version go out of sync).
9. scp/transfer globs do not expand; use a tar pipe or transfer file by file.

## Assertions / acceptance
10. Never trust a script's own *_DONE/ALL_DONE/BUILD_OK; trust only the artifacts (exists + non-zero bytes + all fields present + numbers match the criteria).
11. Criteria must match a string unique to the verdict, guarding against always-true greps (a scoring regex once matched noise lines like "score: 60").
12. Before saying "all / none / 0 remaining", run grep/find first and state the search scope.
13. The three elements of a disk-write claim: machine + absolute path + byte count; without write-back evidence you may not say "written".
14. Failures must be visible (write *_FAILED); silent continuation is forbidden.

## Hooks / configuration layer
15. Hook failures are silent: heartbeat (proves it ran) + smoke test (proves it did the right thing) + explicit declaration — triple self-verification; hook timeouts are fail-open.
16. Some agent frameworks' hooks trust by command string: changing the command = silently skipped; put the logic in a new script and keep the old path as a trampoline.
17. New CLI flags swallow positional arguments (e.g. --disallowedTools swallowing the prompt): feeding the prompt via stdin is the most stable route.

## Evaluation / experiment design
18. Data-split leakage (per-item split) can drop 98% to 40%; controls must use the same split; data splitting and the evaluation protocol are the biggest disaster areas.
19. Rule out trivial explanations before evaluating: scale/normalization differences, confidence-interval width, pseudoreplication (shared data source counted as independent samples).
20. Seeds and initialization order affect replication; fixing the seed is not enough — fix the initialization order too.
21. Figure font size is back-derived as natural size × natural width / layout width; changing the layout requires updating the font-size constant in step.

## LLM evaluation pitfalls (measured in this repository)
22. **The evaluation environment must be bare**: tools present → the deliverable gets written to a file and the grader sees only fragments; old files present → the model reads them back to "deliver"; agent charter/skills present → the model refuses and goes to "delegate". Empty cwd per cell + tools disabled + isolated config.
23. Classify refusals: "give me a writable environment" = environment-induced refusal; "wrong content / missing main artifact" = capability failure. Score them separately, list them separately in the report.
24. Score differences between two runs of the same prompt can reach the ±50 level: single-sample ΔQ is untrustworthy; ≥3 samples per arm, measured against the noise band.
25. LLM grading occasionally produces "placeholder stub" void papers (self-reports "to be overwritten"): verify the papers, re-grade void papers once, keep the raw record.
26. Judge-family bias: the judge must not be the producer; cross-family dual judging + disagreement annotation.
27. Generation calls must set a timeout: a hung API stream waits forever (measured: same prompt hung 32 minutes straight); timeout = transport failure, retry a limited number of times.
28. When grepping processes, don't write a hyphen-joined string: "claude -p" gets separated by `--settings ...` and slips through; match broadly by process name, and falsify your own checker first.
