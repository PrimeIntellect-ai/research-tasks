# test_final_state.py

import os
import json
import pytest

def test_cpp_file_exists():
    """Verify that the C++ source file was created at the correct path."""
    cpp_path = '/home/user/tune_and_benchmark.cpp'
    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} is missing."

def test_report_exists_and_format():
    """Verify that the report.json exists and has the required keys."""
    report_path = '/home/user/report.json'
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Report file {report_path} is not valid JSON.")

    assert "best_k" in data, "Missing 'best_k' in report.json."
    assert "best_cv_mse" in data, "Missing 'best_cv_mse' in report.json."
    assert "benchmark_time_microseconds" in data, "Missing 'benchmark_time_microseconds' in report.json."

def test_report_values():
    """Recompute the ground truth for KNN CV MSE and verify the report's values."""
    csv_path = '/home/user/spectra.csv'
    assert os.path.isfile(csv_path), f"Dataset file {csv_path} is missing."

    # Load dataset
    data_rows = []
    with open(csv_path, 'r') as f:
        lines = f.read().strip().split('\n')
        for line in lines[1:]:
            if not line.strip(): continue
            parts = line.split(',')
            data_rows.append({
                'id': int(parts[0]),
                'fold': int(parts[1]),
                'x': float(parts[2]),
                'y': float(parts[3])
            })

    # KNN prediction logic
    def knn_predict(train_data, test_x, k):
        distances = []
        for row in train_data:
            dist = abs(row['x'] - test_x)
            distances.append((dist, row['id'], row['y']))
        # Sort by distance, then by id to break ties
        distances.sort(key=lambda item: (item[0], item[1]))
        top_k = distances[:k]
        return sum(item[2] for item in top_k) / k

    # Compute CV MSE for each K
    mses_by_k = {}
    for k in [1, 3, 5, 7, 9]:
        fold_mses = []
        for fold in [1, 2, 3]:
            train = [r for r in data_rows if r['fold'] != fold]
            test = [r for r in data_rows if r['fold'] == fold]

            sq_errors = []
            for row in test:
                pred = knn_predict(train, row['x'], k)
                sq_errors.append((row['y'] - pred) ** 2)

            fold_mses.append(sum(sq_errors) / len(sq_errors))

        mses_by_k[k] = sum(fold_mses) / len(fold_mses)

    # Determine best K and its MSE
    best_k = min(mses_by_k.keys(), key=lambda k: mses_by_k[k])
    best_mse = mses_by_k[best_k]

    # Validate report
    report_path = '/home/user/report.json'
    with open(report_path, 'r') as f:
        report = json.load(f)

    assert report["best_k"] == best_k, f"Expected best_k to be {best_k}, got {report['best_k']}."

    # The MSE should be rounded to 4 decimal places, allow a small floating point tolerance
    expected_mse_rounded = round(best_mse, 4)
    reported_mse = report["best_cv_mse"]
    assert abs(reported_mse - expected_mse_rounded) < 1e-4 or abs(reported_mse - best_mse) < 1e-4, \
        f"Expected best_cv_mse to be close to {expected_mse_rounded}, got {reported_mse}."

    benchmark_time = report["benchmark_time_microseconds"]
    assert isinstance(benchmark_time, int), "benchmark_time_microseconds should be an integer."
    assert benchmark_time > 0, "benchmark_time_microseconds should be greater than 0."