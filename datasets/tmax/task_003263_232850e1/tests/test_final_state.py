# test_final_state.py

import os
import subprocess
import pytest

def test_etl_pipeline_output():
    script_path = "/home/user/etl_pipeline.sh"
    report_path = "/home/user/report.csv"

    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    # Run the script to generate the report
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed with error: {result.stderr}"

    assert os.path.isfile(report_path), f"Report file {report_path} was not generated."

    with open(report_path, "r") as f:
        content = f.read().strip().splitlines()

    expected_content = [
        "101,Alice,Premium,50.0",
        "102,Bob,Standard,75.5",
        "103,Alice,Premium,30.0",
        "104,Charlie,Premium,100.0"
    ]

    assert len(content) == len(expected_content), f"Expected {len(expected_content)} rows, but got {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_content)):
        assert actual == expected, f"Row {i+1} mismatch: expected '{expected}', got '{actual}'."