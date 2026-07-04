# test_final_state.py
import os
import csv
import json
import math

def test_fit_results_and_plot():
    csv_path = '/home/user/detector_events.csv'
    json_path = '/home/user/fit_results.json'
    plot_path = '/home/user/fit_plot.png'

    # 1. Verify CSV exists and compute expected values using standard library
    assert os.path.exists(csv_path), f"Input file {csv_path} is missing."

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        timestamps = [float(row['timestamp']) for row in reader]

    assert len(timestamps) > 1, "Not enough timestamps to compute intervals."

    diffs = [timestamps[i] - timestamps[i-1] for i in range(1, len(timestamps))]

    # Compute lambda (1 / mean)
    mean_diff = sum(diffs) / len(diffs)
    expected_lambda = 1.0 / mean_diff

    # Compute KS statistic manually
    diffs.sort()
    n = len(diffs)
    expected_ks = 0.0
    for i, x in enumerate(diffs):
        # Theoretical CDF for exponential distribution
        cdf_x = 1.0 - math.exp(-expected_lambda * x)

        # Empirical CDF jumps at x
        ecdf_prev = i / n
        ecdf_next = (i + 1) / n

        # KS stat is the maximum distance
        ks_prev = abs(ecdf_prev - cdf_x)
        ks_next = abs(ecdf_next - cdf_x)
        expected_ks = max(expected_ks, ks_prev, ks_next)

    # 2. Verify JSON results
    assert os.path.exists(json_path), f"Results file {json_path} is missing."

    with open(json_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} is not a valid JSON file."

    assert 'lambda' in results, "'lambda' key missing from JSON."
    assert 'ks_stat' in results, "'ks_stat' key missing from JSON."

    actual_lambda = results['lambda']
    actual_ks = results['ks_stat']

    expected_lambda_rounded = round(expected_lambda, 4)
    expected_ks_rounded = round(expected_ks, 4)

    assert abs(actual_lambda - expected_lambda_rounded) <= 1e-4, \
        f"Expected lambda to be approximately {expected_lambda_rounded}, but got {actual_lambda}"

    assert abs(actual_ks - expected_ks_rounded) <= 1e-4, \
        f"Expected ks_stat to be approximately {expected_ks_rounded}, but got {actual_ks}"

    # 3. Verify Plot
    assert os.path.exists(plot_path), f"Plot file {plot_path} is missing."
    assert os.path.getsize(plot_path) > 0, f"Plot file {plot_path} is empty."

    # Verify it is a valid PNG file by checking the magic number
    with open(plot_path, 'rb') as f:
        header = f.read(8)
        assert header == b'\x89PNG\r\n\x1a\n', f"File {plot_path} is not a valid PNG image."