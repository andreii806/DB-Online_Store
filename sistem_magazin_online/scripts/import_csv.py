import csv
from pathlib import Path

from app.db import get_connection
from scripts.export_csv import ALLOWED_TABLES

AUTO_SKIP_COLS = {"id", "created_at", "move_time"}


def get_table_columns(cur, table: str) -> set[str]:
    cur.execute(f"DESCRIBE {table};")
    return {row[0] for row in cur.fetchall()}


def import_table_from_csv(table: str, csv_path: Path, truncate_first: bool = False):
    table = table.strip()

    if table not in ALLOWED_TABLES:
        raise ValueError(f"Tabel invalid. Alege din: {sorted(ALLOWED_TABLES)}")

    if not csv_path.exists():
        raise FileNotFoundError(f"Nu exista CSV: {csv_path}")

    conn = get_connection()
    cur = conn.cursor()

    inserted = 0
    skipped = 0

    try:
        table_cols = get_table_columns(cur, table)

        if truncate_first:
            cur.execute(f"TRUNCATE TABLE {table};")

        with csv_path.open("r", encoding="utf-8", newline="") as f:
            reader = csv.DictReader(f)

            if not reader.fieldnames:
                raise ValueError("CSV invalid: lipseste header-ul.")

            cols = []
            for c in reader.fieldnames:
                c = c.strip()
                if c in AUTO_SKIP_COLS:
                    continue
                if c in table_cols:
                    cols.append(c)

            if not cols:
                raise ValueError(
                    "Nu am coloane importabile (header-ul nu corespunde tabelului)."
                )

            placeholders = ", ".join(["%s"] * len(cols))
            col_list = ", ".join(cols)

            sql = f"INSERT INTO {table} ({col_list}) VALUES ({placeholders});"

            for row in reader:
                values = []
                empty_row = True

                for c in cols:
                    val = row.get(c)

                    if val is None:
                        val = ""

                    val = val.strip()

                    if val != "":
                        empty_row = False

                    values.append(val if val != "" else None)

                if empty_row:
                    skipped += 1
                    continue

                cur.execute(sql, tuple(values))
                inserted += 1

        conn.commit()
        print(f"IMPORT OK -> table={table}, inserted={inserted}, skipped={skipped}")

    except Exception as e:
        conn.rollback()
        print("IMPORT FAIL -> rollback. Eroare:", e)
        raise

    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    table = input(f"Tabel ({', '.join(sorted(ALLOWED_TABLES))}): ").strip()
    path = input("CSV path (ex: exports/products.csv): ").strip()
    truncate = input("TRUNCATE inainte? (y/n): ").strip().lower() == "y"

    import_table_from_csv(table, Path(path), truncate_first=truncate)
