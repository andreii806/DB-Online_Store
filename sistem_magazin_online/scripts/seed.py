import random
from faker import Faker
from datetime import datetime, timedelta
from app.db import run_execute, run_select

fake = Faker()

NUM_USERS = 501
NUM_PRODUCTS = 501
NUM_MOVES = 501  # număr de ieșiri OUT (IN se face separat)
NUM_ORDERS = 501
MAX_ITEMS_PER_ORDER = 5

# --- USERS ---
print("Cream user admin fix")
run_execute(
    "INSERT INTO users (username, password, role) VALUES (%s, %s, %s);",
    ("admin", "admin123", "admin")
)

print(f"Generam {NUM_USERS - 1} utilizatori random cu parole simple")
simple_passwords = [
    "ananas", "parola123", "qwerty", "qwerty2024", "student123",
    "password", "abc123", "test123", "letmein", "maria2024"
]

simple_roles = ["admin", "client", "vanzator", "manager"]

for _ in range(NUM_USERS - 1):
    username = fake.user_name() + str(random.randint(1, 999))
    password = random.choice(simple_passwords)
    role = random.choice(simple_roles)
    run_execute(
        "INSERT INTO users (username, password, role) VALUES (%s, %s, %s);",
        (username, password, role)
    )

# --- PRODUCTS ---
print(f"Generam {NUM_PRODUCTS} produse cu SKU-uri compatibile")
categories = ["Laptop", "Mouse", "Monitor", "Cablu", "Tastatura"]

for i in range(1, NUM_PRODUCTS + 1):
    category = random.choice(categories)
    name = f"{category} {fake.company()}"
    sku = f"SKU-{i:03d}"
    price = random.randint(300, 9999)
    stock = random.randint(0, 100)
    run_execute(
        "INSERT INTO products (name, category, sku, price, stock) VALUES (%s, %s, %s, %s, %s);",
        (name, category, sku, price, stock)
    )

# --- INVENTORY MOVES (IN) ---
print("Initializam stoc (doar IN initial)")
products = run_select("SELECT id, stock FROM products;")
stock_tracker = {}

for product_id, stock in products:
    qty = random.randint(20, 200)
    stock_tracker[product_id] = qty
    run_execute(
        "INSERT INTO inventory_moves (product_id, qty, move_type) VALUES (%s, %s, %s);",
        (product_id, qty, "IN")
    )

# --- INVENTORY MOVES (OUT) ---
print(f"Simulam {NUM_MOVES} iesiri fara a depasi stocul")
for _ in range(NUM_MOVES):
    product_id = random.choice(list(stock_tracker.keys()))
    current_stock = stock_tracker[product_id]

    if current_stock > 0:
        qty = random.randint(1, min(10, current_stock))
        stock_tracker[product_id] -= qty
        run_execute(
            "INSERT INTO inventory_moves (product_id, qty, move_type) VALUES (%s, %s, %s);",
            (product_id, qty, "OUT")
        )

# --- ORDERS AND ORDER_ITEMS ---
print(f"Generam {NUM_ORDERS} comenzi random")
users = run_select("SELECT id FROM users;")
product_ids = [pid for pid, _ in products]

for _ in range(NUM_ORDERS):
    user_id = random.choice([u[0] for u in users])
    order_date = datetime.now() - timedelta(days=random.randint(0, 30))

    # Inserăm comanda și preluăm ID-ul ei
    order_id = run_execute(
        "INSERT INTO orders (user_id, order_date) VALUES (%s, %s);",
        (user_id, order_date),
    )

    num_items = random.randint(1, MAX_ITEMS_PER_ORDER)
    for _ in range(num_items):
        product_id = random.choice(product_ids)
        max_qty = min(stock_tracker.get(product_id, 0), 5)
        if max_qty == 0:
            continue
        qty = random.randint(1, max_qty)
        stock_tracker[product_id] -= qty
        run_execute(
            "INSERT INTO order_items (order_id, product_id, qty) VALUES (%s, %s, %s);",
            (order_id, product_id, qty)
        )

# --- USER LOG ---
print(f"Generam 501 loguri random pentru utilizatori")
actions = ["login", "logout", "placed_order", "updated_profile", "deleted_item"]

for _ in range(501):
    user_id = random.choice([u[0] for u in users])
    action = random.choice(actions)
    run_execute(
        "INSERT INTO user_log (user_id, action) VALUES (%s, %s);",
        (user_id, action)
    )

print("Date generate complet si corect pentru toate tabelele")
