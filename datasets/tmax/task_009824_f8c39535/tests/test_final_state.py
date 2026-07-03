# test_final_state.py

import os
import pytest

def test_analyze_script_exists_and_executable():
    script_path = "/home/user/analyze.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

def test_report_html_exists():
    report_path = "/home/user/report.html"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist"

def test_report_html_content():
    report_path = "/home/user/report.html"
    assert os.path.isfile(report_path), f"Report file {report_path} does not exist"

    with open(report_path, "r") as f:
        content = f.read()

    # Check if the placeholder was replaced
    assert "__TABLE_ROWS__" not in content, "Placeholder __TABLE_ROWS__ was not replaced in the report"

    # Check for the expected rows in chronological and alphabetical order
    expected_rows = [
        "<tr><td>2023-10-01_10</td><td>ERR-001</td><td>3</td></tr>",
        "<tr><td>2023-10-01_10</td><td>ERR-002</td><td>1</td></tr>",
        "<tr><td>2023-10-01_11</td><td>ERR-002</td><td>2</td></tr>"
    ]

    # Verify each row is in the file
    for row in expected_rows:
        assert row in content.replace(" ", ""), f"Expected row {row} not found in {report_path}"

    # Verify the order of the rows
    content_no_spaces = content.replace(" ", "")
    pos1 = content_no_spaces.find(expected_rows[0])
    pos2 = content_no_spaces.find(expected_rows[1])
    pos3 = content_no_spaces.find(expected_rows[2])

    assert pos1 != -1 and pos2 != -1 and pos3 != -1, "Not all expected rows were found"
    assert pos1 < pos2 < pos3, "The generated rows are not sorted correctly by HOUR and ERROR_CODE"