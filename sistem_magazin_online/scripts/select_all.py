import json
from pathlib import Path
from app.db import run_select

sql = """
SELECT
    p.id,
    p.name,
    p.sku,
    COALESCE(SUM(CASE WHEN m.move_type='IN' THEN m.qty ELSE -m.qty END), 0) AS stock
FROM products p
LEFT JOIN inventory_moves m ON m.product_id = p.id
GROUP BY p.id, p.name, p.sku
ORDER BY p.sku;
"""

rows = run_select(sql)

data = []
for r in rows:
    data.append({
        "id": r[0],
        "name": r[1],
        "sku": r[2],
        "stock": int(r[3]) if r[3] is not None else 0
    })

out_path = Path("outputs") / "products_with_stock.json"
out_path.parent.mkdir(exist_ok=True)

out_path.write_text(
    json.dumps(data, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(f"JSON salvat: {out_path}")
