# test_final_state.py
import os
import sqlite3
import json
import pytest

DB_PATH = "/home/user/db_perf/sales.db"
INDEX_SQL_PATH = "/home/user/db_perf/indexes.sql"
CPP_PATH = "/home/user/db_perf/aggregator.cpp"
EXE_PATH = "/home/user/db_perf/aggregator"
JSON_PATH = "/home/user/db_perf/regional_summary.json"

def test_indexes_created():
    assert os.path.isfile(INDEX_SQL_PATH), f"File {INDEX_SQL_PATH} is missing."

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='index'")
    indexes = [row[0] for row in c.fetchall() if not row[0].startswith('sqlite_')]
    conn.close()

    assert len(indexes) > 0, "No custom indexes found in the database. You must apply the indexes."

def test_cpp_files_exist():
    assert os.path.isfile(CPP_PATH), f"C++ source file missing at {CPP_PATH}."
    assert os.path.isfile(EXE_PATH), f"Compiled executable missing at {EXE_PATH}."
    assert os.access(EXE_PATH, os.X_OK), f"File {EXE_PATH} is not executable."

def test_json_output():
    assert os.path.isfile(JSON_PATH), f"JSON output missing at {JSON_PATH}."

    with open(JSON_PATH, 'r') as f:
        try:
            agent_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_PATH} is not valid JSON.")

    assert isinstance(agent_data, list), "JSON root must be a list."

    # Calculate truth
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT u.region, p.category, SUM(oi.quantity * oi.price), COUNT(DISTINCT o.id)
        FROM users u
        JOIN orders o ON u.id = o.user_id
        JOIN order_items oi ON o.id = oi.order_id
        JOIN products p ON oi.product_id = p.id
        WHERE o.status = 'COMPLETED'
        GROUP BY u.region, p.category
    """)

    truth_data = {}
    for region, category, rev, count in c.fetchall():
        if region not in truth_data:
            truth_data[region] = {}
        truth_data[region][category] = {"revenue": round(rev, 2), "order_count": count}
    conn.close()

    # Check sorting of regions
    regions_in_json = [obj.get("region") for obj in agent_data]
    assert regions_in_json == sorted(regions_in_json), "Regions in JSON are not sorted alphabetically."

    for region_obj in agent_data:
        r = region_obj.get("region")
        assert r in truth_data, f"Unexpected region '{r}' in output."

        categories = region_obj.get("categories", [])
        assert isinstance(categories, list), f"'categories' for region '{r}' must be a list."

        cats_in_json = [cat.get("category") for cat in categories]
        assert cats_in_json == sorted(cats_in_json), f"Categories in region '{r}' are not sorted alphabetically."

        for cat_obj in categories:
            c_name = cat_obj.get("category")
            assert c_name in truth_data[r], f"Unexpected category '{c_name}' in region '{r}'."

            truth_rev = truth_data[r][c_name]["revenue"]
            agent_rev = cat_obj.get("revenue", 0)
            assert abs(truth_rev - agent_rev) < 0.1, f"Revenue mismatch for {r}-{c_name}. Expected {truth_rev}, got {agent_rev}."

            truth_cnt = truth_data[r][c_name]["order_count"]
            agent_cnt = cat_obj.get("order_count", 0)
            assert truth_cnt == agent_cnt, f"Order count mismatch for {r}-{c_name}. Expected {truth_cnt}, got {agent_cnt}."

        # Ensure all categories for this region are present
        assert len(categories) == len(truth_data[r]), f"Missing categories in region '{r}'."

    # Ensure all regions are present
    assert len(agent_data) == len(truth_data), "Missing regions in the JSON output."