# test_final_state.py

import os
import json
import pytest

def test_root_cause_file():
    """Verify that root_cause.txt contains the correct trace_id."""
    root_cause_path = "/home/user/root_cause.txt"
    assert os.path.isfile(root_cause_path), f"File {root_cause_path} does not exist."

    with open(root_cause_path, "r") as f:
        content = f.read().strip()

    assert "req-4" in content, f"Expected 'req-4' in {root_cause_path}, but found: {content}"

def test_completed_traces_json():
    """Verify that completed_traces.json contains the correct traces and omits req-4."""
    traces_path = "/home/user/completed_traces.json"
    assert os.path.isfile(traces_path), f"File {traces_path} does not exist. Did you run the fixed program?"

    with open(traces_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{traces_path} is not valid JSON.")

    assert isinstance(data, list), f"Expected JSON array in {traces_path}, got {type(data)}."
    assert len(data) == 4, f"Expected exactly 4 traces in {traces_path}, but found {len(data)}."

    trace_ids = [item.get("trace_id") for item in data if isinstance(item, dict)]
    expected_traces = {"req-1", "req-2", "req-3", "req-5"}

    assert set(trace_ids) == expected_traces, f"Expected traces {expected_traces}, but found {set(trace_ids)}."
    assert "req-4" not in trace_ids, "req-4 should not be included in the completed traces."

def test_rust_code_fixed():
    """Verify that the unwrap() panic was removed from main.rs."""
    main_rs_path = "/home/user/trace_aggregator/src/main.rs"
    assert os.path.isfile(main_rs_path), f"Source file missing at {main_rs_path}"

    with open(main_rs_path, "r") as f:
        content = f.read()

    buggy_line = "let start_time = active_traces.get(&event.trace_id).unwrap();"
    assert buggy_line not in content, "The buggy unwrap() call is still present in main.rs."