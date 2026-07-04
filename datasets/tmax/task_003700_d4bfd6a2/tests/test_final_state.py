# test_final_state.py
import os
import csv
import re

def test_report_exists_and_correct():
    dataset_path = '/home/user/dataset.csv'
    report_path = '/home/user/report.txt'

    assert os.path.isfile(dataset_path), f"File {dataset_path} does not exist."
    assert os.path.isfile(report_path), f"File {report_path} does not exist."

    # Parse dataset and compute expected values
    valid_f1_sum = 0
    valid_count = 0
    rows = []

    with open(dataset_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            f1_str = row['f1']
            y = float(row['y'])
            if f1_str == "NaN":
                rows.append({'f1': None, 'y': y})
            else:
                f1_val = int(f1_str)
                valid_f1_sum += f1_val
                valid_count += 1
                rows.append({'f1': f1_val, 'y': y})

    assert valid_count > 0, "No valid f1 values found in the dataset."
    expected_imputed_mean = valid_f1_sum // valid_count

    # Compute MSE for the 3 models
    models = [
        {'id': 1, 'w': 1.2e-10, 'b': 0.5},
        {'id': 2, 'w': 1.5e-10, 'b': -0.2},
        {'id': 3, 'w': 1.3e-10, 'b': 0.1},
    ]

    best_model = None
    best_mse = float('inf')

    for model in models:
        mse_sum = 0.0
        for r in rows:
            f1 = expected_imputed_mean if r['f1'] is None else r['f1']
            y_pred = f1 * model['w'] + model['b']
            mse_sum += (y_pred - r['y']) ** 2
        mse = mse_sum / len(rows)
        if mse < best_mse:
            best_mse = mse
            best_model = model['id']

    expected_best_mse_str = f"{best_mse:.4f}"

    # Read and parse the report
    with open(report_path, 'r') as f:
        report_content = f.read().strip().split('\n')

    assert len(report_content) == 4, f"Report should contain exactly 4 lines, found {len(report_content)}."

    # Line 1: Imputed Mean
    match_mean = re.match(r"^Imputed Mean:\s*(-?\d+)$", report_content[0].strip())
    assert match_mean, f"First line format incorrect. Expected 'Imputed Mean: <exact_integer_mean>', got: {report_content[0]}"
    reported_mean = int(match_mean.group(1))
    assert reported_mean == expected_imputed_mean, f"Imputed Mean is incorrect. Expected {expected_imputed_mean}, got {reported_mean}. Check for integer overflow or precision loss."

    # Line 2: Best Model
    match_model = re.match(r"^Best Model:\s*(\d+)$", report_content[1].strip())
    assert match_model, f"Second line format incorrect. Expected 'Best Model: <1, 2, or 3>', got: {report_content[1]}"
    reported_model = int(match_model.group(1))
    assert reported_model == best_model, f"Best Model is incorrect. Expected {best_model}, got {reported_model}."

    # Line 3: Best MSE
    match_mse = re.match(r"^Best MSE:\s*(\d+\.\d{4})$", report_content[2].strip())
    assert match_mse, f"Third line format incorrect. Expected 'Best MSE: <MSE_rounded_to_4_decimal_places>', got: {report_content[2]}"
    reported_mse = match_mse.group(1)

    # Allow a small tolerance in string formatting / float precision
    assert abs(float(reported_mse) - best_mse) < 0.0002, f"Best MSE is incorrect. Expected around {expected_best_mse_str}, got {reported_mse}."

    # Line 4: Benchmark Time
    match_time = re.match(r"^Benchmark Time:\s*(\d+(?:\.\d+)?)\s*ms$", report_content[3].strip())
    assert match_time, f"Fourth line format incorrect. Expected 'Benchmark Time: <total_time_in_milliseconds> ms', got: {report_content[3]}"