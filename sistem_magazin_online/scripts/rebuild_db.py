from app.db import run_execute
from scripts.create_tables import create_tables

print("Stergem tabelele existente (daca exista)")

run_execute("DROP TABLE IF EXISTS order_items;")
run_execute("DROP TABLE IF EXISTS inventory_moves;")
run_execute("DROP TABLE IF EXISTS user_log;")
run_execute("DROP TABLE IF EXISTS orders;")
run_execute("DROP TABLE IF EXISTS products;")
run_execute("DROP TABLE IF EXISTS users;")

print("Creez tabelele din schema sql...")
create_tables()

print("Rebuild gata!")
