# test_final_state.py

import os
import csv

def compute_median(values):
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    if n == 0:
        return 0.0
    if n % 2 == 1:
        return sorted_vals[n // 2]
    else:
        return (sorted_vals[n // 2 - 1] + sorted_vals[n // 2]) / 2.0

def compute_mad(values, median):
    abs_diffs = [abs(v - median) for v in values]
    return compute_median(abs_diffs)

def compute_f1(y_true, y_pred):
    tp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 1)
    fp = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 0 and yp == 1)
    fn = sum(1 for yt, yp in zip(y_true, y_pred) if yt == 1 and yp == 0)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0

    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)

def get_expected_results():
    train_path = '/home/user/train.csv'
    test_path = '/home/user/test.csv'

    train_data = []
    with open(train_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            train_data.append({
                'id': row['id'],
                'value': float(row['value']),
                'is_anomaly': int(row['is_anomaly'])
            })

    test_data = []
    with open(test_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            test_data.append({
                'id': row['id'],
                'value': float(row['value'])
            })

    k_values = [1.0, 1.5, 2.0, 2.5, 3.0]
    fold_size = len(train_data) // 4

    cv_results = []
    k_f1_sums = {k: 0.0 for k in k_values}

    for fold in range(4):
        val_start = fold * fold_size
        val_end = val_start + fold_size

        val_set = train_data[val_start:val_end]
        train_set = train_data[:val_start] + train_data[val_end:]

        train_values = [d['value'] for d in train_set]
        median = compute_median(train_values)
        mad = compute_mad(train_values, median)

        val_values = [d['value'] for d in val_set]
        y_true = [d['is_anomaly'] for d in val_set]

        for k in k_values:
            y_pred = [1 if abs(v - median) > k * mad else 0 for v in val_values]
            f1 = compute_f1(y_true, y_pred)
            cv_results.append((k, fold, f1))
            k_f1_sums[k] += f1

    best_k = None
    best_f1_avg = -1.0
    for k in k_values:
        avg_f1 = k_f1_sums[k] / 4.0
        if avg_f1 > best_f1_avg:
            best_f1_avg = avg_f1
            best_k = k
        elif avg_f1 == best_f1_avg and (best_k is None or k < best_k):
            best_k = k

    all_train_values = [d['value'] for d in train_data]
    global_median = compute_median(all_train_values)
    global_mad = compute_mad(all_train_values, global_median)

    cleaned_test_data = []
    for d in test_data:
        if abs(d['value'] - global_median) <= best_k * global_mad:
            cleaned_test_data.append(d)

    return cv_results, cleaned_test_data

def test_cv_results():
    cv_path = '/home/user/cv_results.csv'
    assert os.path.isfile(cv_path), f"File not found: {cv_path}"

    expected_cv, _ = get_expected_results()

    with open(cv_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['k', 'fold', 'f1_score'], f"Incorrect header in cv_results.csv: {header}"

        rows = list(reader)
        assert len(rows) == len(expected_cv), f"Expected {len(expected_cv)} rows in cv_results.csv, found {len(rows)}"

        # Sort both just in case the order is different, though spec implies sequential
        expected_cv_sorted = sorted(expected_cv, key=lambda x: (x[0], x[1]))

        parsed_rows = []
        for r in rows:
            assert len(r) == 3, f"Expected 3 columns in cv_results.csv, found {len(r)}"
            parsed_rows.append((float(r[0]), int(r[1]), float(r[2])))

        parsed_rows_sorted = sorted(parsed_rows, key=lambda x: (x[0], x[1]))

        for exp, act in zip(expected_cv_sorted, parsed_rows_sorted):
            assert exp[0] == act[0], f"Expected k={exp[0]}, found {act[0]}"
            assert exp[1] == act[1], f"Expected fold={exp[1]}, found {act[1]}"
            assert abs(exp[2] - act[2]) < 1e-4, f"Expected f1_score={exp[2]:.4f} for k={exp[0]} fold={exp[1]}, found {act[2]}"

def test_cleaned_test():
    cleaned_path = '/home/user/cleaned_test.csv'
    assert os.path.isfile(cleaned_path), f"File not found: {cleaned_path}"

    _, expected_cleaned = get_expected_results()

    with open(cleaned_path, 'r', newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['id', 'value'], f"Incorrect header in cleaned_test.csv: {header}"

        rows = list(reader)
        assert len(rows) == len(expected_cleaned), f"Expected {len(expected_cleaned)} rows in cleaned_test.csv, found {len(rows)}"

        expected_ids = [d['id'] for d in expected_cleaned]
        actual_ids = [r[0] for r in rows]

        assert expected_ids == actual_ids, "The IDs in cleaned_test.csv do not match the expected non-anomalous rows."