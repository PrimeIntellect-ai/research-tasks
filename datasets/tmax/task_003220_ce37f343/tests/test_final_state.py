# test_final_state.py
import pytest
import requests
import math

def transpose(M):
    return [[M[j][i] for j in range(len(M))] for i in range(len(M[0]))]

def matmul(A, B):
    return [[sum(a * b for a, b in zip(A_row, B_col)) for B_col in transpose(B)] for A_row in A]

def invert_matrix(M):
    n = len(M)
    A = [row[:] + [1.0 if i == j else 0.0 for j in range(n)] for i, row in enumerate(M)]
    for i in range(n):
        pivot = A[i][i]
        for j in range(2 * n):
            A[i][j] /= pivot
        for k in range(n):
            if k != i:
                factor = A[k][i]
                for j in range(2 * n):
                    A[k][j] -= factor * A[i][j]
    return [row[n:] for row in A]

def compute_expected_values():
    features_raw = [
        [1, 1.5, 2.3, 0.5],
        [2, 2.0, 1.1, -1.2],
        [3, 3.1, 4.5, 1.0],
        [4, 0.5, 0.8, 0.1],
        [5, 4.2, 3.3, -2.5],
        [6, 2.2, 2.2, 2.2],
        [7, 1.8, 4.1, 0.0],
        [8, 5.0, 1.0, 1.0],
        [9, 3.5, 2.9, -0.5],
        [10, 0.1, 0.2, 0.3]
    ]
    targets_raw = [
        [1, 5.6],
        [2, 4.2],
        [3, 11.5],
        [4, 2.0],
        [5, 8.1],
        [6, 7.8],
        [7, 8.0],
        [8, 9.5],
        [9, 7.4],
        [10, 0.5]
    ]

    # Sort and join by customer_id
    features_raw.sort(key=lambda x: x[0])
    targets_raw.sort(key=lambda x: x[0])

    X = [[1.0, row[1], row[2], row[3]] for row in features_raw]
    y = [[row[1]] for row in targets_raw]

    Xt = transpose(X)
    XtX = matmul(Xt, X)
    XtX_inv = invert_matrix(XtX)
    beta = matmul(matmul(XtX_inv, Xt), y)

    y_pred = matmul(X, beta)
    rss = sum((y[i][0] - y_pred[i][0])**2 for i in range(len(y)))
    df = len(y) - len(beta)
    sigma2 = rss / df

    se = [(sigma2 * XtX_inv[i][i])**0.5 for i in range(len(beta))]

    t_crit = 2.4469 # df=6, alpha=0.05

    ci = []
    for i in range(len(beta)):
        ci.append((beta[i][0] - t_crit * se[i], beta[i][0] + t_crit * se[i]))

    return beta, ci

@pytest.fixture(scope="module")
def expected_data():
    beta, ci = compute_expected_values()
    return {
        "beta": [b[0] for b in beta],
        "ci": ci
    }

def test_predict_endpoint(expected_data):
    url = "http://127.0.0.1:8000/predict"
    payload = {"x1": 2.0, "x2": 3.5, "x3": -1.0}
    try:
        response = requests.post(url, json=payload, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "prediction" in data, "Response JSON missing 'prediction' key"

    beta = expected_data["beta"]
    expected_pred = beta[0] + beta[1]*2.0 + beta[2]*3.5 + beta[3]*(-1.0)

    assert math.isclose(data["prediction"], expected_pred, rel_tol=1e-3, abs_tol=1e-3), \
        f"Prediction mismatch. Expected approx {expected_pred}, got {data['prediction']}"

def test_ci_endpoint(expected_data):
    url = "http://127.0.0.1:8000/ci"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    expected_keys = ["intercept", "x1", "x2", "x3"]
    for key in expected_keys:
        assert key in data, f"Response JSON missing key '{key}'"
        assert len(data[key]) == 2, f"Expected 2 values for CI of '{key}'"

    expected_ci = expected_data["ci"]

    for i, key in enumerate(expected_keys):
        lower_expected, upper_expected = expected_ci[i]
        lower_actual, upper_actual = data[key]

        assert math.isclose(lower_actual, lower_expected, rel_tol=1e-2, abs_tol=1e-2), \
            f"CI lower bound mismatch for {key}. Expected approx {lower_expected}, got {lower_actual}"
        assert math.isclose(upper_actual, upper_expected, rel_tol=1e-2, abs_tol=1e-2), \
            f"CI upper bound mismatch for {key}. Expected approx {upper_expected}, got {upper_actual}"