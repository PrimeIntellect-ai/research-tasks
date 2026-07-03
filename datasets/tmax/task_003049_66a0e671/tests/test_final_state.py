# test_final_state.py
import os
import pytest

def test_go_source_exists():
    file_path = "/home/user/queuing_mcmc.go"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."

def test_cpu_profile_exists():
    file_path = "/home/user/cpu.prof"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."
    assert os.path.getsize(file_path) > 0, f"The file {file_path} is empty."

def test_results_file_and_values():
    file_path = "/home/user/results.txt"
    assert os.path.isfile(file_path), f"The file {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    parts = content.split(",")
    assert len(parts) == 2, f"Expected 2 comma-separated values in {file_path}, got {len(parts)}."

    try:
        mu = float(parts[0].strip())
        sigma = float(parts[1].strip())
    except ValueError:
        pytest.fail(f"Could not parse values in {file_path} as floats. Content: {content}")

    assert 2.0 <= mu <= 3.5, f"Estimated mu ({mu}) is outside the expected range [2.0, 3.5]."
    assert 0.05 <= sigma <= 0.4, f"Estimated sigma ({sigma}) is outside the expected range [0.05, 0.4]."