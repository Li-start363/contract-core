#!/usr/bin/env python3
# 配对测量器:你的任务 × {裸, 机制} × ≥3 采样 → ΔQ 报告(带噪声带)
# 用法:
#   python3 ab_runner.py --tasks tasks/ --engine 'claude -p < {prompt} > {output}' --samples 3 --out runs/
#   python3 ab_runner.py --analyze runs/ --scores scores.json
# 纪律(评测环境规范):每格全新空 cwd;引擎侧自行禁工具/隔离配置;拒答产物保留并在报告单列。
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
        # scores 结构: {"task_arm_sample": 分数, "control_bare_sample": 分, "control_contract_sample": 分}
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
        print("ΔQ 报告")
        print("| 任务 | 臂 | 均值 | 采样数 |")
        print("|---|---|---|---|")
        for r in rows: print(f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |")
        for t in sorted({r[0] for r in rows}):
            m = {arm: v for (tt, arm), v in [((x[0], x[1]), x[2]) for x in rows] if tt == t}
            if "contract" in m and "bare" in m:
                dq = round(m["contract"] - m["bare"], 1)
                verdict = "≥噪声带" if noise and dq > noise else ("低于噪声带" if noise else "噪声带未测")
                print(f"- {t}: ΔQ={dq} ({verdict})")
        if noise: print(f"噪声带(同合同对照): {noise}")
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
        prompt = (contract + "\n\n【任务】\n" if arm == "contract" else "") + tasks[t]
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
