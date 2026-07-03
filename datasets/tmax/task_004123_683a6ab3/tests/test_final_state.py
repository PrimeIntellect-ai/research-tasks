# test_final_state.py
import os
import csv
import json
import pytest

def test_processed_csv():
    """Validates the processed.csv file has the correct fixes applied."""
    csv_path = '/home/user/processed.csv'
    assert os.path.isfile(csv_path), f"File missing: {csv_path}"

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            doc_id = int(row['doc_id'])
            category_id = row['category_id']

            assert category_id.strip() != "", f"Empty category_id found for doc_id {doc_id}"
            assert "nan" not in category_id.lower(), f"NaN category_id found for doc_id {doc_id}"

            if 501 <= doc_id <= 600:
                assert category_id == "-1", f"Expected category_id '-1' for missing doc_id {doc_id}, but got '{category_id}'"

def test_report_json():
    """Validates the report.json outputs and benchmarking results."""
    json_path = '/home/user/report.json'
    assert os.path.isfile(json_path), f"File missing: {json_path}"

    with open(json_path, 'r', encoding='utf-8') as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON")

    # 1. Validate top 5 for doc_id = 10
    assert "top_5_for_10" in report, "Key 'top_5_for_10' missing in report.json"
    expected_top_5 = [999, 584, 829, 693, 22]
    assert report["top_5_for_10"] == expected_top_5, f"Expected top_5_for_10 to be {expected_top_5}, got {report['top_5_for_10']}"

    # 2. Validate category_id_dtype
    assert "category_id_dtype" in report, "Key 'category_id_dtype' missing in report.json"
    assert report["category_id_dtype"] == "int64", f"Expected category_id_dtype to be 'int64', got {report['category_id_dtype']}"

    # 3. Validate benchmarking metrics
    for key in ["mean_time_sec", "ci_lower", "ci_upper"]:
        assert key in report, f"Key '{key}' missing in report.json"
        assert isinstance(report[key], (int, float)), f"Key '{key}' must be a number"

    mean_time = report["mean_time_sec"]
    ci_lower = report["ci_lower"]
    ci_upper = report["ci_upper"]

    assert mean_time > 0, f"mean_time_sec must be greater than 0, got {mean_time}"
    assert ci_lower < mean_time, f"ci_lower ({ci_lower}) must be less than mean_time_sec ({mean_time})"
    assert mean_time < ci_upper, f"mean_time_sec ({mean_time}) must be less than ci_upper ({ci_upper})"