# test_final_state.py

import os
import stat
import csv
import re
import math
import pytest

def test_orchestrate_script_exists_and_executable():
    """Check that /home/user/orchestrate.sh exists and is executable."""
    file_path = "/home/user/orchestrate.sh"
    assert os.path.isfile(file_path), f"Script {file_path} is missing."

    st = os.stat(file_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {file_path} is not executable."

def test_results_csv_content():
    """Check the content of /home/user/results.csv."""
    file_path = "/home/user/results.csv"
    assert os.path.isfile(file_path), f"Results file {file_path} is missing."

    with open(file_path, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"{file_path} is empty."
    assert rows[0] == ["iteration", "dt", "final_y"], f"{file_path} has incorrect header."

    assert len(rows) == 6, f"{file_path} should have exactly 5 data rows (plus header), found {len(rows)-1}."

    # Check the last row
    last_row = rows[-1]
    assert last_row[0] == "5", f"Expected final iteration to be 5, got {last_row[0]}."

    # dt can be .03125 or 0.03125
    dt_val = float(last_row[1])
    assert math.isclose(dt_val, 0.03125, rel_tol=1e-5), f"Expected final dt to be 0.03125, got {last_row[1]}."

    y_val = float(last_row[2])
    assert math.isclose(y_val, 2.66773329623816568114, rel_tol=1e-5), f"Expected final y to be approx 2.667733, got {last_row[2]}."

def test_report_md_content():
    """Check the content of /home/user/report.md."""
    file_path = "/home/user/report.md"
    assert os.path.isfile(file_path), f"Report file {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    # The exact format might vary slightly with leading zeros or trailing decimals, so we use a regex
    # Expected: Convergence achieved at iteration 5 with step size 0.03125 and final value 2.66773329623816568114.
    pattern = r"Convergence achieved at iteration 5 with step size 0?\.03125 and final value 2\.667733\d*\.?"

    assert re.search(pattern, content), f"Report content does not match expected format. Got: {content}"