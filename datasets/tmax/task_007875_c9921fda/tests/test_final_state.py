# test_final_state.py

import os
import json
import pytest

def test_report_json_exists_and_content():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Expected output file {report_path} is missing."

    with open(report_path, "r", encoding="utf-8") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} does not contain valid JSON.")

    expected_keys = {"shortest_path", "pattern_matches", "top_authors"}
    assert set(report_data.keys()) == expected_keys, f"JSON keys in {report_path} do not match expected keys. Found: {list(report_data.keys())}"

    expected_shortest_path = ["P10", "P9", "P3", "P1"]
    assert report_data["shortest_path"] == expected_shortest_path, f"shortest_path is incorrect. Expected {expected_shortest_path}, got {report_data['shortest_path']}"

    expected_pattern_matches = [
        ["P5", "P3", "P1"],
        ["P9", "P8", "P7"]
    ]
    assert report_data["pattern_matches"] == expected_pattern_matches, f"pattern_matches is incorrect. Expected {expected_pattern_matches}, got {report_data['pattern_matches']}"

    expected_top_authors = ["A1", "A2", "A3"]
    assert report_data["top_authors"] == expected_top_authors, f"top_authors is incorrect. Expected {expected_top_authors}, got {report_data['top_authors']}"