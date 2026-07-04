# test_final_state.py

import os
import json
import math
import pytest

def test_results_json():
    results_path = "/home/user/output/results.json"
    assert os.path.exists(results_path), f"File {results_path} does not exist. Ensure your program writes to the correct absolute path."

    with open(results_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON.")

    # Check for required keys
    expected_keys = {"time_us_f32", "time_us_f64", "max_abs_diff", "top_match_id"}
    missing_keys = expected_keys - set(results.keys())
    assert not missing_keys, f"Missing keys in results.json: {missing_keys}"

    # Validate types and basic constraints
    assert isinstance(results["time_us_f32"], int), "time_us_f32 must be an integer"
    assert results["time_us_f32"] > 0, "time_us_f32 must be greater than 0"

    assert isinstance(results["time_us_f64"], int), "time_us_f64 must be an integer"
    assert results["time_us_f64"] > 0, "time_us_f64 must be greater than 0"

    assert isinstance(results["max_abs_diff"], (float, int)), "max_abs_diff must be a float"
    assert isinstance(results["top_match_id"], int), "top_match_id must be an integer"

    # Compute expected top_match_id using standard library f64 math
    query_path = "/home/user/data/query.csv"
    db_path = "/home/user/data/database.csv"

    assert os.path.exists(query_path), "Query CSV missing, cannot verify correctness."
    assert os.path.exists(db_path), "Database CSV missing, cannot verify correctness."

    with open(query_path, 'r') as f:
        q_line = f.readline().strip().split(',')
        q_vec = [float(x) for x in q_line[1:]]

    top_id = -1
    max_sim = -2.0

    with open(db_path, 'r') as f:
        for line in f:
            parts = line.strip().split(',')
            if not parts or not parts[0]:
                continue
            id_val = int(parts[0])
            db_vec = [float(x) for x in parts[1:]]

            dot = sum(a * b for a, b in zip(q_vec, db_vec))
            norm_q = math.sqrt(sum(a * a for a in q_vec))
            norm_db = math.sqrt(sum(a * a for a in db_vec))

            sim = dot / (norm_q * norm_db)
            if sim > max_sim:
                max_sim = sim
                top_id = id_val

    assert results["top_match_id"] == top_id, f"Expected top_match_id {top_id}, got {results['top_match_id']}."

    # Check max_abs_diff is in a reasonable range for f32 vs f64 precision differences
    max_diff = results["max_abs_diff"]
    assert 0.0 <= max_diff <= 0.0001, f"max_abs_diff {max_diff} is out of the expected range (0.0 to 0.0001) for typical f32 vs f64 precision differences."