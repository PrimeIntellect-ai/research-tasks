# test_final_state.py
import json
import os
import csv
import math
import pytest

def test_results_json_exists():
    """Test that the results.json file exists."""
    assert os.path.isfile('/home/user/results.json'), "The file /home/user/results.json was not found."

def test_results_json_structure():
    """Test that results.json contains the correct keys and correctly formatted values."""
    with open('/home/user/results.json', 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("/home/user/results.json is not a valid JSON file.")

    expected_keys = {"dropped_feature", "imputed_target_reg_mean", "classification_accuracy"}
    assert set(results.keys()) == expected_keys, f"JSON keys do not match. Expected {expected_keys}, got {set(results.keys())}."

    # Check formatting of floats (should be 4 decimal places, though we accept floats)
    assert isinstance(results["dropped_feature"], str), "dropped_feature must be a string."

    try:
        float(results["imputed_target_reg_mean"])
    except ValueError:
        pytest.fail("imputed_target_reg_mean is not a valid number.")

    try:
        float(results["classification_accuracy"])
    except ValueError:
        pytest.fail("classification_accuracy is not a valid number.")

def test_dropped_feature_logic():
    """Verify the dropped feature by calculating correlation in pure Python."""
    data_path = '/home/user/data.csv'
    assert os.path.isfile(data_path), f"File {data_path} is missing."

    with open(data_path, 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        data = [row for row in reader]

    # Extract feature columns only
    feature_cols = [c for c in header if c.startswith('feature_')]
    col_indices = {c: header.index(c) for c in feature_cols}

    # Compute means
    n = len(data)
    means = {}
    for c in feature_cols:
        idx = col_indices[c]
        means[c] = sum(float(row[idx]) for row in data) / n

    # Compute standard deviations and covariances
    stds = {}
    for c in feature_cols:
        idx = col_indices[c]
        variance = sum((float(row[idx]) - means[c])**2 for row in data) / n
        stds[c] = math.sqrt(variance)

    # Find highly correlated pair
    correlated_pair = None
    for i in range(len(feature_cols)):
        for j in range(i + 1, len(feature_cols)):
            c1 = feature_cols[i]
            c2 = feature_cols[j]
            idx1 = col_indices[c1]
            idx2 = col_indices[c2]

            cov = sum((float(row[idx1]) - means[c1]) * (float(row[idx2]) - means[c2]) for row in data) / n
            corr = abs(cov / (stds[c1] * stds[c2]))

            if corr > 0.999:
                correlated_pair = (c1, c2)
                break
        if correlated_pair:
            break

    assert correlated_pair is not None, "Could not find a highly correlated pair of features in the dataset."

    # Determine which one to drop (higher index number)
    idx_a = int(correlated_pair[0].split('_')[1])
    idx_b = int(correlated_pair[1].split('_')[1])

    expected_dropped = correlated_pair[0] if idx_a > idx_b else correlated_pair[1]

    with open('/home/user/results.json', 'r') as f:
        results = json.load(f)

    assert results["dropped_feature"] == expected_dropped, f"Expected dropped_feature to be {expected_dropped}, got {results['dropped_feature']}."