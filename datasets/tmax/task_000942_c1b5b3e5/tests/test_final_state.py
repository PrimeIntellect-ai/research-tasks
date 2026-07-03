# test_final_state.py
import os
import json
import csv
import re
import pytest

def compute_expected_metrics():
    source1_path = "/home/user/data/source1.csv"
    source2_path = "/home/user/data/source2.csv"
    meta_path = "/home/user/data/meta.csv"

    # Read meta
    meta = {}
    if os.path.exists(meta_path):
        with open(meta_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                meta[row["item_id"]] = row["category_code"]

    # Read source1
    combined = []
    if os.path.exists(source1_path):
        with open(source1_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                combined.append({"id": row["id"], "text": row["text"]})

    # Read source2
    if os.path.exists(source2_path):
        with open(source2_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                combined.append({"id": row["req_id"], "text": row["review_body"]})

    # Join and score
    total_rows = 0
    sum_scores = 0

    for row in combined:
        item_id = row["id"]
        if item_id in meta:
            category_code = meta[item_id]
            text = row["text"]

            # Tokenization rules
            text = text.lower()
            text = re.sub(r'[^a-z0-9\s]', '', text)
            tokens = text.split()
            valid_tokens = [t for t in tokens if len(t) >= 3]
            token_count = len(valid_tokens)

            # Score
            score = (token_count * len(category_code)) % 10

            total_rows += 1
            sum_scores += score

    return total_rows, sum_scores

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Master execution script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_report_json_content():
    report_path = "/home/user/report.json"
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {report_path} is not valid JSON.")

    expected_total_rows, expected_sum_scores = compute_expected_metrics()

    assert "total_rows" in data, "Key 'total_rows' is missing from report.json."
    assert "sum_scores" in data, "Key 'sum_scores' is missing from report.json."
    assert "benchmark_runs" in data, "Key 'benchmark_runs' is missing from report.json."

    assert data["total_rows"] == expected_total_rows, f"Expected total_rows to be {expected_total_rows}, got {data['total_rows']}"
    assert data["sum_scores"] == expected_sum_scores, f"Expected sum_scores to be {expected_sum_scores}, got {data['sum_scores']}"
    assert data["benchmark_runs"] == 100, f"Expected benchmark_runs to be 100, got {data['benchmark_runs']}"