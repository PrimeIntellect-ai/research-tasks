# test_final_state.py
import os
import csv

def test_executable_exists():
    executable_path = "/home/user/experiment/evaluate"
    assert os.path.isfile(executable_path), "The compiled executable 'evaluate' does not exist. Did you run make?"
    assert os.access(executable_path, os.X_OK), "The file 'evaluate' is not executable."

def test_metrics_report():
    report_path = "/home/user/experiment/metrics_report.txt"
    assert os.path.isfile(report_path), f"The file {report_path} does not exist. Did the program run and generate it?"

    # Read truth and preds to compute expected logically
    truth_path = "/home/user/experiment/truth.csv"
    preds_path = "/home/user/experiment/preds.csv"

    assert os.path.isfile(truth_path), "truth.csv is missing."
    assert os.path.isfile(preds_path), "preds.csv is missing."

    truth_data = {}
    with open(truth_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            truth_data[int(row['id'])] = float(row['value'])

    preds_data = {}
    with open(preds_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            preds_data[int(row['id'])] = float(row['value'])

    matched_ids = set(truth_data.keys()).intersection(set(preds_data.keys()))
    assert len(matched_ids) > 0, "No matching IDs found between truth and predictions."

    sq_errors = []
    correct = 0
    for i in matched_ids:
        t = truth_data[i]
        p = preds_data[i]
        sq_errors.append((t - p) ** 2)

        t_class = 1 if t >= 0.5 else 0
        p_class = 1 if p >= 0.5 else 0
        if t_class == p_class:
            correct += 1

    expected_samples = len(matched_ids)
    expected_mse = sum(sq_errors) / expected_samples if expected_samples > 0 else 0.0
    expected_accuracy = correct / expected_samples if expected_samples > 0 else 0.0

    with open(report_path, 'r') as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.split('\n') if line.strip()]
    assert len(lines) == 3, f"metrics_report.txt should have exactly 3 lines, but found {len(lines)}."

    expected_line1 = f"Total Samples: {expected_samples}"
    expected_line2 = f"MSE: {expected_mse:.4f}"
    expected_line3 = f"Accuracy: {expected_accuracy:.4f}"

    assert lines[0] == expected_line1, f"Line 1 mismatch. Expected '{expected_line1}', got '{lines[0]}'"
    assert lines[1] == expected_line2, f"Line 2 mismatch. Expected '{expected_line2}', got '{lines[1]}'"
    assert lines[2] == expected_line3, f"Line 3 mismatch. Expected '{expected_line3}', got '{lines[2]}'"