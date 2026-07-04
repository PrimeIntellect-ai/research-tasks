# test_final_state.py
import os
import json
import csv
import re
import pytest

def get_expected_top_experiments():
    # 1. Read config
    configs = set()
    with open('/home/user/experiments.jsonl', 'r') as f:
        for line in f:
            if not line.strip(): continue
            data = json.loads(line)
            configs.add(data['experiment_id'])

    # 2. Read metrics
    metrics = {}
    with open('/home/user/metrics.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            metrics[row['experiment_id']] = {
                'final_loss': float(row['final_loss']),
                'final_accuracy': float(row['final_accuracy'])
            }

    # 3. Read logs
    logs = {}
    with open('/home/user/logs.txt', 'r') as f:
        for line in f:
            match = re.match(r'^\[exp_id:\s*(EXP_\d+)\]\s*(.*)', line)
            if match:
                exp_id = match.group(1)
                msg = match.group(2).lower()
                tokens = re.findall(r'\b[a-z]+\b', msg)
                error_count = tokens.count('error')
                warning_count = tokens.count('warning')

                if exp_id not in logs:
                    logs[exp_id] = {'error_count': 0, 'warning_count': 0}
                logs[exp_id]['error_count'] += error_count
                logs[exp_id]['warning_count'] += warning_count

    # 4. Join and compute stability_score
    scores = []
    for exp_id in configs:
        if exp_id in metrics and exp_id in logs:
            acc = metrics[exp_id]['final_accuracy']
            loss = metrics[exp_id]['final_loss']
            err = logs[exp_id]['error_count']
            warn = logs[exp_id]['warning_count']

            score = acc / (loss + 1e-5) - (0.1 * err) - (0.05 * warn)
            scores.append((exp_id, score))

    # Sort descending by score
    scores.sort(key=lambda x: x[1], reverse=True)
    return [x[0] for x in scores[:3]]

def test_etl_pipeline_exists_and_configured():
    path = "/home/user/etl_pipeline.py"
    assert os.path.exists(path), f"ETL script not found at {path}"

    with open(path, "r") as f:
        content = f.read()

    assert "OMP_NUM_THREADS" in content, "The environment variable OMP_NUM_THREADS was not found in the ETL script."

def test_parquet_file_created_and_valid():
    path = "/home/user/consolidated_artifacts.parquet"
    assert os.path.exists(path), f"Parquet output file not found at {path}"
    assert os.path.getsize(path) > 0, "Parquet file is empty."

    # Check Parquet magic bytes
    with open(path, "rb") as f:
        magic = f.read(4)
    assert magic == b"PAR1", f"File {path} does not appear to be a valid Parquet file (missing PAR1 magic bytes)."

def test_top_experiments_output():
    path = "/home/user/top_experiments.txt"
    assert os.path.exists(path), f"Top experiments output file not found at {path}"

    with open(path, "r") as f:
        actual_top = [line.strip() for line in f if line.strip()]

    expected_top = get_expected_top_experiments()

    assert len(actual_top) == 3, f"Expected exactly 3 top experiments, found {len(actual_top)}."
    assert actual_top == expected_top, f"Top experiments mismatch. Expected {expected_top}, got {actual_top}."