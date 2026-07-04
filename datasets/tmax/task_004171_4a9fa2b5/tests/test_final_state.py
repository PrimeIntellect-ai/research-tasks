# test_final_state.py
import csv
import os
import math

TRAIN_CSV = '/home/user/train_clean.csv'
TEST_CSV = '/home/user/test_clean.csv'

def read_csv(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def test_output_files_exist():
    assert os.path.exists(TRAIN_CSV), f"Expected output file not found: {TRAIN_CSV}"
    assert os.path.exists(TEST_CSV), f"Expected output file not found: {TEST_CSV}"

def test_row_counts():
    train_data = read_csv(TRAIN_CSV)
    test_data = read_csv(TEST_CSV)

    assert len(train_data) == 8, f"Expected 8 rows in train_clean.csv, found {len(train_data)}"
    assert len(test_data) == 3, f"Expected 3 rows in test_clean.csv, found {len(test_data)}"

def test_rounding_to_4_decimal_places():
    for filepath in [TRAIN_CSV, TEST_CSV]:
        data = read_csv(filepath)
        for i, row in enumerate(data):
            for col in ['age', 'income']:
                val_str = row[col]
                if '.' in val_str:
                    decimals = len(val_str.split('.')[1])
                    assert decimals <= 4, f"Value '{val_str}' in {col} (row {i}) is not rounded to 4 decimal places in {filepath}"

def test_train_mean_is_zero():
    train_data = read_csv(TRAIN_CSV)

    age_sum = sum(float(row['age']) for row in train_data)
    income_sum = sum(float(row['income']) for row in train_data)

    age_mean = age_sum / len(train_data)
    income_mean = income_sum / len(train_data)

    assert math.isclose(age_mean, 0.0, abs_tol=1e-3), f"Mean of 'age' in train set is {age_mean}, expected ~0.0. Scaler was likely not fit correctly."
    assert math.isclose(income_mean, 0.0, abs_tol=1e-3), f"Mean of 'income' in train set is {income_mean}, expected ~0.0. Scaler was likely not fit correctly."

def test_test_mean_is_not_zero():
    test_data = read_csv(TEST_CSV)

    age_sum = sum(float(row['age']) for row in test_data)

    age_mean = age_sum / len(test_data)

    assert not math.isclose(age_mean, 0.0, abs_tol=1e-3), f"Mean of 'age' in test set is {age_mean}, which is too close to 0.0. Scaler might have been fit on the test set (data leakage)."