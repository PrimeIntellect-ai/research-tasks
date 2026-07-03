# test_final_state.py

import os
import glob
import json
import pytest

def test_c_extension_built():
    """Verify that the C-extension was built successfully in-place."""
    so_files = glob.glob("/home/user/telemetry/fast_decomp*.so")
    assert len(so_files) > 0, "The fast_decomp C-extension was not built successfully. Make sure to run 'python3 setup.py build_ext --inplace'."

def test_summary_json_exists():
    """Verify that summary.json was generated."""
    summary_path = "/home/user/telemetry/summary.json"
    assert os.path.exists(summary_path), f"The output file {summary_path} does not exist. Did you run the parser script?"
    assert os.path.isfile(summary_path), f"{summary_path} is not a file."

def test_summary_json_content():
    """Verify the content of summary.json meets the pipeline requirements."""
    summary_path = "/home/user/telemetry/summary.json"
    if not os.path.exists(summary_path):
        pytest.fail(f"Cannot verify contents because {summary_path} is missing.")

    try:
        with open(summary_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"{summary_path} does not contain valid JSON.")

    assert isinstance(data, list), "The JSON output should be a list of records."
    assert len(data) == 4, f"Expected exactly 4 records in the summary JSON, but found {len(data)}. Ensure no records are dropped."

    # Check the 3rd record specifically for the edge case
    record = data[2]
    assert "level" in record, "Record is missing 'level' key."
    assert "message" in record, "Record is missing 'message' key."

    assert record["level"] == "ERROR", f"Expected the 3rd record level to be 'ERROR', got {record['level']}."
    expected_message = "Parsing failed on | symbol in message"
    assert record["message"] == expected_message, f"The 3rd record message was parsed incorrectly. Expected '{expected_message}', but got '{record['message']}'."

def test_parser_fixed():
    """Verify that the parser.py script was actually modified to fix the bug."""
    parser_path = "/home/user/telemetry/parser.py"
    assert os.path.exists(parser_path), "parser.py is missing."

    with open(parser_path, 'r') as f:
        content = f.read()

    # It should no longer have the buggy exact split logic that fails on extra pipes
    # A simple split('|') without maxsplit or manual joining is what caused the bug
    assert "line.split('|')" not in content or "line.split('|', 2)" in content or "line.split('|', maxsplit=2)" in content or "join" in content, "parser.py still seems to contain the buggy split logic that crashes on extra '|' characters."