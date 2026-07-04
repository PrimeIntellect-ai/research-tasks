# test_final_state.py
import os
import json
import sqlite3
import pytest
from collections import defaultdict

RAW_DATA_PATH = '/home/user/raw_data/orders.json'
DB_PATH = '/home/user/ecommerce.db'
SUMMARY_PATH = '/home/user/summary.json'

def get_expected_data():
    if not os.path.isfile(RAW_DATA_PATH):
        pytest.fail(f"Raw data file {RAW_DATA_PATH} is missing.")

    with open(RAW_DATA_PATH, 'r') as f:
        orders = json.load(f)

    users = {}
    products = {}
    order_records = {}
    order_items = []

    category_user_spent = defaultdict(lambda: defaultdict(float))

    for order in orders:
        o_id = order['order_id']
        u = order['user']
        u_id = u['user_id']

        users[u_id] = u
        order_records[o_id] = {
            'order_id': o_id,
            'user_id': u_id,
            'order_date': order['order_date']
        }

        for item in order['items']:
            p = item['product']
            p_id = p['product_id']
            qty = item['quantity']

            products[p_id] = p
            order_items.append({
                'order_id': o_id,
                'product_id': p_id,
                'quantity': qty
            })

            category_user_spent[p['category']][u['name']] += p['price'] * qty

    expected_summary = []
    for category, user_spent in category_user_spent.items():
        # sort by spent desc, then name asc for tie-breaking
        sorted_users = sorted(user_spent.items(), key=lambda x: (-x[1], x[0]))
        top_user_name, top_spent = sorted_users[0]
        expected_summary.append({
            "category": category,
            "top_user_name": top_user_name,
            "total_spent_by_top_user": round(top_spent, 2)
        })

    expected_summary.sort(key=lambda x: x['category'])

    return users, products, order_records, order_items, expected_summary

def test_db_exists():
    assert os.path.isfile(DB_PATH), f"Database file {DB_PATH} is missing. The ETL script did not create it."

def test_db_tables_and_counts():
    users, products, order_records, order_items, _ = get_expected_data()

    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        c.execute("SELECT count(*) FROM users")
        assert c.fetchone()[0] == len(users), "Incorrect number of rows in 'users' table. Did you deduplicate properly?"

        c.execute("SELECT count(*) FROM products")
        assert c.fetchone()[0] == len(products), "Incorrect number of rows in 'products' table. Did you deduplicate properly?"

        c.execute("SELECT count(*) FROM orders")
        assert c.fetchone()[0] == len(order_records), "Incorrect number of rows in 'orders' table."

        c.execute("SELECT count(*) FROM order_items")
        assert c.fetchone()[0] == len(order_items), "Incorrect number of rows in 'order_items' table."

    except sqlite3.OperationalError as e:
        pytest.fail(f"SQLite OperationalError: {e}. Ensure all required tables are created with the correct schemas.")
    finally:
        conn.close()

def test_summary_json():
    assert os.path.isfile(SUMMARY_PATH), f"Summary file {SUMMARY_PATH} is missing. The report script did not create it."

    _, _, _, _, expected_summary = get_expected_data()

    with open(SUMMARY_PATH, 'r') as f:
        try:
            actual_summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{SUMMARY_PATH} is not valid JSON.")

    assert isinstance(actual_summary, list), "summary.json must contain a JSON array at the root level."
    assert len(actual_summary) == len(expected_summary), f"Expected {len(expected_summary)} categories in summary.json, but got {len(actual_summary)}."

    for i in range(len(expected_summary)):
        expected = expected_summary[i]
        actual = actual_summary[i]

        assert actual.get("category") == expected["category"], f"Expected category '{expected['category']}' at index {i}. Ensure the array is sorted alphabetically by category."
        assert actual.get("top_user_name") == expected["top_user_name"], f"Expected top_user_name '{expected['top_user_name']}' for category '{expected['category']}'. Check your tie-breaking logic."
        assert isinstance(actual.get("total_spent_by_top_user"), float), f"total_spent_by_top_user for '{expected['category']}' must be a float."
        assert round(actual.get("total_spent_by_top_user"), 2) == expected["total_spent_by_top_user"], f"Expected total_spent_by_top_user {expected['total_spent_by_top_user']} for category '{expected['category']}'."