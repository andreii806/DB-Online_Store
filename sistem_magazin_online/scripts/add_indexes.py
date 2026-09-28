import time
from app.db import run_execute

def apply_indexes():
    print("=== APLICARE INDEX PENTRU OPTIMIZARE===")

    index_queries = [
        "CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);",
        "CREATE INDEX IF NOT EXISTS idx_products_name ON products(name);"
    ]

    for query in index_queries:
        print(f"Rulam: {query}")
        try:
            start_time = time.time()
            run_execute(query)
            end_time = time.time()
            duration = (end_time - start_time) * 1000
            print(f"-> Succes! (Durata creare: {duration:.2f} ms)\n")
        except Exception as e:
            print(f"-> Eroare la crearea indexului: {e}\n")

    print("Indexuri aplicate cu succes.")
    print("-----------------------------------------------")


if __name__ == "__main__":
    apply_indexes()
