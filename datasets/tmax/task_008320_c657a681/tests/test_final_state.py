# test_final_state.py
import os
import json
import pytest

PIPELINE_JSON_PATH = '/home/user/pipeline.json'

def test_pipeline_json_exists():
    assert os.path.exists(PIPELINE_JSON_PATH), f"Output file {PIPELINE_JSON_PATH} is missing."
    assert os.path.isfile(PIPELINE_JSON_PATH), f"{PIPELINE_JSON_PATH} is not a file."

def test_pipeline_json_content():
    assert os.path.exists(PIPELINE_JSON_PATH), f"Cannot check content, {PIPELINE_JSON_PATH} is missing."

    with open(PIPELINE_JSON_PATH, 'r') as f:
        content = f.read()

    # Check exact minified format as requested
    stripped_content = content.strip()
    expected_content = '{"pipeline":["raw_clicks","stg_clicks","realtime_metrics","executive_dashboard"]}'

    assert stripped_content == expected_content, (
        f"The content of {PIPELINE_JSON_PATH} does not match the expected minified JSON string.\n"
        f"Expected: {expected_content}\n"
        f"Actual: {stripped_content}"
    )

    # Ensure it contains no internal spaces or newlines (except possibly a trailing newline)
    assert ' ' not in stripped_content, "The JSON output contains spaces, which violates the minified constraint."
    assert '\n' not in stripped_content, "The JSON output contains newlines inside the structure, which violates the minified constraint."

    # Validate it is valid JSON
    try:
        parsed = json.loads(stripped_content)
    except json.JSONDecodeError:
        pytest.fail("The output is not valid JSON.")

    assert "pipeline" in parsed, "The JSON output does not contain the 'pipeline' key."
    assert parsed["pipeline"] == ["raw_clicks", "stg_clicks", "realtime_metrics", "executive_dashboard"], "The shortest path is incorrect."