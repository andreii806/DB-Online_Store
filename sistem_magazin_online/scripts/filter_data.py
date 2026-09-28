import json
from pathlib import Path
from app.db import run_select

MIN_STOCK = 99

sql = """
SELECT
    p.sku,
    p.name,
    COALESCE(SUM(CASE WHEN m.move_type='IN' THEN m.qty ELSE -m.qty END), 0) AS stock
FROM products p
LEFT JOIN inventory_moves m ON m.product_id = p.id
GROUP BY p.id, p.sku, p.name
HAVING stock >= %s
ORDER BY stock DESC;
"""

rows = run_select(sql, (MIN_STOCK,))

data = []
for r in rows:
    data.append({
        "sku": r[0],
        "name": r[1],
        "stock": int(r[2])
    })

out_path = Path("outputs") / "products_stock_filtered.json"
out_path.write_text(
    json.dumps({
        "min_stock": MIN_STOCK,
        "results": data
    }, indent=2, ensure_ascii=False),
    encoding="utf-8"
)

print(f"JSON salvat: {out_path}")
