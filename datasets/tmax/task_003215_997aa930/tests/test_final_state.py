# test_final_state.py
import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/analyze_backups.sh"
OUTPUT_PATH = "/home/user/restore_plan.txt"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_output_format_and_logic_analytics():
    # Remove output file if it exists
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)

    # Run the script with the primary test case
    result = subprocess.run(
        [SCRIPT_PATH, "analytics", "2023-10-01 00:00:00"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} was not created."

    with open(OUTPUT_PATH, "r") as f:
        content = f.read().strip()

    expected_content = """Total Size: 10000
Restoration Order:
1. core_inventory - 201 - 2023-09-28 10:00:00
2. core_users - 101 - 2023-09-29 10:00:00
3. orders - 301 - 2023-09-30 05:00:00
4. analytics - 401 - 2023-09-30 06:00:00"""

    assert content == expected_content, f"Output content did not match expected for 'analytics'.\nExpected:\n{expected_content}\n\nGot:\n{content}"

def test_dynamic_logic_reporting():
    # Remove output file to ensure fresh run
    if os.path.exists(OUTPUT_PATH):
        os.remove(OUTPUT_PATH)

    # Run the script with a different target to ensure logic is dynamic
    result = subprocess.run(
        [SCRIPT_PATH, "reporting", "2023-10-01 00:00:00"],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, f"Script failed with error: {result.stderr}"
    assert os.path.isfile(OUTPUT_PATH), f"Output file {OUTPUT_PATH} was not created."

    with open(OUTPUT_PATH, "r") as f:
        content = f.read().strip()

    expected_content = """Total Size: 15000
Restoration Order:
1. core_inventory - 201 - 2023-09-28 10:00:00
2. core_users - 101 - 2023-09-29 10:00:00
3. orders - 301 - 2023-09-30 05:00:00
4. analytics - 401 - 2023-09-30 06:00:00
5. reporting - 501 - 2023-09-30 07:00:00"""

    assert content == expected_content, f"Output content did not match expected for 'reporting'. The script might have hardcoded outputs. \nExpected:\n{expected_content}\n\nGot:\n{content}"