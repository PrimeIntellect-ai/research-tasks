# test_final_state.py

import os
import json
import subprocess
import pytest

SCRIPT_PATH = "/home/user/org_query.py"
OUTPUT_PATH = "/home/user/output.json"

def run_script(emp_id):
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)

    result = subprocess.run(
        ["python3", SCRIPT_PATH, str(emp_id)],
        capture_output=True,
        text=True
    )
    return result

def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."

def test_script_logic_and_output_emp_2():
    result = run_script(2)
    assert result.returncode == 0, f"Script failed for emp_id 2 with error: {result.stderr}"
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} was not created."

    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data.get("manager_id") == 2, "Incorrect manager_id in output."
    assert data.get("total_employees") == 6, "Incorrect total_employees for emp_id 2."
    assert data.get("total_salary") == 650000, "Incorrect total_salary for emp_id 2."

def test_script_logic_and_output_emp_3():
    result = run_script(3)
    assert result.returncode == 0, f"Script failed for emp_id 3 with error: {result.stderr}"
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} was not created."

    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data.get("manager_id") == 3, "Incorrect manager_id in output."
    assert data.get("total_employees") == 3, "Incorrect total_employees for emp_id 3."
    assert data.get("total_salary") == 340000, "Incorrect total_salary for emp_id 3."

def test_script_logic_and_output_emp_1():
    result = run_script(1)
    assert result.returncode == 0, f"Script failed for emp_id 1 with error: {result.stderr}"
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} was not created."

    with open(OUTPUT_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert data.get("manager_id") == 1, "Incorrect manager_id in output."
    assert data.get("total_employees") == 10, "Incorrect total_employees for emp_id 1."
    assert data.get("total_salary") == 1190000, "Incorrect total_salary for emp_id 1."

def test_script_uses_recursive_cte():
    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        content = f.read().lower()

    assert "with recursive" in content or "with " in content, "Script does not appear to use a CTE (WITH RECURSIVE)."
    assert "?" in content or ":" in content or "%s" in content, "Script does not appear to use parameterized queries."