# test_final_state.py

import os
import json
import math
import pytest

def test_primer_report_exists():
    """Check that the primer_report.json file exists."""
    report_path = "/home/user/primer_report.json"
    assert os.path.isfile(report_path), f"Missing file: {report_path}"

def test_primer_report_contents():
    """Validate the contents of primer_report.json based on the task specification."""
    report_path = "/home/user/primer_report.json"

    with open(report_path, 'r') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    required_keys = {"best_region", "k_value", "primer_sequence", "gc_content"}
    missing_keys = required_keys - set(report.keys())
    assert not missing_keys, f"Missing keys in JSON report: {missing_keys}"

    # Check best_region
    assert report["best_region"] == "B", \
        f"Expected best_region to be 'B', got '{report['best_region']}'"

    # Check k_value
    k_val = report["k_value"]
    assert isinstance(k_val, (int, float)), "k_value must be a number."
    assert math.isclose(k_val, 0.0120, abs_tol=0.0005), \
        f"Expected k_value to be close to 0.0120, got {k_val}"

    # Check primer_sequence
    primer_seq = report["primer_sequence"]
    assert isinstance(primer_seq, str), "primer_sequence must be a string."
    assert primer_seq == "ATCGATCGATCGATCGATCG", \
        f"Expected primer_sequence to be 'ATCGATCGATCGATCGATCG', got '{primer_seq}'"

    # Check gc_content
    gc_content = report["gc_content"]
    assert isinstance(gc_content, (int, float)), "gc_content must be a number."
    assert math.isclose(gc_content, 50.0, abs_tol=0.05), \
        f"Expected gc_content to be close to 50.0, got {gc_content}"