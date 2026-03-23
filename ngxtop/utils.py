import sys
import json
import tabulate
import yaml
from typing import List, Dict

# =========================
# 核心转换
# =========================
def to_records(headers: List[str], rows: List[List]) -> List[Dict]:
    return [dict(zip(headers, row)) for row in rows]

# =========================
# 各种 Renderer
# =========================
def render_table(headers, rows):
    return tabulate.tabulate(rows, headers=headers, tablefmt='orgtbl', floatfmt='.2f')
def render_markdown(headers, rows):
    return tabulate.tabulate(rows, headers=headers, tablefmt="github", floatfmt='.2f')

def render_vertical(headers, rows):
    lines = []
    width = max(len(h) for h in headers)

    for i, row in enumerate(rows, 1):
        lines.append(f"--- record {i} ---")
        for k, v in zip(headers, row):
            lines.append(f"  {k.ljust(width)} : {v}")
        lines.append("")

    return "\n".join(lines)

def render_json(headers, rows):
    records = to_records(headers, rows)
    return json.dumps(records, indent=2, ensure_ascii=False)

def render_yaml(headers, rows):
    records = to_records(headers, rows)
    return yaml.dump(records, allow_unicode=True, sort_keys=False, width=4096, default_flow_style=False)

def render_tsv(headers, rows):
    lines = ["\t".join(headers)]
    for row in rows:
        lines.append("\t".join(str(x) for x in row))
    return "\n".join(lines)

# =========================
# 渲染分发器（核心）
# =========================
RENDERERS = {
    "table": render_table,
    "vertical": render_vertical,
    "json": render_json,
    "yaml": render_yaml,
    "tsv": render_tsv,
    "md": render_markdown,
}

def render(headers, rows, fmt="table"):
    if fmt not in RENDERERS:
        raise ValueError(f"Unsupported format: {fmt}")
    return RENDERERS[fmt](headers, rows)

def choose_one(choices, prompt):
    for idx, choice in enumerate(choices):
        print('%d. %s' % (idx + 1, choice))
    selected = None
    if sys.version[0] == '3':
        raw_input = input
    while not selected or selected <= 0 or selected > len(choices):
        selected = raw_input(prompt)
        try:
            selected = int(selected)
        except ValueError:
            selected = None
    return choices[selected - 1]


def error_exit(msg, status=1):
    sys.stderr.write('Error: %s\n' % msg)
    sys.exit(status)
