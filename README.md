# Contract Core — lift cheap LLMs to flagship level on creative tasks

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**A 5-clause prompt "contract" that makes cheap models think before they write — measured across ~200 controlled outputs, with a self-optimization kit and an honest failure map.**

一句话:给便宜模型套一份 5 条款「合同」(先出方案/排除平凡误判/写明可被推翻/禁编造/结果诚实),在创意类任务上把它抬到接近旗舰模型裸奔的水平——附自优化工具包与诚实的失效边界。

> Status: **experimental**. Evidence from ~200 controlled outputs (4-arm/5-arm × blind dual-judge, pre-registered). Not a guarantee — read the failure map below before use.

## Evidence(实测,2026-11)

| Task domain | Cheap model + contract vs flagship bare | Mechanism gain (contract − bare, cheap model) | Verdict |
|---|---|---|---|
| Research / creative ideas | within ~2.5–12 pts (two independent task sets) | **+17.7 / +9.0** (both non-trivial) | direction consistent; strict independent replication **not passed** |
| Engineering (code) | competitive (per-item spread −75.5…+92.5) | +6.0 (set A, below +10 threshold); code-task mechanical scores saturated at 100/100 | reliability insurance in restricted sandboxes (qualitative); mechanism gain **not established** |
| Writing | −9.3 / −7.5 (both sets) | −7.0 (set A) / +1.3 (set B) — **not reliable** | **failure boundary**: no reliable gain, and the lifted model still trails flagship bare on both sets |
| Data analysis | −4.7 (set A) / +7.3 (set B) | +1.7 / +3.3 (below +10 threshold) | no useful gain; (the earlier ≈0 figure referred to information-synthesis tasks, old S-set, ≈0 there) |

- 递减律(观察):模型越弱、合同吃得越多 — cheap +6.25 / mid +3.25 / frontier +0.5(pilot, n=2, exploratory only)。

  ![Diminishing contract gain (pilot, n=2, exploratory): cheap +6.25 / mid +3.25 / frontier +0.5](assets/gain_curve.png)
- ⚠️ Measurement noise is large (same-contract twin runs can differ by ±50 judged points): **always multi-sample and compare against your noise floor** (built into `selftune/`).

```
┌─────────────────────────────────────────────┐
│  contracts/contract-core.md   ← the 5 clauses │
│        │                                      │
│        ▼                                      │
│  your agent runtime (hook / system prompt)    │
│        │                                      │
│        ▼                                      │
│  selftune/  ← measure, prune, inject pitfalls │
│    calibrate → A/B → prune → pitfalls → criteria│
└─────────────────────────────────────────────┘
```

## 30 秒上手

```bash
# 1) 把 contracts/contract-core.md 拼进你的任务提示前缀
# 2) 跑一次 A/B(每臂 ≥3 采样)
python3 selftune/ab_runner.py --tasks my_tasks/ \
  --engine 'claude -p < {prompt}' --samples 3 --out runs/
# 3) 打分后出 ΔQ 报告(对照噪声带)
python3 selftune/ab_runner.py --analyze runs/ --scores scores.json
```

端到端示例(5 分钟):`examples/`。

## 自优化工具包(selftune/,五件)

| Piece | File | What it does |
|---|---|---|
| Calibrator | `selftune/calibrate/` | 8 probes with difficulty gradient → capability profile + recommended clause config |
| A/B runner | `selftune/ab_runner.py` | paired bare/contract runs, ≥3 samples/arm, ΔQ with noise band |
| Pruning protocol | `selftune/修剪协议.md` | delete-clause rules with ≥2-locatable-evidence threshold (judged before results) |
| Pitfall injector | `selftune/pitfall_inject.py` | your lessons → standard pitfall entries → hook injection |
| Criteria generator | `selftune/判据生成器.md` | falsification-triple template (threshold / degradation plan / refuse-to-judge) |

**三条硬规则**(实测换来的):评测环境必须裸(`selftune/评测环境规范.md`)、必须多采样对照噪声带、修剪必须有可定位证据。

## Where it helps / where it hurts(优势与局限,详见 [docs/applicability-map.md](docs/applicability-map.md))

**Strengths(实测)**:creative/research/design tasks get a real, non-trivial lift(+17.7/+9.0 on two independent sets)——contract scaffolding targets exactly that domain's failure modes(wishful reasoning, fabrication, unfalsifiable claims);in restricted sandboxes it doubles as delivery-reliability insurance;weakest models benefit most(递减律观察)。

**Limitations(如实,全部实测)**:
- **Writing/final-deliverable prose: no reliable gain (−7.0 / +1.3 across two sets), and the lifted model still trails flagship bare (−9.3 / −7.5)——don't use it there.** The scaffolding eats the deliverable's budget and reads as boilerplate.
- Data/computation tasks: no useful gain (mechanism +1.7 / +3.3, below threshold; information-synthesis ≈0)。
- Research lift is direction-consistent but **strict independent replication did not pass**(claim scoped accordingly;CI very wide at n=3/domain)。
- Self-optimization via clause-pruning is **not proven**(G≈+0.9 < noise floor)——pruning needs runnable tests, not text evidence。
- Measurement noise is large(±50 pts scale on twin runs):single-sample conclusions are worthless。
- LLM-as-judge(跨族双评缓解未消除)、单一 cheap-model 主体、域覆盖 4 类、评测环境必须裸(三次整批返工的教训)。

**One-liner**: use it for think-before-you-write tasks(ideas/plans/designs/reviews);don't use it for finished prose or pure computation;measure on your own tasks first(selftune, 30 min)。

## 安全与范围

- MIT license;no telemetry;runs fully local against your own model endpoint.
- Contract text is model-agnostic;换模型不换合同,换模型后重测增益(工具包自带标定)。

---

## 中文摘要

给便宜模型套 5 条款「合同核心」,在创意类任务上实测增益 +17.7/+9.0(两独立任务集,双盲双评,预注册),方向一致地逼近旗舰裸奔;写作域为负、数据域为零——失效边界如实公开。附自优化工具包(标定/A-B测量/修剪协议/坑注入/判据生成)与评测环境规范。实测警示:单样本评分噪声可达 ±50 分级,任何增益结论必须多采样并对照噪声带。
