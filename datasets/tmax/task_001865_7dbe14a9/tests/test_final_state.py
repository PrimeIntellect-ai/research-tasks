# test_final_state.py
import json
import os
import pytest

def test_report_accuracy():
    """Validates the output report.json against the expected ground truth using Jaccard similarity."""
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Report file not found at {report_path}"

    try:
        with open(report_path, 'r') as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {report_path} is not valid JSON")

    expected_server = "SERVER-82"
    actual_server = data.get("server_audited")
    assert actual_server == expected_server, f"Expected server_audited to be '{expected_server}', but got '{actual_server}'"

    expected_tuples = {("U-909", 1672531100), ("U-112", 1672540000)}

    actual_tuples = set()
    for item in data.get("unauthorized_access", []):
        actual_tuples.add((item.get("user_id"), item.get("timestamp")))

    intersection = expected_tuples.intersection(actual_tuples)
    union = expected_tuples.union(actual_tuples)

    if not union:
        jaccard = 0.0
    else:
        jaccard = len(intersection) / len(union)

    assert jaccard >= 0.99, f"Jaccard similarity {jaccard:.4f} is below threshold 0.99. Expected {expected_tuples}, got {actual_tuples}"