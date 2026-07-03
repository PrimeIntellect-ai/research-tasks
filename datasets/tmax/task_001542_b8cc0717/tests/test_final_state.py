# test_final_state.py

import os
import re
import pytest

def test_report_exists_and_format():
    """Verify that report.txt exists and contains the correct answers."""
    report_path = "/home/user/report.txt"
    assert os.path.exists(report_path), f"Missing required file: {report_path}"
    assert os.path.isfile(report_path), f"Expected a file, but found something else: {report_path}"

    with open(report_path, "r") as f:
        content = f.read().strip()

    # Parse the content
    missing_library_match = re.search(r"Missing library:\s*(.+)", content)
    failing_row_match = re.search(r"Failing row index:\s*(\d+)", content)

    assert missing_library_match is not None, "Could not find 'Missing library: <name>' in report.txt"
    assert failing_row_match is not None, "Could not find 'Failing row index: <integer>' in report.txt"

    missing_library = missing_library_match.group(1).strip()
    failing_row = int(failing_row_match.group(1).strip())

    assert missing_library == "m", f"Expected missing library to be 'm', but got '{missing_library}'"
    assert failing_row == 682, f"Expected failing row index to be 682, but got {failing_row}"

def test_setup_py_fixed():
    """Verify that setup.py was modified to include the missing library."""
    setup_path = "/home/user/setup.py"
    assert os.path.exists(setup_path), f"Missing {setup_path}"

    with open(setup_path, "r") as f:
        content = f.read()

    # The user should have added libraries=['m'] to setup.py
    # We just check if 'm' is somewhere in the file, likely as libraries=['m']
    assert re.search(r"libraries\s*=\s*\[\s*['\"]m['\"]\s*\]", content) is not None, "setup.py does not appear to have libraries=['m'] added."