from app.db import run_execute, run_select

print("Inseram utilizatori")
run_execute(
    "INSERT INTO users (username, password, role) VALUES (%s, %s, %s);",
    ("admin1", "hash_admin", "admin")
)
run_execute(
    "INSERT INTO users (username, password, role) VALUES (%s, %s, %s);",
    ("client1", "hash_client", "client")
)

print("Inseram produse")
run_execute(
    "INSERT INTO products (name, category, sku, price, stock) VALUES (%s, %s, %s, %s, %s);",
    ("Laptop Lenovo", "LAPTOP",  "SKU-001", 2999, 10)
)
run_execute(
    "INSERT INTO products (name, category, sku, price, stock) VALUES (%s, %s, %s, %s, %s);",
    ("Mouse Logitech", "MOUSE", "SKU-002", 500, 3)
)

print("Inseram miscari")

p1 = run_select(
    "SELECT id FROM products WHERE sku=%s;",
    ("SKU-001",)
)[0][0]

p2 = run_select(
    "SELECT id FROM products WHERE sku=%s;",
    ("SKU-002",)
)[0][0]

run_execute(
    "INSERT INTO inventory_moves (product_id, qty, move_type) VALUES (%s, %s, %s);",
    (p1, 10, "IN")
)
run_execute(
    "INSERT INTO inventory_moves (product_id, qty, move_type) VALUES (%s, %s, %s);",
    (p1, 2, "OUT")
)
run_execute(
    "INSERT INTO inventory_moves (product_id, qty, move_type) VALUES (%s, %s, %s);",
    (p2, 50, "IN")
)

print("Inseram log-uri")

admin_id = run_select(
    "SELECT id FROM users WHERE username=%s;",
    ("admin1",)
)[0][0]

run_execute(
    "INSERT INTO user_log (user_id, action) VALUES (%s, %s);",
    (admin_id, "REBUILD_DB")
)
run_execute(
    "INSERT INTO user_log (user_id, action) VALUES (%s, %s);",
    (admin_id, "INSERT_DATE")
)

print("Datele au fost inserate cu succes!")
