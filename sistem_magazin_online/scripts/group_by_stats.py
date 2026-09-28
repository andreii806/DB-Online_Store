import json
from pathlib import Path
from app.db import run_select

sql = """
SELECT
    m.move_type,
    COUNT(*) AS moves_count,
    AVG(m.qty) AS avg_qty
FROM inventory_moves m
GROUP BY m.move_type
ORDER BY moves_count ASC;
"""

rows = run_select(sql)

data = []
for r in rows:
    data.append({
        "move_type": r[0],
        "moves_count": int(r[1]),
        "avg_qty": float(r[2]) if r[2] is not None else 0.0
    })

out_path = Path("outputs") / "moves_stats.json"
out_path.write_text(
    json.dumps(data, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(f"JSON salvat: {out_path}")
