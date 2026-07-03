# test_final_state.py

import os
import sys
import importlib.util
import pytest

def test_mre_exists_and_valid():
    mre_path = "/home/user/mre.py"
    assert os.path.exists(mre_path), f"File {mre_path} is missing. You must create the MRE script."

    with open(mre_path, "r") as f:
        content = f.read()

    # The MRE should be a python script that references StreamingStats
    assert "StreamingStats" in content, "mre.py must instantiate and use the StreamingStats class."
    # It should contain some python code, likely a try/except or a list of floats
    assert "100000000.1" in content or "try:" in content or "except" in content, \
        "mre.py should contain the minimal sequence of floats to reproduce the issue and handle the exception."

def test_stats_fixed_no_domain_error():
    stats_path = "/home/user/stats.py"
    assert os.path.exists(stats_path), f"File {stats_path} is missing."

    # Dynamically import the stats module
    spec = importlib.util.spec_from_file_location("stats", stats_path)
    stats_module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(stats_module)
    except Exception as e:
        pytest.fail(f"Failed to import {stats_path}: {e}")

    assert hasattr(stats_module, "StreamingStats"), "StreamingStats class is missing from stats.py."

    stats = stats_module.StreamingStats()
    # Feed the minimal sequence that caused catastrophic cancellation
    problematic_sequence = [100000000.1, 100000000.1, 100000000.1]

    for val in problematic_sequence:
        stats.update(val)

    try:
        stddev = stats.get_stddev()
    except ValueError as e:
        pytest.fail(f"stats.py still raises ValueError on problematic sequence: {e}. The variance calculation is not fixed.")
    except Exception as e:
        pytest.fail(f"stats.py raised an unexpected error: {e}")

    assert stddev >= 0.0, "Standard deviation should be non-negative."

def test_success_txt_exists_and_complete():
    success_path = "/home/user/success.txt"
    assert os.path.exists(success_path), f"File {success_path} is missing. You must redirect the successful output here."

    with open(success_path, "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, "success.txt is empty."

    content = "".join(lines)
    # The original CSV has 8 lines (1 header + 7 data rows)
    # The last row is index 7 (Row 7 in 0-indexed loop + 1)
    assert "Row 7:" in content, "success.txt does not contain the output for the final row. The script may have crashed."
    assert "val=100000000.1" in content, "success.txt does not contain the expected value for the final row."