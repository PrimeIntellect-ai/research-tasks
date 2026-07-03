# test_final_state.py
import os
import json
import sqlite3
import pytest

DB_PATH = "/home/user/logistics.db"
BOTTLENECK_PATH = "/home/user/bottleneck.txt"
QUERY_PATH = "/home/user/query.sql"
JSON_PATH = "/home/user/expensive_deliveries.json"

def test_bottleneck_file():
    assert os.path.exists(BOTTLENECK_PATH), f"File missing: {BOTTLENECK_PATH}"
    with open(BOTTLENECK_PATH, "r") as f:
        content = f.read().strip()
    assert content == "Central_Sort", f"Expected bottleneck to be 'Central_Sort', but got '{content}'"

def test_sql_query_file():
    assert os.path.exists(QUERY_PATH), f"File missing: {QUERY_PATH}"
    with open(QUERY_PATH, "r") as f:
        content = f.read().upper()
    assert "OVER" in content or "WINDOW" in content, "The SQL query must use a Window Function (OVER or WINDOW clause)."

def test_expensive_deliveries_json():
    assert os.path.exists(JSON_PATH), f"File missing: {JSON_PATH}"

    # Derive the expected result from the database
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    query = """
    WITH ValidDeliveries AS (
        SELECT 
            d.delivery_id,
            n1.region_code,
            d.cost,
            n1.name as source_name,
            n2.name as dest_name
        FROM t3_z d
        JOIN t1_x n1 ON d.src_id = n1.id
        JOIN t1_x n2 ON d.dst_id = n2.id
        JOIN t2_y e ON d.src_id = e.source_id AND d.dst_id = e.target_id
        WHERE e.distance > 100
    ),
    RankedDeliveries AS (
        SELECT *,
               ROW_NUMBER() OVER(PARTITION BY region_code ORDER BY cost DESC, delivery_id ASC) as rn
        FROM ValidDeliveries
    )
    SELECT delivery_id, region_code, cost, source_name, dest_name
    FROM RankedDeliveries
    WHERE rn <= 2
    ORDER BY region_code ASC, cost DESC
    """

    c.execute(query)
    expected_rows = [dict(row) for row in c.fetchall()]
    conn.close()

    with open(JSON_PATH, "r") as f:
        try:
            actual_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_PATH} is not valid JSON.")

    assert isinstance(actual_data, list), f"Expected JSON to be a list, got {type(actual_data)}"
    assert len(actual_data) == len(expected_rows), f"Expected {len(expected_rows)} deliveries, but got {len(actual_data)}"

    for i, (actual, expected) in enumerate(zip(actual_data, expected_rows)):
        assert actual.get("delivery_id") == expected["delivery_id"], f"Row {i}: Expected delivery_id {expected['delivery_id']}, got {actual.get('delivery_id')}"
        assert actual.get("region_code") == expected["region_code"], f"Row {i}: Expected region_code {expected['region_code']}, got {actual.get('region_code')}"
        assert float(actual.get("cost")) == float(expected["cost"]), f"Row {i}: Expected cost {expected['cost']}, got {actual.get('cost')}"
        assert actual.get("source_name") == expected["source_name"], f"Row {i}: Expected source_name {expected['source_name']}, got {actual.get('source_name')}"
        assert actual.get("dest_name") == expected["dest_name"], f"Row {i}: Expected dest_name {expected['dest_name']}, got {actual.get('dest_name')}"