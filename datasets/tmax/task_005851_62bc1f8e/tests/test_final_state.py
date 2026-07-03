# test_final_state.py

import os
import re

def test_solution_txt_content():
    solution_path = "/home/user/solution.txt"
    assert os.path.isfile(solution_path), f"{solution_path} does not exist. Did you redirect the output?"

    with open(solution_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "Local Hour 1: 0",
        "Local Hour 2: 1",
        "Exact Diff: 1.5014"
    ]

    for line in expected_lines:
        assert line in content, f"Expected line '{line}' not found in {solution_path}."

def test_run_diag_sh_fixed():
    script_path = "/home/user/run_diag.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    # The script should now export TZ=UTC (quotes are optional but possible)
    assert re.search(r"TZ=['\"]?UTC['\"]?", content), "run_diag.sh does not correctly set TZ=UTC."
    assert "Mars/Phobos" not in content, "run_diag.sh still contains the incorrect Mars/Phobos timezone."

def test_calc_cpp_fixed():
    calc_path = "/home/user/calc.cpp"
    assert os.path.isfile(calc_path), f"{calc_path} does not exist."

    with open(calc_path, "r") as f:
        content = f.read()

    # The exact integer division bug should be gone
    # Original: double diff_hours = (t2 - t1) / 3600;
    # We check if the student changed it to floating point division or added a cast.
    bug_pattern = r"double\s+diff_hours\s*=\s*\(t2\s*-\s*t1\)\s*/\s*3600\s*;"
    assert not re.search(bug_pattern, content), "The integer division bug is still present in calc.cpp."