# test_final_state.py

import os
import csv
import json
import math
import pytest

def get_expected_values():
    raw_csv_path = '/home/user/data/raw.csv'
    if not os.path.exists(raw_csv_path):
        return None

    with open(raw_csv_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if len(rows) != 100:
        return None

    train = rows[:80]
    test = rows[80:]

    # LCG
    seed = 42
    indices = []
    for _ in range(80):
        seed = (1103515245 * seed + 12345) % (2**31)
        idx = (seed // 65536) % 80
        indices.append(idx)

    boot_train = [train[i] for i in indices]

    f1_train = [float(r['f1']) for r in boot_train]
    f2_train = [float(r['f2']) for r in boot_train]

    def mean(lst):
        return sum(lst) / len(lst)

    def pop_std(lst, m):
        return math.sqrt(sum((x - m)**2 for x in lst) / len(lst))

    m_f1 = mean(f1_train)
    s_f1 = pop_std(f1_train, m_f1)
    m_f2 = mean(f2_train)
    s_f2 = pop_std(f2_train, m_f2)

    f1_test_scaled = [(float(r['f1']) - m_f1) / s_f1 for r in test]
    f2_test_scaled = [(float(r['f2']) - m_f2) / s_f2 for r in test]

    expected_json = {
        "train_f1_mean": round(m_f1, 4),
        "train_f1_std": round(s_f1, 4),
        "train_f2_mean": round(m_f2, 4),
        "train_f2_std": round(s_f2, 4),
        "test_f1_mean_after_scaling": round(mean(f1_test_scaled), 4),
        "test_f2_mean_after_scaling": round(mean(f2_test_scaled), 4)
    }

    boot_train_scaled = []
    for r in boot_train:
        boot_train_scaled.append({
            'f1': (float(r['f1']) - m_f1) / s_f1,
            'f2': (float(r['f2']) - m_f2) / s_f2,
            'target': r['target']
        })

    test_scaled = []
    for i, r in enumerate(test):
        test_scaled.append({
            'f1': f1_test_scaled[i],
            'f2': f2_test_scaled[i],
            'target': r['target']
        })

    return expected_json, boot_train_scaled, test_scaled


def test_experiment_log():
    expected_data = get_expected_values()
    assert expected_data is not None, "Could not compute expected values; raw.csv is missing or invalid."
    expected_json, _, _ = expected_data

    log_path = '/home/user/experiment_log.json'
    assert os.path.isfile(log_path), f"Experiment log missing at {log_path}"

    with open(log_path, 'r') as f:
        try:
            actual_json = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("experiment_log.json is not valid JSON.")

    for key, expected_val in expected_json.items():
        assert key in actual_json, f"Key '{key}' missing in experiment_log.json"
        actual_val = actual_json[key]
        assert isinstance(actual_val, (int, float)), f"Value for '{key}' must be a number."
        assert math.isclose(actual_val, expected_val, abs_tol=1e-4), \
            f"Expected {key} to be {expected_val}, got {actual_val}"


def test_train_scaled_csv():
    expected_data = get_expected_values()
    assert expected_data is not None, "Could not compute expected values."
    _, expected_train_scaled, _ = expected_data

    train_scaled_path = '/home/user/data/train_scaled.csv'
    assert os.path.isfile(train_scaled_path), f"Scaled train file missing at {train_scaled_path}"

    with open(train_scaled_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 80, f"Expected 80 rows in train_scaled.csv, got {len(rows)}"
    assert reader.fieldnames == ['f1', 'f2', 'target'], "Header format in train_scaled.csv is incorrect"

    for i, (actual, expected) in enumerate(zip(rows, expected_train_scaled)):
        assert math.isclose(float(actual['f1']), expected['f1'], abs_tol=1e-3), f"Row {i} f1 mismatch in train_scaled.csv"
        assert math.isclose(float(actual['f2']), expected['f2'], abs_tol=1e-3), f"Row {i} f2 mismatch in train_scaled.csv"
        assert actual['target'] == expected['target'], f"Row {i} target mismatch in train_scaled.csv"


def test_test_scaled_csv():
    expected_data = get_expected_values()
    assert expected_data is not None, "Could not compute expected values."
    _, _, expected_test_scaled = expected_data

    test_scaled_path = '/home/user/data/test_scaled.csv'
    assert os.path.isfile(test_scaled_path), f"Scaled test file missing at {test_scaled_path}"

    with open(test_scaled_path, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    assert len(rows) == 20, f"Expected 20 rows in test_scaled.csv, got {len(rows)}"
    assert reader.fieldnames == ['f1', 'f2', 'target'], "Header format in test_scaled.csv is incorrect"

    for i, (actual, expected) in enumerate(zip(rows, expected_test_scaled)):
        assert math.isclose(float(actual['f1']), expected['f1'], abs_tol=1e-3), f"Row {i} f1 mismatch in test_scaled.csv"
        assert math.isclose(float(actual['f2']), expected['f2'], abs_tol=1e-3), f"Row {i} f2 mismatch in test_scaled.csv"
        assert actual['target'] == expected['target'], f"Row {i} target mismatch in test_scaled.csv"