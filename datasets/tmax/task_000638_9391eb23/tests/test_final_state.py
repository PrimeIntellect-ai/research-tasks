# test_final_state.py

import os
import json
import math
import re
import pytest

def compute_expected_closest():
    log_path = "/home/user/flight_data.log"
    assert os.path.exists(log_path), f"Log file missing at {log_path}"

    depot_lat = 45.5000
    depot_lon = -122.6000

    closest_drone = None
    min_dist = float('inf')

    with open(log_path, 'r') as f:
        for line in f:
            if " INFO " in line and "Pos:" in line:
                drone_match = re.search(r"Drone ID:\s*([^\s|]+)", line)
                pos_match = re.search(r"Pos:\s*([-\d.]+),\s*([-\d.]+)", line)
                if drone_match and pos_match:
                    drone_id = drone_match.group(1)
                    lat = float(pos_match.group(1))
                    lon = float(pos_match.group(2))

                    dist = math.sqrt((lat - depot_lat)**2 + (lon - depot_lon)**2)
                    if dist < min_dist:
                        min_dist = dist
                        closest_drone = drone_id

    return closest_drone, round(min_dist, 4)

def test_script_exists_and_executable():
    script_path = "/home/user/process_flights.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_json_output_correct():
    json_path = "/home/user/closest_drone.json"
    assert os.path.exists(json_path), f"The output JSON file {json_path} does not exist."
    assert os.path.isfile(json_path), f"{json_path} is not a file."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    assert "closest_drone" in data, f"'closest_drone' key missing in {json_path}"
    assert "distance" in data, f"'distance' key missing in {json_path}"

    expected_drone, expected_dist = compute_expected_closest()

    assert data["closest_drone"] == expected_drone, (
        f"Expected closest_drone to be '{expected_drone}', but got '{data['closest_drone']}'. "
        "Ensure you are only considering valid INFO lines."
    )

    actual_dist = data["distance"]
    assert isinstance(actual_dist, (int, float)), f"'distance' must be a number, got {type(actual_dist)}"

    assert math.isclose(actual_dist, expected_dist, rel_tol=1e-4, abs_tol=1e-4), (
        f"Expected distance to be {expected_dist}, but got {actual_dist}."
    )