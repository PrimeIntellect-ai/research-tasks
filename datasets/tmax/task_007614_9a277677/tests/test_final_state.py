# test_final_state.py

import os
import csv
import math

def get_input_data():
    input_path = '/home/user/input.csv'
    assert os.path.exists(input_path), f"Input file {input_path} is missing."
    with open(input_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def compute_expected():
    data = get_input_data()
    total_rows = len(data)
    train_size = int(total_rows * 0.8)

    train_data = data[:train_size]
    test_data = data[train_size:]

    # Calculate train mean
    train_known_values = [float(row['sensor_value']) for row in train_data if row['sensor_value'].strip() != '']
    train_mean = sum(train_known_values) / len(train_known_values)

    # Calculate train std dev (population)
    variance = sum((x - train_mean) ** 2 for x in train_known_values) / len(train_known_values)
    train_std = math.sqrt(variance)

    upper_bound = train_mean + 2 * train_std
    lower_bound = train_mean - 2 * train_std

    def process_row(row):
        word_count = len(row['text_log'].split())

        if row['sensor_value'].strip() == '':
            sensor_value = train_mean
        else:
            sensor_value = float(row['sensor_value'])

        is_outlier = 1 if (sensor_value > upper_bound or sensor_value < lower_bound) else 0

        return {
            'id': row['id'],
            'word_count': str(word_count),
            'sensor_value': sensor_value,
            'is_outlier': str(is_outlier)
        }

    expected_train = [process_row(row) for row in train_data]
    expected_test = [process_row(row) for row in test_data]

    return expected_train, expected_test

def check_csv_file(path, expected_rows):
    assert os.path.exists(path), f"Output file {path} is missing."
    with open(path, 'r', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))

    assert len(reader) == len(expected_rows), f"Row count mismatch in {path}. Expected {len(expected_rows)}, got {len(reader)}."

    expected_headers = ['id', 'word_count', 'sensor_value', 'is_outlier']
    if len(reader) > 0:
        assert list(reader[0].keys()) == expected_headers, f"Column headers mismatch in {path}. Expected {expected_headers}."

    for act, exp in zip(reader, expected_rows):
        assert act['id'] == exp['id'], f"ID mismatch in {path}: expected {exp['id']}, got {act['id']}"
        assert act['word_count'] == exp['word_count'], f"word_count mismatch for ID {act['id']} in {path}: expected {exp['word_count']}, got {act['word_count']}"
        assert act['is_outlier'] == exp['is_outlier'], f"is_outlier mismatch for ID {act['id']} in {path}: expected {exp['is_outlier']}, got {act['is_outlier']}"

        act_val = float(act['sensor_value'])
        exp_val = float(exp['sensor_value'])
        assert abs(act_val - exp_val) <= 0.001, f"sensor_value mismatch for ID {act['id']} in {path}: expected {exp_val:.4f}, got {act_val:.4f}"

def test_train_processed():
    expected_train, _ = compute_expected()
    check_csv_file('/home/user/train_processed.csv', expected_train)

def test_test_processed():
    _, expected_test = compute_expected()
    check_csv_file('/home/user/test_processed.csv', expected_test)

def test_train_bootstrapped():
    expected_train, _ = compute_expected()
    path = '/home/user/train_bootstrapped.csv'
    assert os.path.exists(path), f"Output file {path} is missing."

    with open(path, 'r', encoding='utf-8') as f:
        reader = list(csv.DictReader(f))

    assert len(reader) == len(expected_train), f"Row count mismatch in {path}. Expected {len(expected_train)}, got {len(reader)}."

    expected_headers = ['id', 'word_count', 'sensor_value', 'is_outlier']
    if len(reader) > 0:
        assert list(reader[0].keys()) == expected_headers, f"Column headers mismatch in {path}. Expected {expected_headers}."

    # Build a set of valid expected rows for easy checking
    expected_rows_dict = {row['id']: row for row in expected_train}

    for act in reader:
        act_id = act['id']
        assert act_id in expected_rows_dict, f"Unknown ID {act_id} found in {path}. Bootstrapped rows must come from the training set."

        exp = expected_rows_dict[act_id]
        assert act['word_count'] == exp['word_count'], f"word_count mismatch for ID {act_id} in {path}"
        assert act['is_outlier'] == exp['is_outlier'], f"is_outlier mismatch for ID {act_id} in {path}"

        act_val = float(act['sensor_value'])
        exp_val = float(exp['sensor_value'])
        assert abs(act_val - exp_val) <= 0.001, f"sensor_value mismatch for ID {act_id} in {path}"