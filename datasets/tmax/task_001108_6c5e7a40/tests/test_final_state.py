# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/org_rollup.py"

def test_script_exists():
    assert os.path.exists(SCRIPT_PATH), f"Script {SCRIPT_PATH} is missing."
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} is not a file."

def test_script_requirements():
    with open(SCRIPT_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    content_upper = content.upper()
    assert "WITH RECURSIVE" in content_upper, "Script does not use 'WITH RECURSIVE' CTE as required."
    assert "SQLITE3" in content_upper, "Script does not use sqlite3 module."
    assert "CSV" in content_upper, "Script does not use csv module."
    assert "PANDAS" not in content_upper, "Script should not use external libraries like pandas."

@pytest.mark.parametrize("manager_id, expected_output", [
    ("2", "353000.00"),
    ("5", "144000.00"),
    ("1", "538000.00")
])
def test_script_output(manager_id, expected_output):
    result = subprocess.run(
        ["python3", SCRIPT_PATH, manager_id],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Script failed for manager_id {manager_id} with error: {result.stderr}"

    output = result.stdout.strip()
    assert output == expected_output, f"Expected output {expected_output} for manager_id {manager_id}, but got {output}"