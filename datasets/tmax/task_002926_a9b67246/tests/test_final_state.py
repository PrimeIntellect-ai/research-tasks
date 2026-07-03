# test_final_state.py

import os
import math
import stat
import pytest

def test_normalized_files_exist():
    assert os.path.isfile('/home/user/data/train_normalized.csv'), "/home/user/data/train_normalized.csv is missing"
    assert os.path.isfile('/home/user/data/test_normalized.csv'), "/home/user/data/test_normalized.csv is missing"

def test_normalization_logic():
    # Read the original documents to compute truth dynamically
    docs_path = '/home/user/data/documents.csv'
    assert os.path.isfile(docs_path), f"{docs_path} is missing"

    with open(docs_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    header = lines[0]
    data = lines[1:]

    total_lines = len(data)
    train_lines = int(total_lines * 0.8)

    train_data = data[:train_lines]
    test_data = data[train_lines:]

    # Compute max words from TRAIN set only
    max_words_train = 0
    for row in train_data:
        parts = row.split(',')
        if len(parts) >= 2:
            text = parts[1]
            word_count = len(text.split())
            if word_count > max_words_train:
                max_words_train = max_words_train
                max_words_train = word_count

    assert max_words_train > 0, "Could not compute max words from training data"

    # Validate test_normalized.csv
    with open('/home/user/data/test_normalized.csv', 'r') as f:
        test_norm_lines = [line.strip() for line in f if line.strip()]

    assert len(test_norm_lines) == len(test_data), "test_normalized.csv does not have the correct number of rows"

    expected_test_x = []
    expected_test_y = []

    for i, row in enumerate(test_data):
        parts = row.split(',')
        doc_id = parts[0]
        text = parts[1]
        label = parts[2]
        word_count = len(text.split())

        expected_norm = word_count / max_words_train

        norm_parts = test_norm_lines[i].split()
        assert len(norm_parts) == 3, f"test_normalized.csv row {i+1} does not have exactly 3 space-separated columns"

        assert norm_parts[0] == doc_id, f"test_normalized.csv row {i+1} ID mismatch"
        assert norm_parts[2] == label, f"test_normalized.csv row {i+1} label mismatch"

        actual_norm = float(norm_parts[1])
        assert math.isclose(actual_norm, expected_norm, rel_tol=1e-4), f"test_normalized.csv row {i+1} has incorrect normalized word count. Expected {expected_norm}, got {actual_norm}. Leakage might not be fixed."

        expected_test_x.append(expected_norm)
        expected_test_y.append(float(label))

def test_validate_script_exists_and_executable():
    script_path = '/home/user/validate.sh'
    assert os.path.isfile(script_path), f"{script_path} is missing"
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable"

def test_covariance_result():
    result_path = '/home/user/covariance_result.txt'
    assert os.path.isfile(result_path), f"{result_path} is missing. Did you run validate.sh?"

    # Dynamically compute expected covariance based on test_normalized.csv
    # We read test_normalized.csv directly to ensure covariance matches the file's contents
    test_norm_path = '/home/user/data/test_normalized.csv'
    x_vals = []
    y_vals = []
    with open(test_norm_path, 'r') as f:
        for line in f:
            if not line.strip(): continue
            parts = line.strip().split()
            x_vals.append(float(parts[1]))
            y_vals.append(float(parts[2]))

    n = len(x_vals)
    assert n > 0, "test_normalized.csv is empty"

    mean_x = sum(x_vals) / n
    mean_y = sum(y_vals) / n

    sum_xy = sum(x * y for x, y in zip(x_vals, y_vals))
    expected_cov = (sum_xy / n) - (mean_x * mean_y)

    with open(result_path, 'r') as f:
        content = f.read().strip()

    try:
        actual_cov = float(content)
    except ValueError:
        pytest.fail(f"Content of {result_path} is not a valid number: {content}")

    assert math.isclose(actual_cov, expected_cov, abs_tol=1e-4), f"Covariance in {result_path} ({actual_cov}) does not match expected population covariance ({expected_cov:.4f})"