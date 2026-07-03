# test_final_state.py

import os
import json
import re

def test_clean_traces_exists_and_correct():
    """Check if clean_traces.json exists and contains the expected resolved traces."""
    output_path = '/home/user/clean_traces.json'
    assert os.path.isfile(output_path), f"Output file not found: {output_path}"

    try:
        with open(output_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {output_path} is not valid JSON.")

    expected = {
        "T001": "Init Process",
        "T002": "Init Process -> Auth Module",
        "T005": "Init Process -> Auth Module -> DB Query",
        "T006": "Init Process -> Auth Module -> DB Query -> Render Response"
    }

    assert data == expected, f"Content of {output_path} does not match expected output. Got: {data}"

def test_trace_analyzer_uses_assert():
    """Check if trace_analyzer.py implements the required assert statement for trace_id validation."""
    script_path = '/home/user/trace_analyzer.py'
    assert os.path.isfile(script_path), f"Script not found: {script_path}"

    with open(script_path, 'r') as f:
        content = f.read()

    # The instructions specifically mandate using Python's `assert` statement to verify the trace_id format.
    assert "assert " in content, "trace_analyzer.py does not contain an 'assert' statement as required."
    assert "AssertionError" in content, "trace_analyzer.py does not catch 'AssertionError' as required."