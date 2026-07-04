# test_final_state.py

import os
import time
import sqlite3
import requests
import pytest

def test_server_ready_file():
    ready_file = "/home/user/server_ready"
    # Wait up to 5 seconds for the file to exist
    for _ in range(50):
        if os.path.exists(ready_file):
            break
        time.sleep(0.1)

    assert os.path.isfile(ready_file), f"Server ready file missing at {ready_file}"
    with open(ready_file, 'r') as f:
        content = f.read().strip()
    assert "READY" in content.upper(), f"Server ready file does not contain 'READY', got: {content}"

def test_vendored_framework_fixed():
    server_file = "/app/vendored_microframe/server.py"
    assert os.path.isfile(server_file), f"Server file missing at {server_file}"
    with open(server_file, 'r') as f:
        content = f.read()

    assert "split('&')" in content or 'split("&")' in content, f"The bug in {server_file} does not appear to be fixed (should split on '&')."
    assert "split(';')" not in content and 'split(";")' not in content, f"The bug in {server_file} is still present (splitting on ';')."

def test_database_indexes():
    db_path = "/home/user/ecommerce.db"
    assert os.path.isfile(db_path), f"Database file missing at {db_path}"

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name IN ('idx_product_category', 'idx_order_items_product');")
    indexes = {row[0] for row in cursor.fetchall()}
    conn.close()

    assert 'idx_product_category' in indexes, "Index 'idx_product_category' is missing."
    assert 'idx_order_items_product' in indexes, "Index 'idx_order_items_product' is missing."

def test_api_endpoint():
    # Wait for server to be actually listening
    url = "http://127.0.0.1:8080/api/top_customers?category=Electronics&limit=2"

    response = None
    for _ in range(50):
        try:
            response = requests.get(url, timeout=1)
            break
        except requests.RequestException:
            time.sleep(0.1)

    assert response is not None, f"Failed to connect to the server at {url}"
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"
    assert "application/json" in response.headers.get("Content-Type", ""), "Expected Content-Type to be application/json"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response is not valid JSON")

    assert isinstance(data, list), "Expected JSON response to be a list"

    if len(data) > 0:
        for item in data:
            assert "customer_name" in item, "Missing 'customer_name' in response item"
            assert "total_spend" in item, "Missing 'total_spend' in response item"
            assert isinstance(item["total_spend"], (int, float)), "Expected 'total_spend' to be a number"

    assert len(data) <= 2, f"Expected at most 2 items, got {len(data)}"