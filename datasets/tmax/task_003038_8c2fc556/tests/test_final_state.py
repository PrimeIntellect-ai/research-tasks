# test_final_state.py

import os
import json
import csv
import time
import subprocess
from collections import defaultdict

def compute_expected_weights(data_path, roots):
    """
    Re-derive the expected 2-hop aggregation weights directly from the JSONL file.
    """
    edges = defaultdict(list)
    with open(data_path, 'r') as f:
        for line in f:
            if not line.strip():
                continue
            e = json.loads(line)
            edges[e['src']].append((e['dst'], e['weight']))

    expected = {}
    for r in roots:
        total = 0
        # 2-hop aggregation: weight = hop1.weight + hop2.weight
        for dst1, w1 in edges.get(r, []):
            for dst2, w2 in edges.get(dst1, []):
                total += w1 + w2
        expected[r] = total
    return expected

def test_validation_report_correctness():
    """
    Validates that the generated CSV report matches the expected computed weights.
    """
    report_path = '/home/user/validation_report.csv'
    data_path = '/home/user/graph_export.jsonl'
    roots = [15, 1024, 5000, 9999]

    assert os.path.isfile(report_path), f"Validation report missing at {report_path}."

    expected_weights = compute_expected_weights(data_path, roots)

    actual_weights = {}
    with open(report_path, 'r') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            assert False, "Validation report is empty."

        assert header == ['root_id', 'aggregate_weight'], \
            f"CSV header mismatch. Expected ['root_id', 'aggregate_weight'], got {header}."

        for row in reader:
            if not row:
                continue
            try:
                root_id = int(row[0])
                weight = int(row[1])
                actual_weights[root_id] = weight
            except ValueError:
                assert False, f"Invalid row format in CSV: {row}"

    for r in roots:
        assert r in actual_weights, f"Root {r} missing from validation report."
        assert actual_weights[r] == expected_weights[r], \
            f"Incorrect aggregate weight for root {r}. Expected {expected_weights[r]}, got {actual_weights[r]}."

def test_execution_time_threshold():
    """
    Measures the execution time of the compiled validator tool and asserts it meets the SLA threshold.
    """
    executable = "/app/graph_backup_validator-1.0.0/validator"
    data_path = "/home/user/graph_export.jsonl"

    assert os.path.isfile(executable), f"Executable not found at {executable}. Did you recompile it?"

    start_time = time.time()
    proc = subprocess.run(
        [executable, "--data", data_path, "--roots", "15,1024,5000,9999", "--depth", "2"],
        capture_output=True, text=True
    )
    elapsed = time.time() - start_time

    assert proc.returncode == 0, f"Validator execution failed with return code {proc.returncode}. Stderr: {proc.stderr}"

    threshold = 0.25
    assert elapsed <= threshold, \
        f"Metric Threshold Failed: Execution took {elapsed:.4f}s. Threshold is {threshold}s."