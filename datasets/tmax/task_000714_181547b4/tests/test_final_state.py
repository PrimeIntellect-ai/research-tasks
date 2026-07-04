# test_final_state.py

import os
import csv
import json
import urllib.request
from urllib.error import URLError

def get_raw_data_stats():
    raw_path = "/home/user/raw_data.csv"
    assert os.path.exists(raw_path), f"Original raw data {raw_path} is missing."

    with open(raw_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    temps = []
    missing_count = 0
    outlier_count = 0

    for row in rows:
        t = row['temperature']
        if t.strip() == '':
            missing_count += 1
        else:
            temps.append(float(t))

        h = float(row['humidity'])
        if h < 0 or h > 100:
            outlier_count += 1

    temps.sort()
    n = len(temps)
    if n % 2 == 1:
        median_temp = temps[n // 2]
    else:
        median_temp = (temps[n // 2 - 1] + temps[n // 2]) / 2.0

    return {
        "missing_count": missing_count,
        "outlier_count": outlier_count,
        "median_temp": median_temp,
        "total_rows": len(rows)
    }

def test_cleaned_data_exists_and_content():
    stats = get_raw_data_stats()
    clean_path = "/home/user/cleaned_data.csv"
    assert os.path.exists(clean_path), f"Cleaned data file {clean_path} does not exist."

    with open(clean_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == ['timestamp', 'temperature', 'humidity'], f"Header is incorrect: {header}"
        rows = list(reader)

    expected_rows = stats["total_rows"] - stats["outlier_count"]
    assert len(rows) == expected_rows, f"Expected {expected_rows} rows in cleaned data, got {len(rows)}."

    imputed_count = 0
    for row in rows:
        temp = float(row[1])
        humidity = float(row[2])

        assert 0 <= humidity <= 100, f"Found outlier humidity value {humidity} in cleaned data."

        if abs(temp - stats["median_temp"]) < 1e-5:
            imputed_count += 1

    # The imputed count should be at least the missing_count (it could be more if original data had the exact median value)
    assert imputed_count >= stats["missing_count"], f"Expected at least {stats['missing_count']} median values in cleaned data, found {imputed_count}."

def test_mlflow_tracking():
    stats = get_raw_data_stats()
    run_id_path = "/home/user/run_id.txt"
    assert os.path.exists(run_id_path), f"Run ID file {run_id_path} does not exist."

    with open(run_id_path, 'r') as f:
        run_id = f.read().strip()

    assert run_id, "Run ID file is empty."

    url = f"http://127.0.0.1:5000/api/2.0/mlflow/runs/get?run_id={run_id}"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
    except URLError as e:
        assert False, f"Failed to connect to MLflow server or retrieve run: {e}"

    assert 'run' in data and 'data' in data['run'] and 'metrics' in data['run']['data'], "Invalid MLflow API response structure."

    metrics = data['run']['data']['metrics']
    metric_dict = {m['key']: m['value'] for m in metrics}

    assert 'missing_imputed' in metric_dict, "Metric 'missing_imputed' was not logged."
    assert metric_dict['missing_imputed'] == stats["missing_count"], f"Expected 'missing_imputed' to be {stats['missing_count']}, got {metric_dict['missing_imputed']}."

    assert 'rows_removed' in metric_dict, "Metric 'rows_removed' was not logged."
    assert metric_dict['rows_removed'] == stats["outlier_count"], f"Expected 'rows_removed' to be {stats['outlier_count']}, got {metric_dict['rows_removed']}."