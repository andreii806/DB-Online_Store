import mariadb
import bcrypt



DB_HOST = "127.0.0.1"
DB_PORT = 3307
DB_NAME = "inventory_magazin"
ROOT_USER = "root"
ROOT_PASS = "rootpass"



def get_root_connection():
    return mariadb.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=ROOT_USER,
        password=ROOT_PASS,
        database=DB_NAME
    )



def hash_password(plain: str) -> str:
    return bcrypt.hashpw(
        plain.encode(),
        bcrypt.gensalt()
    ).decode()



def create_db_users():
    conn = get_root_connection()
    cur = conn.cursor()

    db_users = [
        ("manager", "manager123", "ALL PRIVILEGES"),
        ("insert_user", "insert123", "SELECT, INSERT"),
        ("update_user", "update123", "SELECT, INSERT, UPDATE"),
        ("delete_user", "delete123", "SELECT, DELETE")
    ]

    for username, password, privileges in db_users:
        try:
            cur.execute(f"DROP USER IF EXISTS '{username}'@'%'")
            cur.execute(f"CREATE USER '{username}'@'%' IDENTIFIED BY '{password}'")
            cur.execute(f"GRANT {privileges} ON {DB_NAME}.* TO '{username}'@'%'")
            print(f"[OK] Created DB user: {username}")
        except Exception as e:
            print("Error:", e)

    cur.execute("FLUSH PRIVILEGES")
    conn.commit()
    conn.close()



def encrypt_app_users():
    conn = get_root_connection()
    cur = conn.cursor()

    cur.execute("SELECT id, password FROM users")
    rows = cur.fetchall()

    for user_id, pwd in rows:

        if not str(pwd).startswith("$2b$"):
            hashed = hash_password(pwd)
            cur.execute(
                "UPDATE users SET password=? WHERE id=?",
                (hashed, user_id)
            )
            print(f"[UPDATED] User ID {user_id} password encrypted")

    conn.commit()
    conn.close()



def main():
    print("\n=== CREATE DB USERS + GRANT ===")
    create_db_users()

    print("\n=== ENCRYPT APP USERS PASSWORDS ===")
    encrypt_app_users()

    print("\n SECURITY SETUP COMPLETED")

if __name__ == "__main__":
    main()