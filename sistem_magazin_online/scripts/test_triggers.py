from app.db import run_execute, run_select

print("TEST TRIGGER BEFORE INSERT (inventory_moves)")

product_id = run_select("SELECT id FROM products LIMIT 1;")[0][0]

print("Inserare valida (qty = 5)")
try:
    run_execute(
        sql="INSERT INTO inventory_moves (product_id, qty, move_type) VALUES (%s, %s, %s);",
        params=(product_id, 5, "IN")
    )
    print("OK: Inserarea valida a reusit")
except Exception as e:
    print("EROARE (nu trebuia):", e)


print("\nInserare invalida (qty = -3)")
try:
    run_execute(
        sql="INSERT INTO inventory_moves (product_id, qty, move_type) VALUES (%s, %s, %s);",
        params=(product_id, -3, "IN")
    )
    print("EROARE: Inserarea invalida a trecut (trigger NU functioneaza)")
except Exception as e:
    print("OK: Inserarea invalida a fost respinsa de trigger")
    print("Mesaj DB:", e)


print("\nTEST TRIGGER AFTER UPDATE (products)")
print("Facem update pe produs")

run_execute(
    sql="UPDATE products SET name=%s WHERE id=%s;",
    params=("PRODUS TEST UPDATE", product_id)
)

print("Verificam log-urile")

logs = run_select(
    "SELECT action FROM user_log ORDER BY id DESC LIMIT 3;"
)

for l in logs:
    print("-", l[0])


print("\nTEST TRIGGERE FINALIZAT")
