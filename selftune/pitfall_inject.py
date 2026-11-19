#!/usr/bin/env python3
# 坑注入器:把你的踩坑记录转成标准坑库条目 + hook 注入片段
# 用法:python3 pitfall_inject.py 我的踩坑.md >> 坑库.md
# 输入格式宽松:任意 markdown,含"标题/现象/根因/怎么防"任意几段即可
import sys, re, datetime

def section(text, *names):
    for n in names:
        m = re.search(rf"(?:^|\n)#+\s*{n}[^\n]*\n(.*?)(?=\n#+\s|\Z)", text, re.S)
        if m: return m.group(1).strip()
    return ""

def main():
    raw = open(sys.argv[1], encoding="utf-8").read()
    title = (re.search(r"^#\s*(.+)$", raw, re.M) or [None, sys.argv[1]])[1].strip()
    symptom = section(raw, "现象", "症状", "问题") or raw.split("\n", 1)[1][:200]
    cause = section(raw, "根因", "原因") or "【待补】"
    fix = section(raw, "怎么防", "预防", "解法", "对策") or "【待补】"
    today = datetime.date.today().isoformat()
    entry = f"""
## {title}({today})
- 现象:{symptom[:300]}
- 根因:{cause[:300]}
- 怎么防:{fix[:300]}
"""
    inject = f"- 【坑】{title[:60]}:{fix[:120]}"
    print(entry)
    print("---hook 注入片段(粘进任务书/守则末尾)---")
    print(inject)

if __name__ == "__main__":
    main()
