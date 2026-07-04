# test_final_state.py

import csv
import math
import requests
import pytest

def compute_expected_correlation(csv_path):
    data = []
    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            data.append([float(x) for x in row])

    n_cols = len(data[0])
    cols = [[row[i] for row in data] for i in range(n_cols)]

    matrix = []
    for i in range(n_cols):
        row_corr = []
        for j in range(n_cols):
            x = cols[i]
            y = cols[j]
            n = len(x)
            mean_x = sum(x) / n
            mean_y = sum(y) / n
            num = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
            den = math.sqrt(sum((xi - mean_x)**2 for xi in x) * sum((yi - mean_y)**2 for yi in y))
            corr = num / den if den != 0 else 0.0
            row_corr.append(corr)
        matrix.append(row_corr)
    return matrix

def test_correlation_endpoint():
    """Test that GET /correlation returns the correct 4x4 Pearson correlation matrix."""
    try:
        response = requests.get("http://127.0.0.1:8080/correlation", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the web service at 127.0.0.1:8080/correlation: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        actual_matrix = response.json()
    except ValueError:
        pytest.fail("Response from /correlation is not valid JSON")

    assert isinstance(actual_matrix, list), "Expected JSON array of arrays"
    assert len(actual_matrix) == 4, f"Expected 4 rows in correlation matrix, got {len(actual_matrix)}"

    expected_matrix = compute_expected_correlation("/app/data.csv")

    for i in range(4):
        assert isinstance(actual_matrix[i], list), f"Row {i} is not a list"
        assert len(actual_matrix[i]) == 4, f"Expected 4 columns in row {i}, got {len(actual_matrix[i])}"
        for j in range(4):
            expected_val = expected_matrix[i][j]
            actual_val = actual_matrix[i][j]
            assert math.isclose(actual_val, expected_val, rel_tol=1e-3, abs_tol=1e-3), \
                f"Mismatch at ({i}, {j}): expected {expected_val}, got {actual_val}"

def test_tune_endpoint():
    """Test that GET /tune returns the correct best_lambda and k_folds."""
    try:
        response = requests.get("http://127.0.0.1:8080/tune", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the web service at 127.0.0.1:8080/tune: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("Response from /tune is not valid JSON")

    assert isinstance(data, dict), "Expected JSON object"
    assert "best_lambda" in data, "Missing 'best_lambda' in response"
    assert "k_folds" in data, "Missing 'k_folds' in response"

    assert data["k_folds"] == 5, f"Expected k_folds to be 5, got {data['k_folds']}"
    assert math.isclose(data["best_lambda"], 0.5, rel_tol=1e-3, abs_tol=1e-3), \
        f"Expected best_lambda to be 0.5, got {data['best_lambda']}"