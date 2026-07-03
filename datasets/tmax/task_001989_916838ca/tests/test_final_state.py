# test_final_state.py

import os
import subprocess
import pytest

SCRIPT_PATH = "/home/user/query_sales.sh"

def test_script_exists_and_executable():
    """Check if the script exists and is executable."""
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} is missing."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def run_script(*args):
    """Helper to run the script and return stdout."""
    cmd = [SCRIPT_PATH] + [str(a) for a in args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}\nStderr: {result.stderr}"
    return result.stdout.strip()

def test_query_west_amount_desc():
    """Test Case 1: West, min amount 200, sort by Amount (col 5) desc, page 2, size 2."""
    output = run_script("West", 200, 5, 2, 2)
    expected = (
        "103,2023-01-03,West,Electronics,800,Charlie\n"
        "117,2023-01-17,West,Books,500,Charlie"
    )
    assert output == expected, f"Expected:\n{expected}\nGot:\n{output}"

def test_query_north_id_desc():
    """Test Case 2: North, min amount 0, sort by TransactionID (col 1) desc, page 1, size 2."""
    output = run_script("North", 0, 1, 1, 2)
    expected = (
        "114,2023-01-14,North,Books,350,Alice\n"
        "107,2023-01-07,North,Clothing,100,Alice"
    )
    assert output == expected, f"Expected:\n{expected}\nGot:\n{output}"

def test_query_south_category_desc():
    """Test Case 3: South, min amount 100, sort by Category (col 4) desc alphabetically, page 1, size 3."""
    output = run_script("South", 100, 4, 1, 3)
    # South rows:
    # 102,2023-01-02,South,Books,150,Bob
    # 109,2023-01-09,South,Electronics,900,Bob
    # 116,2023-01-16,South,Clothing,130,Bob
    # Sorted by Category desc (Electronics, Clothing, Books):
    expected = (
        "109,2023-01-09,South,Electronics,900,Bob\n"
        "116,2023-01-16,South,Clothing,130,Bob\n"
        "102,2023-01-02,South,Books,150,Bob"
    )
    assert output == expected, f"Expected:\n{expected}\nGot:\n{output}"