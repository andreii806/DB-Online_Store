import json
from app.db import get_connection, run_select

print("ORDER SERVICE")

user_id = run_select("SELECT id FROM users WHERE username=%s;", ("admin",))[0][0]

items = [
    {"sku": "SKU-001", "qty": 1},
    {"sku": "SKU-002", "qty": 2},
    {"sku": "SKU-003", "qty": 3},
]
items_json = json.dumps(items)

print("Apelam procedura create_order...")

conn = get_connection()
cur = conn.cursor()

try:
    cur.execute("CALL create_order(%s, %s);", (user_id, items_json))

    row = cur.fetchone()
    order_id = row[0]

    while cur.nextset():
        if cur.description is not None:
            cur.fetchall()

    conn.commit()
    print("OK: Comanda creata. order_id =", order_id)

finally:
    cur.close()
    conn.close()

print("\nVerificare in DB (order_items):")
rows = run_select("""
SELECT oi.order_id, p.sku, p.name, oi.qty
FROM order_items oi
JOIN products p ON p.id = oi.product_id
WHERE oi.order_id = %s
ORDER BY p.sku;
""", (order_id,))

for r in rows:
    print(r)