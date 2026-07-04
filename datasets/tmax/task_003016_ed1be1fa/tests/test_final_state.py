# test_final_state.py

import os
import json
import csv
import pytest

def test_experiment_summary_json():
    summary_path = "/home/user/experiment_summary.json"
    assert os.path.isfile(summary_path), f"File {summary_path} is missing. The Rust program must produce this file."

    with open(summary_path, "r") as f:
        try:
            summary = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {summary_path} is not valid JSON.")

    # Calculate expected total_artifact_bytes
    artifacts_dir = "/home/user/model_artifacts"
    expected_bytes = 0
    if os.path.isdir(artifacts_dir):
        for root, _, files in os.walk(artifacts_dir):
            for file in files:
                expected_bytes += os.path.getsize(os.path.join(root, file))

    # Calculate expected total_tokens and posterior_mean_latency
    csv_path = "/home/user/inference_benchmarks.csv"
    expected_tokens = 0
    latencies = []
    if os.path.isfile(csv_path):
        with open(csv_path, "r", newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            # Skip header
            next(reader, None)
            for row in reader:
                if len(row) >= 2:
                    text_sample = row[0]
                    # Split by ASCII whitespace equivalent
                    expected_tokens += len(text_sample.split())
                    try:
                        latencies.append(float(row[1]))
                    except ValueError:
                        pass

    n = len(latencies)
    if n > 0:
        sample_mean = sum(latencies) / n
        prior_mean = 50.0
        prior_var = 100.0
        like_var = 25.0

        inv_post_var = (1.0 / prior_var) + (n / like_var)
        post_var = 1.0 / inv_post_var
        expected_post_mean = post_var * ((prior_mean / prior_var) + (n * sample_mean / like_var))
        expected_post_mean_rounded = round(expected_post_mean, 2)
    else:
        expected_post_mean_rounded = 0.0

    assert "total_artifact_bytes" in summary, "Key 'total_artifact_bytes' is missing in the JSON file."
    assert summary["total_artifact_bytes"] == expected_bytes, f"Expected total_artifact_bytes to be {expected_bytes}, got {summary['total_artifact_bytes']}."

    assert "total_tokens" in summary, "Key 'total_tokens' is missing in the JSON file."
    assert summary["total_tokens"] == expected_tokens, f"Expected total_tokens to be {expected_tokens}, got {summary['total_tokens']}."

    assert "posterior_mean_latency" in summary, "Key 'posterior_mean_latency' is missing in the JSON file."
    assert summary["posterior_mean_latency"] == expected_post_mean_rounded, f"Expected posterior_mean_latency to be {expected_post_mean_rounded}, got {summary['posterior_mean_latency']}."