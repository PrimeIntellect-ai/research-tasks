# test_final_state.py
import os
import pytest

def test_script_exists():
    script_path = "/home/user/fit_mcmc.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_trace_file():
    trace_path = "/home/user/trace.txt"
    assert os.path.exists(trace_path), f"Trace file {trace_path} does not exist."

    with open(trace_path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 1000, f"Expected exactly 1000 lines in trace.txt, but got {len(lines)}."

    # Check that all lines are valid floats
    for i, line in enumerate(lines):
        try:
            float(line)
        except ValueError:
            pytest.fail(f"Line {i+1} in trace.txt is not a valid float: '{line}'")

def test_k_mean_file():
    mean_path = "/home/user/k_mean.txt"
    trace_path = "/home/user/trace.txt"

    assert os.path.exists(mean_path), f"Mean file {mean_path} does not exist."

    with open(mean_path, "r") as f:
        content = f.read().strip()

    try:
        k_mean = float(content)
    except ValueError:
        pytest.fail(f"k_mean.txt does not contain a valid float: '{content}'")

    assert 0.25 <= k_mean <= 0.35, f"Expected k_mean to be between 0.25 and 0.35, but got {k_mean}."

    # Verify it matches the mean of the last 500 lines of trace.txt
    if os.path.exists(trace_path):
        with open(trace_path, "r") as f:
            lines = f.read().strip().split('\n')
        if len(lines) == 1000:
            last_500 = [float(x) for x in lines[500:1000]]
            calculated_mean = sum(last_500) / 500.0

            # Allow small floating point / rounding differences (formatted to 4 decimal places)
            assert abs(k_mean - calculated_mean) < 1e-3, (
                f"k_mean.txt value ({k_mean}) does not match the calculated mean of the last 500 trace values ({calculated_mean})."
            )