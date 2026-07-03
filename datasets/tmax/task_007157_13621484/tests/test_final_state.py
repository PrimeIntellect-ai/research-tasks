# test_final_state.py
import os
import json
import sqlite3
import subprocess

def test_extract_script_exists_and_runs():
    script_path = "/home/user/extract.py"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"extract.py failed to execute. Error:\n{result.stderr}"

def test_results_json():
    json_path = "/home/user/results.json"
    assert os.path.exists(json_path), f"File {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} is not valid JSON."

    assert isinstance(results, list), "Results should be a JSON array."
    assert len(results) == 15, f"Expected exactly 15 records for page 2, found {len(results)}."

    # Recompute the truth
    db_path = "/home/user/research.db"
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    query = """
    SELECT 
        s.id as sample_id, 
        l.name as location_name, 
        r.name as researcher_name, 
        s.collection_date, 
        MAX(m.value) as max_carbon
    FROM samples s
    JOIN locations l ON s.location_id = l.id
    JOIN researchers r ON s.researcher_id = r.id
    JOIN measurements m ON s.id = m.sample_id
    WHERE s.type = 'ice_core' 
      AND l.region = 'Polar' 
      AND m.metric_name = 'carbon_ppm'
    GROUP BY s.id, l.name, r.name, s.collection_date
    ORDER BY max_carbon DESC, s.collection_date ASC
    LIMIT 15 OFFSET 15
    """

    cur.execute(query)
    expected_rows = [dict(row) for row in cur.fetchall()]
    conn.close()

    # Check keys and values
    for i, (actual, expected) in enumerate(zip(results, expected_rows)):
        assert "sample_id" in actual, f"Missing 'sample_id' in record {i}"
        assert "location_name" in actual, f"Missing 'location_name' in record {i}"
        assert "researcher_name" in actual, f"Missing 'researcher_name' in record {i}"
        assert "collection_date" in actual, f"Missing 'collection_date' in record {i}"
        assert "max_carbon" in actual, f"Missing 'max_carbon' in record {i}"

        assert actual["sample_id"] == expected["sample_id"], f"Record {i} sample_id mismatch: {actual['sample_id']} != {expected['sample_id']}"
        assert actual["location_name"] == expected["location_name"], f"Record {i} location_name mismatch."
        assert actual["researcher_name"] == expected["researcher_name"], f"Record {i} researcher_name mismatch."
        assert actual["collection_date"] == expected["collection_date"], f"Record {i} collection_date mismatch."
        assert abs(actual["max_carbon"] - expected["max_carbon"]) < 1e-5, f"Record {i} max_carbon mismatch."

def test_query_plan_and_indexes():
    plan_path = "/home/user/plan.txt"
    assert os.path.exists(plan_path), f"File {plan_path} does not exist."

    with open(plan_path, "r") as f:
        plan_content = f.read()

    assert "USING INDEX" in plan_content or "USING COVERING INDEX" in plan_content, "Query plan does not indicate index usage. Ensure you created appropriate indexes and prepended EXPLAIN QUERY PLAN to your exact query."

    # Verify custom indexes exist in DB
    db_path = "/home/user/research.db"
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'")
    indexes = cur.fetchall()
    conn.close()

    assert len(indexes) > 0, "No custom indexes found in the database. You must create indexes to optimize the query."