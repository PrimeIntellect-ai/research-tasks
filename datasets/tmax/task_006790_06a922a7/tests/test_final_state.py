# test_final_state.py
import os
import json
import sqlite3
import csv
import pytest

def get_expected_data():
    db_path = "/home/user/data/sales.sqlite"
    csv_path = "/home/user/data/customers.csv"

    # Read customers
    customers = {}
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            customers[int(row["customer_id"])] = {
                "customer_id": int(row["customer_id"]),
                "full_name": f"{row['first_name']} {row['last_name']}",
                "region": row["region"],
                "active_orders": []
            }

    # Read orders
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Window function to get latest order
    query = """
    WITH RankedOrders AS (
        SELECT 
            order_id, 
            customer_id, 
            amount, 
            status,
            ROW_NUMBER() OVER (PARTITION BY order_id ORDER BY updated_at DESC) as rn
        FROM order_history
    )
    SELECT order_id, customer_id, amount, status
    FROM RankedOrders
    WHERE rn = 1 AND status != 'CANCELLED'
    """

    cursor.execute(query)
    for row in cursor.fetchall():
        cid = row["customer_id"]
        if cid in customers:
            customers[cid]["active_orders"].append({
                "order_id": row["order_id"],
                "amount": float(row["amount"]),
                "status": row["status"]
            })

    conn.close()

    # Format output
    final_customers = []
    for cid in sorted(customers.keys()):
        if customers[cid]["active_orders"]:
            customers[cid]["active_orders"].sort(key=lambda x: x["order_id"])
            final_customers.append(customers[cid])

    return {"customers": final_customers}

def test_output_file_exists():
    output_path = "/home/user/output/active_orders.json"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

def test_output_json_content():
    output_path = "/home/user/output/active_orders.json"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

    with open(output_path, "r", encoding="utf-8") as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse JSON from {output_path}: {e}")

    expected_data = get_expected_data()

    assert "customers" in actual_data, "The JSON object must have a 'customers' key."

    # Compare structure
    assert len(actual_data["customers"]) == len(expected_data["customers"]), \
        f"Expected {len(expected_data['customers'])} customers, but got {len(actual_data['customers'])}."

    for expected_c, actual_c in zip(expected_data["customers"], actual_data["customers"]):
        assert actual_c.get("customer_id") == expected_c["customer_id"], "Customer ID mismatch or missing."
        assert actual_c.get("full_name") == expected_c["full_name"], "Full name mismatch or missing."
        assert actual_c.get("region") == expected_c["region"], "Region mismatch or missing."

        expected_orders = expected_c["active_orders"]
        actual_orders = actual_c.get("active_orders", [])

        assert len(actual_orders) == len(expected_orders), \
            f"Expected {len(expected_orders)} active orders for customer {expected_c['customer_id']}, got {len(actual_orders)}."

        for expected_o, actual_o in zip(expected_orders, actual_orders):
            assert actual_o.get("order_id") == expected_o["order_id"], "Order ID mismatch."
            assert actual_o.get("status") == expected_o["status"], "Order status mismatch."
            # Allow some float tolerance or exact match
            assert float(actual_o.get("amount", 0)) == float(expected_o["amount"]), "Order amount mismatch."