# test_final_state.py

import os
import json
import subprocess
import pytest

SCRIPT_PATH = "/home/user/route_optimizer.py"
OUTPUT_PATH = "/home/user/optimal_route.json"

def run_script(start_node, end_node, max_cost):
    """Helper to run the student's script."""
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)

    result = subprocess.run(
        ["python3", SCRIPT_PATH, start_node, end_node, str(max_cost)],
        capture_output=True,
        text=True
    )
    return result

def test_script_exists():
    """Verify that the student created the script."""
    assert os.path.isfile(SCRIPT_PATH), f"Script not found at {SCRIPT_PATH}"

def test_route_optimizer_scenario_1():
    """Test with parameters A D 15."""
    assert os.path.isfile(SCRIPT_PATH), "Script missing."

    run_script("A", "D", 15)

    assert os.path.isfile(OUTPUT_PATH), f"Output file not found at {OUTPUT_PATH} after running script."

    with open(OUTPUT_PATH, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("Output file is not valid JSON.")

    assert "path" in data, "JSON output missing 'path' key."
    assert "total_time" in data, "JSON output missing 'total_time' key."

    assert data["path"] == ["A", "B", "E", "D"], f"Expected path ['A', 'B', 'E', 'D'], got {data['path']}"
    assert data["total_time"] == 20, f"Expected total_time 20, got {data['total_time']}"

def test_route_optimizer_scenario_2():
    """Test with parameters A D 5."""
    assert os.path.isfile(SCRIPT_PATH), "Script missing."

    run_script("A", "D", 5)

    assert os.path.isfile(OUTPUT_PATH), f"Output file not found at {OUTPUT_PATH} after running script."

    with open(OUTPUT_PATH, "r") as f:
        data = json.load(f)

    assert data["path"] == ["A", "C", "D"], f"Expected path ['A', 'C', 'D'], got {data['path']}"
    assert data["total_time"] == 25, f"Expected total_time 25, got {data['total_time']}"

def test_route_optimizer_no_path():
    """Test with parameters A B 1 (no valid path)."""
    assert os.path.isfile(SCRIPT_PATH), "Script missing."

    run_script("A", "B", 1)

    assert os.path.isfile(OUTPUT_PATH), f"Output file not found at {OUTPUT_PATH} after running script."

    with open(OUTPUT_PATH, "r") as f:
        data = json.load(f)

    assert data["path"] == [], f"Expected empty path [], got {data['path']}"
    assert data["total_time"] is None, f"Expected total_time null, got {data['total_time']}"