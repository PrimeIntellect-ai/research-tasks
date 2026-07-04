# test_final_state.py

import os
import re
import pytest

def test_source_code_contains_assertion():
    path = "/home/user/uptime_monitor.c"
    assert os.path.isfile(path), f"File missing: {path}"

    with open(path, "r") as f:
        content = f.read()

    # Look for assert(variance >= 0.0) with flexible spacing and optional .0
    pattern = r"assert\s*\(\s*variance\s*>=\s*0(\.0)?\s*\)\s*;"
    assert re.search(pattern, content), f"Could not find required intermediate assertion 'assert(variance >= 0.0);' in {path}"

def test_compiled_binary_exists_and_executable():
    path = "/home/user/uptime_monitor_fixed"
    assert os.path.isfile(path), f"Compiled binary missing: {path}"
    assert os.access(path, os.X_OK), f"File is not executable: {path}"

def test_fixed_stats_output():
    path = "/home/user/fixed_stats.txt"
    assert os.path.isfile(path), f"Output file missing: {path}"

    with open(path, "r") as f:
        content = f.read().strip()

    assert content, f"Output file is empty: {path}"

    # Expected output format: Count: 100000, Mean: 1000000.00, StdDev: 2.50
    # We will extract the numbers and validate them.
    count_match = re.search(r"Count:\s*(\d+)", content)
    mean_match = re.search(r"Mean:\s*([\d\.]+)", content)
    stddev_match = re.search(r"StdDev:\s*([\d\.]+)", content)

    assert count_match, "Could not parse Count from output"
    assert mean_match, "Could not parse Mean from output"
    assert stddev_match, "Could not parse StdDev from output"

    count = int(count_match.group(1))
    mean = float(mean_match.group(1))
    stddev = float(stddev_match.group(1))

    assert count == 100000, f"Expected count 100000, got {count}"
    assert 999990.0 <= mean <= 1000010.0, f"Expected mean around 1000000.00, got {mean}"
    assert 2.0 <= stddev <= 3.0, f"Expected stddev around 2.50, got {stddev}"