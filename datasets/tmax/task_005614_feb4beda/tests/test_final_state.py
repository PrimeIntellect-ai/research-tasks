# test_final_state.py
import os
import json
import sqlite3

def test_results_json_exists_and_correct():
    json_path = "/home/user/results.json"
    assert os.path.exists(json_path), f"Output file {json_path} is missing."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} does not contain valid JSON."

    assert isinstance(data, list), f"JSON root must be an array, got {type(data)}."
    assert len(data) == 3, f"Expected exactly 3 objects in JSON array, got {len(data)}."

    expected_data = [
        {"experiment_name": "Exp_10", "total_value": 737.58},
        {"experiment_name": "Exp_20", "total_value": 732.12},
        {"experiment_name": "Exp_18", "total_value": 718.59}
    ]

    for i, expected in enumerate(expected_data):
        actual = data[i]
        assert "experiment_name" in actual, f"Object at index {i} missing 'experiment_name' key."
        assert "total_value" in actual, f"Object at index {i} missing 'total_value' key."
        assert actual["experiment_name"] == expected["experiment_name"], \
            f"Expected experiment_name '{expected['experiment_name']}' at index {i}, got '{actual['experiment_name']}'."
        assert round(actual["total_value"], 2) == expected["total_value"], \
            f"Expected total_value {expected['total_value']} at index {i}, got {actual['total_value']}."

def test_python_script_exists_and_contains_reindex():
    script_path = "/home/user/process_research.py"
    assert os.path.exists(script_path), f"Python script {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    assert "REINDEX" in content.upper(), "The Python script does not appear to contain the REINDEX command to fix the corruption."

def test_index_exists():
    db_path = "/home/user/research.db"
    assert os.path.exists(db_path), f"Database file {db_path} is missing."

    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='index';")
    indices = {row[0] for row in c.fetchall()}
    conn.close()

    assert "idx_opt_samples" in indices, "The required index 'idx_opt_samples' was not created in the database."