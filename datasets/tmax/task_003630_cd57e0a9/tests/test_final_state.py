# test_final_state.py

import os
import pytest

def test_extractor_cpp_exists():
    """Test that the C++ extractor program was created."""
    file_path = "/home/user/extractor.cpp"
    assert os.path.exists(file_path), f"The C++ source file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_distance_metric_value():
    """Test that the calculated distance metric is within the acceptable threshold."""
    file_path = "/home/user/distance_metric.txt"
    assert os.path.exists(file_path), f"The output file {file_path} is missing."

    try:
        with open(file_path, 'r') as f:
            content = f.read().strip()
            val = float(content)
    except ValueError:
        pytest.fail(f"The content of {file_path} ('{content}') could not be parsed as a float.")
    except Exception as e:
        pytest.fail(f"Failed to read {file_path}: {e}")

    target_value = 40.00
    threshold = 0.1

    diff = abs(val - target_value)
    assert diff <= threshold, f"Calculated distance {val} is not within {threshold} of the target {target_value}."