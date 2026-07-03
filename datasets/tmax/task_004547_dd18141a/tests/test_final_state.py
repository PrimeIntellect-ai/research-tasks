# test_final_state.py
import os
import json
import re
import pytest

def test_report_json_exists_and_correct():
    report_path = "/home/user/report.json"
    assert os.path.exists(report_path), f"File {report_path} is missing."

    with open(report_path, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{report_path} is not valid JSON.")

    assert isinstance(report_data, list), "Report must be a JSON array."

    expected_data = [
        {
            "job_id": "JOB_START",
            "storage_target": "s3",
            "latest_3run_avg": 110.0
        },
        {
            "job_id": "JOB_A",
            "storage_target": "gcs",
            "latest_3run_avg": 70.0
        },
        {
            "job_id": "JOB_C",
            "storage_target": "s3",
            "latest_3run_avg": 300.0
        },
        {
            "job_id": "JOB_END",
            "storage_target": "local",
            "latest_3run_avg": 15.0
        }
    ]

    assert len(report_data) == len(expected_data), f"Expected {len(expected_data)} items in report, found {len(report_data)}."

    for i, (actual, expected) in enumerate(zip(report_data, expected_data)):
        assert actual.get("job_id") == expected["job_id"], f"Item {i}: Expected job_id {expected['job_id']}, got {actual.get('job_id')}"
        assert actual.get("storage_target") == expected["storage_target"], f"Item {i}: Expected storage_target {expected['storage_target']}, got {actual.get('storage_target')}"
        assert abs(actual.get("latest_3run_avg", 0) - expected["latest_3run_avg"]) < 1e-5, f"Item {i}: Expected latest_3run_avg {expected['latest_3run_avg']}, got {actual.get('latest_3run_avg')}"

def test_optimize_sql_exists_and_correct():
    optimize_path = "/home/user/optimize.sql"
    assert os.path.exists(optimize_path), f"File {optimize_path} is missing."

    with open(optimize_path, "r") as f:
        sql_content = f.read().strip().lower()

    # The index should be on backup_logs(job_id, run_date) or backup_logs(run_date, job_id)
    # We will use regex to check for CREATE INDEX ... ON backup_logs ... (job_id, run_date)
    assert "create " in sql_content and "index " in sql_content, "optimize.sql must contain a CREATE INDEX statement."
    assert "on backup_logs" in sql_content, "The index must be created on the backup_logs table."

    # Check for the columns in the index
    match = re.search(r"\(([^)]+)\)", sql_content)
    assert match is not None, "Could not find column definitions in CREATE INDEX statement."

    columns = [c.strip() for c in match.group(1).split(",")]
    assert "job_id" in columns and "run_date" in columns, "The index must include both job_id and run_date columns."