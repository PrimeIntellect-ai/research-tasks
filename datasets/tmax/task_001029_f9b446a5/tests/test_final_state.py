# test_final_state.py

import os
import re
import subprocess
import pytest

def test_etl_script_exists_and_executable():
    script_path = "/home/user/etl.sh"
    assert os.path.exists(script_path), f"Script {script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_output_csv_content():
    output_path = "/home/user/output.csv"
    assert os.path.exists(output_path), f"Output file {output_path} does not exist."

    expected_content = """user_id,event,region,tier
101,login,NA,Pro
102,purchase,EU,Free
103,logout,AP,Pro
105,view_item,SA,Free
"""

    with open(output_path, "r") as f:
        actual_content = f.read()

    # Normalize line endings and strip trailing whitespace for robust comparison
    actual_lines = [line.strip() for line in actual_content.strip().splitlines()]
    expected_lines = [line.strip() for line in expected_content.strip().splitlines()]

    assert actual_lines == expected_lines, f"Content of {output_path} does not match expected output."

def test_crontab_entry():
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        crontab_output = result.stdout
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to read crontab: {e.stderr}")

    # Look for a cron entry running at minute 0 of every hour
    # e.g. "0 * * * * /home/user/etl.sh"
    pattern = re.compile(r"^0\s+\*\s+\*\s+\*\s+\*.*\/home\/user\/etl\.sh", re.MULTILINE)

    assert pattern.search(crontab_output), "Crontab entry for /home/user/etl.sh at minute 0 (0 * * * *) is missing or incorrect."