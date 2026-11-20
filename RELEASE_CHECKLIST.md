# Release checklist (set 2026-11-16; push only when all green)
## Paper-data gates
- [x] Set S: 40 scorings complete, paired ΔQ table produced (2026-11-20: external working-tree evidence "old-line ΔQ summary, set S" — file lives in the private working tree, original filename non-ASCII; 40 rows 0 missing; conclusion = no gain on information synthesis, set C saturated, claim already narrowed)
- [x] Claim tier chosen per the downgrade table, diminishing gains rewritten as observation-level (H4 confirmation report final-tier wording; README/applicability-map both at observation-level)
- [x] Three-way comparison ("past 50%") conclusion given (2026-11-20: external working-tree evidence "three-way publication-probability comparison, 2026-11-20" — file lives in the private working tree, original filename non-ASCII; 3/3 agree, none past 50%, goal changed to "submittable, reusable, presentable")
## Repository gates
- [x] README (English): architecture diagram + diminishing-gain data plot + 30-second quick start (2026-11-20 recheck: ASCII architecture diagram and 30-second quick start already present; gain_curve.png was not referenced before, passed after embedding it this time)
- [x] 3 contract templates (core / idea pack / task book) generalized, no research-specific jargon (2026-11-20 recheck: contracts/contract-core.md + template-idea-pack.md + template-task-book.md)
- [x] Sanitized batch runner + smoke test runnable (2026-11-20 recheck: selftune/ab_runner.py; examples/run_demo.sh ran end-to-end with fake engine at zero cost, ΔQ report normal)
- [x] Pitfall library, 28 entries, sanitized (paths / machines / accounts removed) (2026-11-20 recheck: knowledge/pitfalls-general.md count exactly 28)
- [x] Pre-registration template + downgrade-table example (2026-11-20 recheck: templates/preregistration.md contains "3. Downgrade table (frozen)")
- [x] examples/ minimal reproducible demo (end-to-end in 5 minutes) (2026-11-20 recheck: run_demo.sh ran through)
- [x] Sanitization recheck: grep proper nouns / paths / accounts = 0 (2026-11-20 recheck: /Users/, ll-player, sk-/tp- key shapes, AutoDL, 127.0.0.1 all zero hits repo-wide (except .git))
- [x] Clean git history, LICENSE, README badges (2026-11-20 recheck: LICENSE (MIT) present, badges present, commit messages semantically readable)
## Gate rule
Any item not green = no push (contract core: rules before results). The push is performed by the user.
