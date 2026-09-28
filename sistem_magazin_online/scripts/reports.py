import json
import csv
import matplotlib.pyplot as plt

from pathlib import Path
from decimal import Decimal
from datetime import datetime

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch

from app.db import run_select


OUT_DIR = Path("outputs")
OUT_DIR.mkdir(exist_ok=True)

LOGO_PATH = Path("scripts/logo_fiir.jpg")

def normalize(v):
    if isinstance(v, Decimal):
        x = float(v)
        return int(x) if x.is_integer() else x
    return v


def export_csv(data, path, fieldnames):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerows(data)


def export_json(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def generate_chart(data, labels_key, values_key, title, chart_path):

    labels = [str(d[labels_key]) for d in data]
    values = [d[values_key] for d in data]

    plt.figure(figsize=(8, 5))

    plt.bar(labels, values)

    plt.title(title)
    plt.xlabel(labels_key)
    plt.ylabel(values_key)

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig(str(chart_path))

    plt.close()


def generate_pdf(
    title,
    subtitle,
    intro_text,
    data,
    columns,
    chart_path,
    pdf_path
):

    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)

    elements = []

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        name="TitleStyle",
        parent=styles["Heading1"],
        fontSize=18,
        spaceAfter=20
    )

    normal_style = styles["Normal"]

    if LOGO_PATH.exists():

        logo = Image(
            str(LOGO_PATH),
            width=1.5 * inch,
            height=1.5 * inch
        )

        elements.append(logo)
        elements.append(Spacer(1, 20))

    elements.append(Paragraph(title, title_style))

    elements.append(Spacer(1, 10))

    elements.append(Paragraph(subtitle, styles["Heading2"]))

    elements.append(Spacer(1, 15))

    elements.append(Paragraph(intro_text, normal_style))

    elements.append(Spacer(1, 20))

    table_data = [columns]

    for d in data:

        row = [d[col] for col in columns]

        table_data.append(row)

    table = Table(table_data, colWidths=[180] * len(columns))

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#ecf0f1")),

        ("ALIGN", (0, 0), (-1, -1), "CENTER")
    ]))

    elements.append(table)

    elements.append(Spacer(1, 25))

    if chart_path.exists():

        chart = Image(
            str(chart_path),
            width=6 * inch,
            height=4 * inch
        )

        elements.append(chart)

    doc.build(elements)


def report_top_products():

    sql = """
    SELECT
        p.name,
        SUM(oi.qty) AS total_qty
    FROM order_items oi
    JOIN products p
        ON p.id = oi.product_id
    GROUP BY p.id, p.name
    ORDER BY total_qty DESC
    """

    rows = run_select(sql)

    data = [
        {
            "Produs": r[0],
            "Cantitate": normalize(r[1])
        }
        for r in rows
    ]

    base_name = "Top_Produse_Vandute"

    csv_path = OUT_DIR / f"{base_name}.csv"
    json_path = OUT_DIR / f"{base_name}.json"
    pdf_path = OUT_DIR / f"{base_name}.pdf"
    chart_path = OUT_DIR / f"{base_name}_chart.png"

    # CSV
    export_csv(
        data,
        csv_path,
        ["Produs", "Cantitate"]
    )

    export_json(data, json_path)

    generate_chart(
        data,
        "Produs",
        "Cantitate",
        "Top produse vandute",
        chart_path
    )

    intro = f"""
    Raport BI pentru analiza produselor vandute.

    Date agregate folosind functia SUM().

    Raport generat la:
    {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    """

    generate_pdf(
        "Raport Business Intelligence",
        "Top Produse Vandute",
        intro,
        data,
        ["Produs", "Cantitate"],
        chart_path,
        pdf_path
    )


def report_orders_per_customer():

    sql = """
    SELECT
        u.username,
        COUNT(DISTINCT o.id) AS total_orders,
        SUM(oi.qty) AS total_products
    FROM orders o
    JOIN users u
        ON u.id = o.user_id
    JOIN order_items oi
        ON oi.order_id = o.id
    GROUP BY u.id, u.username
    ORDER BY total_products DESC
    """

    rows = run_select(sql)

    data = [
        {
            "Client": r[0],
            "Numar_Comenzi": normalize(r[1]),
            "Produse_Comandate": normalize(r[2])
        }
        for r in rows
    ]

    base_name = "Comenzi_Clienti"

    csv_path = OUT_DIR / f"{base_name}.csv"
    json_path = OUT_DIR / f"{base_name}.json"
    pdf_path = OUT_DIR / f"{base_name}.pdf"
    chart_path = OUT_DIR / f"{base_name}_chart.png"

    export_csv(
        data,
        csv_path,
        ["Client", "Numar_Comenzi", "Produse_Comandate"]
    )

    export_json(data, json_path)

    generate_chart(
        data,
        "Client",
        "Produse_Comandate",
        "Produse comandate per client",
        chart_path
    )

    intro = f"""
    Raport BI pentru analiza comenzilor per client.

    Date agregate folosind functiile COUNT() si SUM().

    Raport generat la:
    {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    """

    generate_pdf(
        "Raport Business Intelligence",
        "Comenzi Per Client",
        intro,
        data,
        ["Client", "Numar_Comenzi", "Produse_Comandate"],
        chart_path,
        pdf_path
    )


def main():

    report_top_products()

    report_orders_per_customer()

    print("Toate rapoartele au fost generate in:")
    print(OUT_DIR.resolve())


if __name__ == "__main__":
    main()