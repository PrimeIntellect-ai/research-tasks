# test_final_state.py

import os
import pytest

def test_best_route_file_exists():
    assert os.path.isfile('/home/user/best_route.txt'), "/home/user/best_route.txt does not exist."

def test_best_route_content():
    with open('/home/user/best_route.txt', 'r') as f:
        lines = f.read().splitlines()

    assert len(lines) >= 2, "Output file must contain at least two lines."

    path = lines[0].strip()
    latency_str = lines[1].strip()

    try:
        latency = int(latency_str)
    except ValueError:
        pytest.fail(f"Second line must be an integer latency, got: '{latency_str}'")

    expected_latency = 60
    error = abs(latency - expected_latency)

    assert error <= 0, f"Calculated latency {latency} is incorrect. Expected {expected_latency}. Error: {error}"

    expected_path = "DB_PRIMARY,DB_B,DB_D,DB_ARCHIVE"
    assert path == expected_path, f"Path is incorrect. Expected '{expected_path}', got '{path}'"