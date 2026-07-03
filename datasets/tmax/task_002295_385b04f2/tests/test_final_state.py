# test_final_state.py

import os
import subprocess
import pytest

BINARY_PATH = "/home/user/finance-aggregator-fixed"
TEST_DATA_DIR = "/tmp/large_test_data"

@pytest.fixture(scope="session", autouse=True)
def setup_test_data():
    """Generates a large dataset for testing memory and determinism."""
    os.makedirs(TEST_DATA_DIR, exist_ok=True)

    # Use the exact bash snippet from the metric evaluation to generate data
    script = f"""
    for i in {{1..50}}; do
        head -n 100000 /dev/urandom | tr -dc '0-9' | fold -w 5 | sed 's/^/T,/' > "{TEST_DATA_DIR}/data_$i.csv"
    done
    """
    subprocess.run(script, shell=True, executable="/bin/bash", check=True)
    yield
    # Cleanup is optional in this containerized environment

def test_binary_exists_and_executable():
    """Verify that the fixed binary exists at the correct path and is executable."""
    assert os.path.isfile(BINARY_PATH), f"Fixed binary not found at {BINARY_PATH}"
    assert os.access(BINARY_PATH, os.X_OK), f"Binary at {BINARY_PATH} is not executable"

def test_determinism_and_race_condition():
    """
    Run the binary twice on the same dataset.
    If the race condition is fixed, the output must be identical both times.
    """
    cmd = [BINARY_PATH, TEST_DATA_DIR]

    run1 = subprocess.run(cmd, capture_output=True, text=True)
    assert run1.returncode == 0, f"Binary failed on first run with error: {run1.stderr}"

    run2 = subprocess.run(cmd, capture_output=True, text=True)
    assert run2.returncode == 0, f"Binary failed on second run with error: {run2.stderr}"

    out1 = run1.stdout.strip()
    out2 = run2.stdout.strip()

    assert out1 != "", "Binary produced no standard output."
    assert out1 == out2, (
        f"Non-deterministic output detected (race condition likely not fixed).\n"
        f"Run 1 output: {out1}\nRun 2 output: {out2}"
    )

def test_memory_leak_fixed_metric():
    """
    Measure Maximum Resident Set Size (RSS) using /usr/bin/time.
    The threshold metric is <= 15000 KB.
    """
    cmd = ["/usr/bin/time", "-f", "%M", BINARY_PATH, TEST_DATA_DIR]

    # /usr/bin/time outputs the format string to stderr
    run = subprocess.run(cmd, capture_output=True, text=True)
    assert run.returncode == 0, f"Binary failed during memory test: {run.stderr}"

    # Parse the peak memory from stderr
    stderr_lines = run.stderr.strip().split('\n')
    peak_mem_str = stderr_lines[-1].strip()

    assert peak_mem_str.isdigit(), f"Could not parse memory usage from /usr/bin/time output: {peak_mem_str}"

    peak_mem_kb = int(peak_mem_str)
    threshold_kb = 15000

    assert peak_mem_kb <= threshold_kb, (
        f"Memory leak detected! Peak memory usage was {peak_mem_kb} KB, "
        f"which exceeds the threshold of {threshold_kb} KB."
    )