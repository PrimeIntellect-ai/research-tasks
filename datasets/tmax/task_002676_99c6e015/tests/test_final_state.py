# test_final_state.py

import os
import json
import math
import pytest

def test_transfer_plan_exists():
    plan_path = "/home/user/transfer_plan.json"
    assert os.path.isfile(plan_path), f"Expected output file {plan_path} is missing. The script did not generate it."

def test_transfer_plan_content():
    plan_path = "/home/user/transfer_plan.json"
    if not os.path.isfile(plan_path):
        pytest.fail(f"Cannot test content because {plan_path} is missing.")

    try:
        with open(plan_path, "r") as f:
            plan = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"The file {plan_path} does not contain valid JSON.")

    # Validate structure based on schema
    assert isinstance(plan, dict), "The top-level JSON structure must be an object (dictionary)."
    assert "backup_name" in plan, "Missing 'backup_name' in the transfer plan."
    assert "path" in plan, "Missing 'path' in the transfer plan."
    assert "total_time_ms" in plan, "Missing 'total_time_ms' in the transfer plan."

    # Validate values
    assert plan["backup_name"] == "auth_db_snapshot_2023", \
        f"Expected backup_name to be 'auth_db_snapshot_2023', got {plan.get('backup_name')}"

    expected_path = ["us-east-1", "eu-west-1", "ap-northeast-1"]
    assert plan["path"] == expected_path, \
        f"Expected path to be {expected_path}, got {plan.get('path')}. Check your pathfinding logic and edge weights."

    expected_time = 36896.666666666664
    actual_time = plan["total_time_ms"]
    assert isinstance(actual_time, (int, float)), "total_time_ms must be a number."

    # Allow a small epsilon for floating point differences
    assert math.isclose(actual_time, expected_time, abs_tol=0.1), \
        f"Expected total_time_ms to be approximately {expected_time}, got {actual_time}. " \
        "Ensure edge weights are calculated as: latency_ms + (size_mb / bandwidth_mbps) * 1000."