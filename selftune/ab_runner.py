#!/usr/bin/env python3
# A/B runner: your tasks × {bare, contract} × ≥3 samples → ΔQ report (with noise band)
# Usage:
#   python3 ab_runner.py --tasks tasks/ --engine 'claude -p < {prompt} > {output}' --samples 3 --out runs/
#   python3 ab_runner.py --analyze runs/ --scores scores.json
# Discipline (evaluation-environment.md): brand-new empty cwd per cell; the engine side must disable tools / isolate config itself; refusal artifacts are kept and listed separately in the report.
import argparse, json, os, random, subprocess, time

def load_tasks(d):
    tasks = {}
    for f in sorted(os.listdir(d)):
        if f.endswith((".txt", ".md")):
            tasks[os.path.splitext(f)[0]] = open(os.path.join(d, f), encoding="utf-8").read()
    return tasks

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tasks"); ap.add_argument("--engine")
    ap.add_argument("--contract", default=os.path.join(os.path.dirname(__file__), "..", "contracts", "contract-core.md"))
    ap.add_argument("--samples", type=int, default=3)
    ap.add_argument("--out", default="runs/")
    ap.add_argument("--seed", type=int, default=20261118)
    ap.add_argument("--analyze"); ap.add_argument("--scores")
    a = ap.parse_args()

    if a.analyze:
        scores = json.load(open(a.scores))
        # scores format: {"task_arm_sample": score, "control_bare_sample": score, "control_contract_sample": score}
        agg = {}
        for k, v in scores.items():
            if k.startswith("_"):
                continue
            t, arm, *_ = k.split("_")
            agg.setdefault((t, arm), []).append(v)
        rows = []
        for (t, arm), vs in sorted(agg.items()):
            rows.append((t, arm, round(sum(vs)/len(vs), 1), len(vs)))
        noise = scores.get("_noise_band")
        print("ΔQ report")
        print("| Task | Arm | Mean | Samples |")
        print("|---|---|---|---|")
        for r in rows: print(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |")
        for t in sorted({r[0] for r in rows}):
            m = {arm: v for (tt, arm), v in [((x[0], x[1]), x[2]) for x in rows] if tt == t}
            if "contract" in m and "bare" in m:
                dq = round(m["contract"] - m["bare"], 1)
                verdict = "≥ noise band" if noise and dq > noise else ("below noise band" if noise else "noise band not measured")
                print(f"- {t}: ΔQ={dq} ({verdict})")
        if noise: print(f"Noise band (same-contract control): {noise}")
        return

    tasks = load_tasks(a.tasks)
    contract = open(a.contract, encoding="utf-8").read()
    os.makedirs(a.out, exist_ok=True)
    jobs = []
    for t in tasks:
        for arm in ("bare", "contract"):
            for s in range(a.samples):
                jobs.append((t, arm, s))
    random.Random(a.seed).shuffle(jobs)
    man = open(os.path.join(a.out, "manifest.jsonl"), "a", encoding="utf-8")
    for t, arm, s in jobs:
        prompt = (contract + "\n\n【Task】\n" if arm == "contract" else "") + tasks[t]
        cell = os.path.join(a.out, "cells", f"{t}_{arm}_{s}")
        os.makedirs(cell, exist_ok=True)
        pf = os.path.join(cell, "prompt.txt"); open(pf, "w", encoding="utf-8").write(prompt)
        of = os.path.join(cell, "output.txt")
        cmd = a.engine.format(prompt=pf, output=of)
        t0 = time.time()
        with open(of, "wb") as fo, open(os.path.join(cell, "stderr.txt"), "wb") as fe:
            rc = subprocess.run(["/bin/bash", "-c", cmd], stdout=fo, stderr=fe, cwd=cell).returncode
        man.write(json.dumps({"task": t, "arm": arm, "sample": s, "rc": rc,
                              "sec": round(time.time()-t0, 1),
                              "bytes": os.path.getsize(of)}, ensure_ascii=False) + "\n")
        man.flush()
        print(f"{t}_{arm}_{s} rc={rc} {os.path.getsize(of)}B", flush=True)
    print("AB_RUN_DONE")

if __name__ == "__main__":
    main()
