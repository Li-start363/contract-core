# contract-core + selftune

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**A lightweight "contract" layer that lifts cheap LLMs toward flagship-level performance on creative/research tasks — with a self-optimization kit and an honest failure map.**

一句话:给便宜模型套一份 5 条款「合同」(先出方案/排除平凡误判/写明可被推翻/禁编造/结果诚实),在创意类任务上把它抬到接近旗舰模型裸奔的水平——附自优化工具包与诚实的失效边界。

> Status: **experimental**. Evidence from ~200 controlled outputs (4-arm/5-arm × blind dual-judge, pre-registered). Not a guarantee — read the failure map below before use.

## Evidence(实测,2026-11)

| Task domain | Cheap model + contract vs flagship bare | Mechanism gain (contract − bare, cheap model) | Verdict |
|---|---|---|---|
| Research / creative ideas | within ~2.5–12 pts (two independent task sets) | **+17.7 / +9.0** (both non-trivial) | direction consistent; strict independent replication **not passed** |
| Engineering (code) | competitive | +6 ~ +28 (noisy; environment-sensitive) | reliability insurance in restricted sandboxes |
| Writing | −7.5 ~ −9.3 | negative | **stable failure boundary** |
| Data analysis | ≈0 | ≈0 | no gain (trivial) |

- 递减律(观察):模型越弱、合同吃得越多 — cheap +6.25 / mid +3.25 / frontier +0.5(pilot, n=2, exploratory only)。
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

## Failure map(诚实失效边界)

- 写作类任务:两组独立数据都显示**负增益**,不要用。
- 数据分析:无增益。
- 研究创意类:方向真实但幅度随任务族波动大(独立集严格门槛未过,单侧 95% CI 极宽)。
- 自优化"删条款变好"**未被证实**(G≈+0.9 < 噪声带):修剪需要可运行验证信号(测试器),纯文本证据不够。

## 安全与范围

- MIT license;no telemetry;runs fully local against your own model endpoint.
- Contract text is model-agnostic;换模型不换合同,换模型后重测增益(工具包自带标定)。

---

## 中文摘要

给便宜模型套 5 条款「合同核心」,在创意类任务上实测增益 +17.7/+9.0(两独立任务集,双盲双评,预注册),方向一致地逼近旗舰裸奔;写作域为负、数据域为零——失效边界如实公开。附自优化工具包(标定/A-B测量/修剪协议/坑注入/判据生成)与评测环境规范。实测警示:单样本评分噪声可达 ±50 分级,任何增益结论必须多采样并对照噪声带。
