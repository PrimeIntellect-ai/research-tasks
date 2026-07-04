# test_final_state.py

import os
import csv
import pytest

def compute_expected_best_model(data_path):
    if not os.path.exists(data_path):
        pytest.fail(f"Input data file {data_path} is missing.")

    cleaned_data = []
    with open(data_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) < 4:
                continue
            sensor_value_str = row[2].strip()
            if sensor_value_str == "" or sensor_value_str == "NA":
                continue
            try:
                sensor_value = float(sensor_value_str)
            except ValueError:
                continue
            if sensor_value < 0:
                continue

            is_anomaly = int(row[3].strip())
            cleaned_data.append((sensor_value, is_anomaly))

    folds = {0: [], 1: [], 2: []}
    for idx, row in enumerate(cleaned_data):
        fold_idx = idx % 3
        folds[fold_idx].append(row)

    thresholds = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    best_t = None
    best_acc = -1.0

    for t in thresholds:
        fold_accuracies = []
        for i in range(3):
            val_set = folds[i]
            if not val_set:
                continue
            correct = 0
            for val, true_label in val_set:
                pred = 1 if val >= t else 0
                if pred == true_label:
                    correct += 1
            acc = correct / len(val_set)
            fold_accuracies.append(acc)

        if len(fold_accuracies) == 3:
            avg_acc = sum(fold_accuracies) / 3.0
        else:
            avg_acc = 0.0

        if avg_acc > best_acc:
            best_acc = avg_acc
            best_t = t
        elif avg_acc == best_acc:
            if best_t is None or t < best_t:
                best_t = t

    return best_t, best_acc

def test_best_model_output():
    """Test that the best_model.csv file exists and contains the correct dynamically computed threshold and accuracy."""
    data_path = "/home/user/sensor_data.csv"
    output_path = "/home/user/best_model.csv"

    expected_t, expected_acc = compute_expected_best_model(data_path)
    expected_line = f"{expected_t},{expected_acc:.4f}"

    assert os.path.isfile(output_path), f"Output file {output_path} is missing."

    with open(output_path, 'r') as f:
        content = f.read().strip()

    assert content == expected_line, f"Expected '{expected_line}' in {output_path}, but got '{content}'."