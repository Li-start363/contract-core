#!/usr/bin/env bash
# 端到端示例:假引擎跑 A/B → 假打分 → ΔQ 报告。不耗模型额度。
set -euo pipefail
cd "$(dirname "$0")"
SELF="../selftune/ab_runner.py"

# 1) 跑 2 臂 × 3 采样(假引擎:直接输出固定文本)
python3 "$SELF" --tasks tasks --engine 'printf "demo-answer"' --samples 3 --out runs_demo

# 2) 用假打分演示分析(真用时换成你的评分 JSON)
python3 "$SELF" --analyze runs_demo --scores scores.json

echo ""
echo "结论样式:ΔQ 高于噪声带(5 分)= 有证据;低于噪声带 = 判'无证据',加采样或上机械判据。"
