# test_final_state.py

import os
import json
import csv
from collections import defaultdict

def compute_truth():
    logs_path = "/home/user/data/pipeline_logs.jsonl"
    csv_path = "/home/user/data/output_data.csv"

    retried_jobs = set()
    if os.path.exists(logs_path):
        with open(logs_path, 'r') as f:
            for line in f:
                if not line.strip():
                    continue
                record = json.loads(line)
                if record.get("status") == "RETRYING":
                    retried_jobs.add(record.get("job_id"))

    retried_jobs_sorted = sorted(list(retried_jobs))

    duplicates_per_job = defaultdict(int)
    record_counts = defaultdict(lambda: defaultdict(int))

    if os.path.exists(csv_path):
        with open(csv_path, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                job_id = row.get("job_id")
                record_id = row.get("record_id")
                if job_id in retried_jobs:
                    record_counts[job_id][record_id] += 1

    for job_id, records in record_counts.items():
        for rec_id, count in records.items():
            if count > 1:
                duplicates_per_job[job_id] += (count - 1)

    total_duplicates = sum(duplicates_per_job.values())
    max_job = max(duplicates_per_job.keys(), key=lambda j: duplicates_per_job[j]) if duplicates_per_job else None

    return {
        "retried_jobs": retried_jobs_sorted,
        "total_duplicates_from_retries": total_duplicates,
        "max_retry_spike_job": max_job
    }

def test_anomaly_report_exists():
    report_path = "/home/user/anomaly_report.json"
    assert os.path.isfile(report_path), f"The anomaly report file {report_path} does not exist."

def test_anomaly_report_content():
    report_path = "/home/user/anomaly_report.json"
    assert os.path.isfile(report_path), f"The anomaly report file {report_path} does not exist."

    with open(report_path, 'r') as f:
        try:
            student_report = json.load(f)
        except json.JSONDecodeError:
            assert False, f"The file {report_path} does not contain valid JSON."

    expected_truth = compute_truth()

    assert "retried_jobs" in student_report, "Missing 'retried_jobs' key in the report."
    assert student_report["retried_jobs"] == expected_truth["retried_jobs"], \
        f"Expected retried_jobs to be {expected_truth['retried_jobs']}, but got {student_report['retried_jobs']}"

    assert "total_duplicates_from_retries" in student_report, "Missing 'total_duplicates_from_retries' key in the report."
    assert student_report["total_duplicates_from_retries"] == expected_truth["total_duplicates_from_retries"], \
        f"Expected total_duplicates_from_retries to be {expected_truth['total_duplicates_from_retries']}, but got {student_report['total_duplicates_from_retries']}"

    assert "max_retry_spike_job" in student_report, "Missing 'max_retry_spike_job' key in the report."
    assert student_report["max_retry_spike_job"] == expected_truth["max_retry_spike_job"], \
        f"Expected max_retry_spike_job to be {expected_truth['max_retry_spike_job']}, but got {student_report['max_retry_spike_job']}"