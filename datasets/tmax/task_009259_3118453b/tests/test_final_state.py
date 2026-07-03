# test_final_state.py

import os
import json
import math
import pytest

JSON_PATH = "/home/user/movement_summary.json"
LOG_PATH = "/home/user/pipeline.log"

def test_movement_summary_json():
    assert os.path.isfile(JSON_PATH), f"JSON file {JSON_PATH} does not exist. The C++ program may not have run or failed to create it."

    with open(JSON_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {JSON_PATH} is not valid JSON.")

    assert "matched_drones" in data, "Key 'matched_drones' missing in JSON."
    assert "average_distance" in data, "Key 'average_distance' missing in JSON."
    assert "max_distance_id" in data, "Key 'max_distance_id' missing in JSON."

    assert data["matched_drones"] == 3, f"Expected 3 matched_drones, got {data['matched_drones']}"
    assert data["max_distance_id"] == "D05", f"Expected max_distance_id 'D05', got {data['max_distance_id']}"
    assert math.isclose(data["average_distance"], 5.0, rel_tol=1e-2), f"Expected average_distance around 5.0, got {data['average_distance']}"

def test_pipeline_log():
    assert os.path.isfile(LOG_PATH), f"Log file {LOG_PATH} does not exist."

    with open(LOG_PATH, "r") as f:
        log_content = f.read()

    expected_lines = [
        "[INFO] Read 4 records from t1",
        "[INFO] Read 5 records from t2",
        "[INFO] Computed distances for 3 drones",
        "[INFO] Results written to JSON"
    ]

    for line in expected_lines:
        assert line in log_content, f"Expected log line '{line}' not found in {LOG_PATH}"