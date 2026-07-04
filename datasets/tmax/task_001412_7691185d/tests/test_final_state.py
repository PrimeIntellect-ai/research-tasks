# test_final_state.py

import os
import sqlite3
import json
import pytest

DB_PATH = "/home/user/ecommerce.db"
SCRIPT_PATH = "/home/user/export_backup.py"
BACKUP_PATH = "/home/user/backup_data.json"

def get_expected_data():
    """Derive the expected JSON structure directly from the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Get all customers who have at least one completed order
    cursor.execute("""
        SELECT DISTINCT c.id, c.name, c.email
        FROM customers c
        JOIN orders o ON c.id = o.customer_id
        WHERE o.status = 'completed'
        ORDER BY c.id ASC
    """)
    customers = cursor.fetchall()

    expected_output = []

    for cust in customers:
        cust_id = cust['id']

        # Get completed orders for this customer
        cursor.execute("""
            SELECT id, order_date
            FROM orders
            WHERE customer_id = ? AND status = 'completed'
            ORDER BY id ASC
        """, (cust_id,))
        orders = cursor.fetchall()

        orders_list = []
        total_spent = 0.0

        for ord_row in orders:
            order_id = ord_row['id']

            # Get items for this order
            cursor.execute("""
                SELECT product_name, price
                FROM items
                WHERE order_id = ?
                ORDER BY product_name ASC
            """, (order_id,))
            items = cursor.fetchall()

            items_list = []
            for item in items:
                items_list.append({
                    "product_name": item['product_name'],
                    "price": float(item['price'])
                })
                total_spent += float(item['price'])

            orders_list.append({
                "order_id": order_id,
                "order_date": ord_row['order_date'],
                "items": items_list
            })

        expected_output.append({
            "customer_id": cust_id,
            "name": cust['name'],
            "email": cust['email'],
            "total_spent": total_spent,
            "orders": orders_list
        })

    conn.close()
    return expected_output

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} does not exist."

def test_backup_file_exists():
    assert os.path.isfile(BACKUP_PATH), f"The backup file {BACKUP_PATH} does not exist."

def test_backup_data_content_and_format():
    assert os.path.isfile(BACKUP_PATH), f"The backup file {BACKUP_PATH} does not exist."

    with open(BACKUP_PATH, 'r') as f:
        raw_content = f.read()

    try:
        actual_data = json.loads(raw_content)
    except json.JSONDecodeError:
        pytest.fail(f"The file {BACKUP_PATH} does not contain valid JSON.")

    expected_data = get_expected_data()

    # Check structure and values
    assert actual_data == expected_data, "The JSON data does not match the expected output derived from the database."

    # Check formatting (indentation)
    # The prompt asks for "properly formatted and indented (2 spaces)"
    expected_raw = json.dumps(expected_data, indent=2)
    assert raw_content.strip() == expected_raw.strip(), "The JSON file is not properly formatted with 2 spaces indentation."