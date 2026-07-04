# test_final_state.py

import os
import subprocess
import re
import pytest

def test_recovered_database():
    db_path = "/home/user/recovered.db"
    assert os.path.isfile(db_path), f"Phase 1 Failed: File {db_path} does not exist."

    try:
        result = subprocess.run(
            ["sqlite3", db_path, "PRAGMA integrity_check;"],
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip().lower()
        assert output == "ok", f"Phase 1 Failed: Integrity check returned '{output}' instead of 'ok'."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Phase 1 Failed: sqlite3 command failed with error: {e.stderr}")
    except FileNotFoundError:
        pytest.fail("Phase 1 Failed: sqlite3 is not installed or not in PATH.")

def test_query_result():
    csv_path = "/home/user/query_result.csv"
    assert os.path.isfile(csv_path), f"Phase 2 Failed: File {csv_path} does not exist."

    with open(csv_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "S4,50.0",
        "S3,40.0",
        "S1,35.0"
    ]
    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"Phase 2 Failed: CSV content mismatch.\n"
        f"Expected: {expected_lines}\n"
        f"Got: {actual_lines}"
    )

def test_mre_script():
    mre_path = "/home/user/mre.sh"
    assert os.path.isfile(mre_path), f"Phase 3 Failed: File {mre_path} does not exist."

    with open(mre_path, "r") as f:
        lines = f.readlines()

    assert len(lines) <= 15, f"Phase 3 Failed: MRE script is too long ({len(lines)} lines). Must be under 15 lines."

    content = "".join(lines)

    # Check for array initialization
    has_array_init = re.search(r"(declare\s+-a\s+\w+|^\s*\w+=\(\))", content, re.MULTILINE)
    assert has_array_init, "Phase 3 Failed: MRE script does not contain an array initialization (e.g., `declare -a ARR` or `ARR=()`)."

    # Check for loop
    has_loop = re.search(r"\b(while|for)\b", content)
    assert has_loop, "Phase 3 Failed: MRE script does not contain a loop (`while` or `for`)."

    # Check for array append
    has_append = re.search(r"\w+\+=\(", content)
    assert has_append, "Phase 3 Failed: MRE script does not contain an array append operation (e.g., `ARR+=()`)."