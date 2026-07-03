# test_final_state.py
import os
import sys
import math
import pytest

CRASH_INPUT_PATH = "/home/user/crash_input.txt"
FIXED_STATS_PATH = "/home/user/fixed_stats.py"
RUN_TRACE_PATH = "/home/user/run_trace.py"
FIXED_OUTPUT_PATH = "/home/user/fixed_output.txt"

def test_files_exist():
    for path in [CRASH_INPUT_PATH, FIXED_STATS_PATH, RUN_TRACE_PATH, FIXED_OUTPUT_PATH]:
        assert os.path.isfile(path), f"Required file {path} is missing."

def test_crash_input_triggers_value_error():
    sys.path.insert(0, "/home/user")
    import legacy_stats

    with open(CRASH_INPUT_PATH, "r") as f:
        content = f.read().strip()

    assert content, "crash_input.txt is empty."
    try:
        data = [float(x.strip()) for x in content.split(",")]
    except ValueError:
        pytest.fail("crash_input.txt does not contain valid comma-separated floats.")

    with pytest.raises(ValueError) as excinfo:
        legacy_stats.calculate_metrics(data)

    assert "math domain error" in str(excinfo.value) or "math domain error" in repr(excinfo.value) or excinfo.type is ValueError, "Expected legacy_stats to raise ValueError due to math domain error."

def test_fixed_stats_implementation():
    sys.path.insert(0, "/home/user")
    import fixed_stats

    # Check that 'statistics' is not imported
    with open(FIXED_STATS_PATH, "r") as f:
        source = f.read()
    assert "import statistics" not in source, "Do not use the statistics module."
    assert "from statistics" not in source, "Do not use the statistics module."

    # Test functional correctness
    test_data = [1e9 + 1, 1e9 + 2, 1e9 + 3]
    mean, std_dev = fixed_stats.calculate_metrics(test_data)

    assert math.isclose(mean, 1e9 + 2), f"Expected mean 1000000002.0, got {mean}"
    # Population std dev of [1, 2, 3] is sqrt(2/3)
    expected_std_dev = math.sqrt(2/3)
    assert math.isclose(std_dev, expected_std_dev), f"Expected std_dev {expected_std_dev}, got {std_dev}"

def test_fixed_output_correctness():
    with open(CRASH_INPUT_PATH, "r") as f:
        content = f.read().strip()
    data = [float(x.strip()) for x in content.split(",")]

    # Calculate truth std dev (two-pass)
    n = len(data)
    mean = sum(data) / n
    variance = sum((x - mean) ** 2 for x in data) / n
    expected_std_dev = math.sqrt(variance)

    with open(FIXED_OUTPUT_PATH, "r") as f:
        output_str = f.read().strip()

    try:
        output_val = float(output_str)
    except ValueError:
        pytest.fail(f"fixed_output.txt does not contain a valid float: {output_str}")

    assert math.isclose(output_val, expected_std_dev, rel_tol=1e-5), f"fixed_output.txt contains {output_val}, expected {expected_std_dev}"