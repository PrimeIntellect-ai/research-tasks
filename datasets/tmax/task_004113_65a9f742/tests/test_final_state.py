# test_final_state.py

import os
import json
import math
import requests
import pytest
from collections import defaultdict

OUTPUT_FILE = "/home/user/etl_worker/output_clean.jsonl"
STATS_URL = "http://127.0.0.1:9090/stats"

def test_stats_endpoint_is_available_and_valid():
    try:
        resp = requests.get(STATS_URL, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to stats endpoint at {STATS_URL}: {e}")

    assert resp.status_code == 200, f"Expected HTTP 200 OK, got {resp.status_code}"
    assert "application/json" in resp.headers.get("Content-Type", "").lower(), \
        f"Expected Content-Type: application/json, got {resp.headers.get('Content-Type')}"

    try:
        stats = resp.json()
    except ValueError:
        pytest.fail(f"Response body is not valid JSON: {resp.text}")

    assert "total_unique" in stats, "Missing 'total_unique' key in stats response"
    assert "averages" in stats, "Missing 'averages' key in stats response"
    assert "sample_count" in stats, "Missing 'sample_count' key in stats response"

    assert isinstance(stats["total_unique"], int), "'total_unique' must be an integer"
    assert stats["total_unique"] >= 1000, f"Expected at least 1000 unique records processed, got {stats['total_unique']}"

    assert isinstance(stats["averages"], dict), "'averages' must be a dictionary"
    assert isinstance(stats["sample_count"], int), "'sample_count' must be an integer"

def test_output_file_contents_and_consistency():
    assert os.path.isfile(OUTPUT_FILE), f"Output file {OUTPUT_FILE} does not exist. Did the worker write to the correct path?"

    try:
        resp = requests.get(STATS_URL, timeout=5)
        stats = resp.json()
    except Exception as e:
        pytest.fail(f"Failed to fetch stats for consistency check: {e}")

    total_unique_stat = stats["total_unique"]
    sample_count_stat = stats["sample_count"]
    averages_stat = stats["averages"]

    seen_ids = set()
    sampled_count = 0
    category_sums = defaultdict(float)
    category_counts = defaultdict(int)

    line_count = 0
    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            line_count += 1
            try:
                # `json.loads` natively validates UTF-8 correctness in Python 3
                record = json.loads(line)
            except ValueError as e:
                pytest.fail(f"Invalid JSON on line {line_count} of output file: {e}")

            assert "id" in record, f"Missing 'id' field in record on line {line_count}"
            record_id = record["id"]
            assert record_id not in seen_ids, f"Duplicate id found in output: {record_id}. Deduplication failed."
            seen_ids.add(record_id)

            if record.get("sampled") is True:
                sampled_count += 1

            cat = record.get("category")
            val = record.get("value")
            if cat is not None and val is not None:
                category_sums[cat] += float(val)
                category_counts[cat] += 1

    # Assert basic counts match the endpoint
    assert line_count == total_unique_stat, \
        f"Output file has {line_count} lines, but stats endpoint reports {total_unique_stat} total_unique"
    assert sampled_count == sample_count_stat, \
        f"Output file has {sampled_count} sampled records, but stats endpoint reports {sample_count_stat}"

    # Assert ~10% sample logic (allowing a small tolerance for stratification rounding bounds)
    expected_sample = total_unique_stat * 0.1
    assert math.isclose(sampled_count, expected_sample, rel_tol=0.15, abs_tol=10), \
        f"Sample count {sampled_count} is not approximately 10% of total unique records ({total_unique_stat})"

    # Recompute averages and compare with the endpoint's reported averages
    for cat, count in category_counts.items():
        expected_avg = category_sums[cat] / count
        reported_avg = averages_stat.get(cat)
        assert reported_avg is not None, f"Missing average for category '{cat}' in stats endpoint"
        assert math.isclose(expected_avg, float(reported_avg), rel_tol=1e-3), \
            f"Average for category '{cat}' mismatch: expected {expected_avg}, but endpoint reported {reported_avg}"