# test_final_state.py
import requests
import pytest

def get_A():
    return [[0.98, 0.05],
            [-0.05, 0.98]]

def mat_mul(A, B):
    return [
        [A[0][0]*B[0][0] + A[0][1]*B[1][0], A[0][0]*B[0][1] + A[0][1]*B[1][1]],
        [A[1][0]*B[0][0] + A[1][1]*B[1][0], A[1][0]*B[0][1] + A[1][1]*B[1][1]]
    ]

def mat_vec_mul(A, V):
    return [
        A[0][0]*V[0] + A[0][1]*V[1],
        A[1][0]*V[0] + A[1][1]*V[1]
    ]

def mat_pow(A, n):
    res = [[1, 0], [0, 1]]
    base = A
    while n > 0:
        if n % 2 == 1:
            res = mat_mul(res, base)
        base = mat_mul(base, base)
        n //= 2
    return res

def test_matrix_endpoint():
    try:
        resp = requests.get("http://127.0.0.1:8080/matrix", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the matrix endpoint: {e}")

    assert resp.status_code == 200, f"Expected status 200, got {resp.status_code}"
    try:
        data = resp.json()
    except ValueError:
        pytest.fail("Matrix response is not valid JSON")

    expected_A = get_A()
    assert "a11" in data and "a12" in data and "a21" in data and "a22" in data, "Matrix response missing required keys"

    assert abs(data["a11"] - expected_A[0][0]) < 0.05, f"a11 expected ~{expected_A[0][0]}, got {data['a11']}"
    assert abs(data["a12"] - expected_A[0][1]) < 0.05, f"a12 expected ~{expected_A[0][1]}, got {data['a12']}"
    assert abs(data["a21"] - expected_A[1][0]) < 0.05, f"a21 expected ~{expected_A[1][0]}, got {data['a21']}"
    assert abs(data["a22"] - expected_A[1][1]) < 0.05, f"a22 expected ~{expected_A[1][1]}, got {data['a22']}"

@pytest.mark.parametrize("t", [10, 50])
def test_predict_endpoint(t):
    try:
        resp = requests.get(f"http://127.0.0.1:8080/predict?t={t}", timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the predict endpoint: {e}")

    assert resp.status_code == 200, f"Expected status 200, got {resp.status_code}"
    try:
        data = resp.json()
    except ValueError:
        pytest.fail("Predict response is not valid JSON")

    assert "x" in data and "y" in data, "Predict response missing required keys"

    A = get_A()
    X0 = [100.0, 50.0]
    A_t = mat_pow(A, t)
    expected_X = mat_vec_mul(A_t, X0)

    assert abs(data["x"] - expected_X[0]) < 5.0, f"x at t={t} expected ~{expected_X[0]}, got {data['x']}"
    assert abs(data["y"] - expected_X[1]) < 5.0, f"y at t={t} expected ~{expected_X[1]}, got {data['y']}"