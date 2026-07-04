# test_final_state.py

import os
import re
import pytest

def test_go_main_exists():
    main_go_path = "/home/user/profiler/main.go"
    assert os.path.exists(main_go_path), f"The file {main_go_path} is missing."
    assert os.path.isfile(main_go_path), f"{main_go_path} is not a file."

def test_output_file_exists():
    output_path = "/home/user/output.txt"
    assert os.path.exists(output_path), f"The file {output_path} is missing. Did your Go program write to it?"
    assert os.path.isfile(output_path), f"{output_path} is not a file."

def test_output_contents():
    output_path = "/home/user/output.txt"
    with open(output_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {output_path}, found {len(lines)}."

    integral_match = re.match(r"^Integral:\s*([0-9\.\-]+)$", lines[0])
    assert integral_match, f"Line 1 does not match the expected format 'Integral: [value]'. Found: '{lines[0]}'"

    tstat_match = re.match(r"^t-stat:\s*([0-9\.\-]+)$", lines[1])
    assert tstat_match, f"Line 2 does not match the expected format 't-stat: [value]'. Found: '{lines[1]}'"

    integral_val = float(integral_match.group(1))
    tstat_val = float(tstat_match.group(1))

    # Check values with a small tolerance for numerical integration and rounding
    assert integral_val == pytest.approx(4.6079, abs=1e-3), \
        f"Expected Integral to be approximately 4.6079, but got {integral_val}"

    assert tstat_val == pytest.approx(3.8730, abs=1e-3), \
        f"Expected t-stat to be approximately 3.8730, but got {tstat_val}"