# test_final_state.py

import os
import re
import pytest

def test_aggregated_data_complete():
    aggregated_file = "/home/user/sensor_pipeline/out/aggregated.dat"
    assert os.path.isfile(aggregated_file), f"Aggregated file {aggregated_file} does not exist."

    with open(aggregated_file, "r") as f:
        lines = f.read().splitlines()

    # Check that all 30 lines are present (10 chunks * 3 lines)
    # The sum of all values should be exactly 60.165
    assert len(lines) == 30, f"Expected exactly 30 lines in {aggregated_file}, found {len(lines)}. Race condition might not be fully fixed."

    total_sum = sum(float(line.strip()) for line in lines if line.strip())
    assert abs(total_sum - 60.165) < 1e-6, f"Expected sum of aggregated data to be 60.165, got {total_sum}."

def test_calculate_convergence_fixed():
    script_path = "/home/user/sensor_pipeline/calculate_convergence.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    with open(script_path, "r") as f:
        content = f.read()

    # Check if scale is set in the bc commands
    assert re.search(r"scale\s*=\s*[6-9]|\bscale\s*=\s*[1-9][0-9]+", content), "The calculate_convergence.sh script does not set scale to at least 6 in bc commands."

def test_convergence_result_file():
    result_file = "/home/user/convergence_result.txt"
    assert os.path.isfile(result_file), f"Result file {result_file} is missing."

    with open(result_file, "r") as f:
        content = f.read().strip()

    assert "." in content, f"Result file {result_file} does not contain a decimal point. Content: {content}"

    # Extract the first float found in the file
    match = re.search(r"(\d+\.\d+)", content)
    assert match is not None, f"Could not find a floating-point number in {result_file}."

    val = float(match.group(1))

    # The theoretical value is ~5.2466 after 50 iterations with scale=6.
    # We allow a generous range to account for different scale values >= 6.
    assert 5.0 < val < 5.5, f"Converged value {val} is outside the expected range (5.0 - 5.5)."