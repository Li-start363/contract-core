# examples:端到端 5 分钟示例

演示 selftune 全流程(用假引擎,不耗你的模型额度):

```bash
cd examples
bash run_demo.sh
```

脚本会:
1. 用 `tasks/` 里的 2 道样题,以假引擎(`printf` 模拟模型)跑 2 臂 × 3 采样;
2. 用 `scores.json`(预先假定的打分)演示 ΔQ 报告与噪声带对照;
3. 打印结论样式(含"低于噪声带则判无证据")。

接真模型:把 `run_demo.sh` 里的 `--engine` 换成你的调用命令即可,例如:
- `--engine 'claude -p < {prompt}'`
- `--engine 'codex exec --sandbox read-only -m <model> < {prompt}'`

⚠️ 真跑前读 `../selftune/评测环境规范.md`(逐格空 cwd、禁工具、隔离 agent 配置、≥3 采样)。
