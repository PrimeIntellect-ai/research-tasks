# test_final_state.py
import os
import math
import pytest

def compute_expected_variance(data_path):
    count = 0
    mean = 0.0
    M2 = 0.0
    with open(data_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                val = float(line)
                count += 1
                delta = val - mean
                mean += delta / count
                delta2 = val - mean
                M2 += delta * delta2
    if count < 2:
        return 0.0
    return M2 / (count - 1)

def test_stats_service_fixed():
    path = "/home/user/stats_service.py"
    assert os.path.isfile(path), f"The file {path} is missing."

    with open(path, 'r') as f:
        content = f.read()

    assert "class StatsTracker:" in content, f"The file {path} does not contain the 'StatsTracker' class."
    assert ".append(" not in content, "The script still contains list appends, which causes memory leaks for large streams."

def test_output_variance_correct():
    data_path = "/home/user/data.txt"
    output_path = "/home/user/output.txt"

    assert os.path.isfile(data_path), f"The dataset file {data_path} is missing."
    assert os.path.isfile(output_path), f"The output file {output_path} is missing. Did you run the script?"

    expected_variance = compute_expected_variance(data_path)

    with open(output_path, 'r') as f:
        output_content = f.read().strip()

    assert output_content, f"The output file {output_path} is empty."

    try:
        actual_variance = float(output_content)
    except ValueError:
        pytest.fail(f"The output file {output_path} does not contain a valid float: '{output_content}'")

    # The original script formats to 6 decimal places, so we check with a reasonable tolerance.
    assert math.isclose(actual_variance, expected_variance, rel_tol=1e-5), \
        f"The computed variance {actual_variance} is incorrect. Expected approximately {expected_variance:.6f}."