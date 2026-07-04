# test_final_state.py
import os
import subprocess
import math
import pytest

def test_minimized_crash_triggers_nan():
    """Test that the minimized crash file exists and triggers 'nan' on the buggy binary."""
    crash_file = "/home/user/minimized_crash.csv"
    buggy_binary = "/home/user/sensor_aggregator_buggy"

    assert os.path.exists(crash_file), f"Minimized crash file missing: {crash_file}"
    assert os.access(buggy_binary, os.X_OK), f"Buggy binary not executable: {buggy_binary}"

    result = subprocess.run([buggy_binary, crash_file], capture_output=True, text=True)
    assert result.returncode == 0, "Buggy binary failed to execute on minimized_crash.csv"
    output = result.stdout.strip().lower()
    assert output == "nan", f"Expected buggy binary to output 'nan', but got: {output}"

def test_fixed_output_file():
    """Test that fixed_output.txt exists and contains a valid non-negative float."""
    output_file = "/home/user/fixed_output.txt"
    assert os.path.exists(output_file), f"Fixed output file missing: {output_file}"

    with open(output_file, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
        assert not math.isnan(val), "fixed_output.txt contains 'nan'"
        assert val >= 0, "Standard deviation cannot be negative"
    except ValueError:
        pytest.fail(f"fixed_output.txt does not contain a valid float: {content}")

def test_fixed_binary_solves_cancellation():
    """Test that the recompiled binary correctly handles catastrophic cancellation."""
    fixed_binary = "/home/user/sensor_aggregator"
    test_csv = "/tmp/test_cancellation.csv"

    # Generate synthetic dataset that causes catastrophic cancellation in naive variance
    with open(test_csv, "w") as f:
        for i in range(100):
            f.write(f"{100000000.0 + i * 0.01}\n")

    assert os.access(fixed_binary, os.X_OK), f"Fixed binary not executable: {fixed_binary}"

    # Recompile to ensure the latest source is tested
    subprocess.run(["make", "-C", "/home/user"], capture_output=True)

    result = subprocess.run([fixed_binary, test_csv], capture_output=True, text=True)
    assert result.returncode == 0, "Fixed binary failed to execute on test dataset"

    output = result.stdout.strip().lower()
    assert output != "nan", "Fixed binary still outputs 'nan' on cancellation dataset"

    try:
        val = float(output)
        assert not math.isnan(val), "Fixed binary output is 'nan'"
        assert val >= 0, "Fixed binary output is negative"
        # The expected stddev for 0, 0.01, ..., 0.99 is approx 0.2901149
        assert 0.28 < val < 0.30, f"Fixed binary output {val} is far from expected ~0.29"
    except ValueError:
        pytest.fail(f"Fixed binary output is not a valid float: {output}")
    finally:
        if os.path.exists(test_csv):
            os.remove(test_csv)