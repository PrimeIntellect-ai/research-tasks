# test_final_state.py
import math
import requests

def test_nginx_proxy_and_inference_math():
    url = "http://127.0.0.1:80/api/predict?x=3.0"

    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        raise AssertionError(f"Failed to connect to Nginx at {url}: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        raise AssertionError(f"Expected JSON response, got: {response.text}")

    assert "mean" in data, f"Response JSON missing 'mean' field: {data}"
    assert "variance" in data, f"Response JSON missing 'variance' field: {data}"

    # Calculate truth locally
    # Dataset: (1.0, 2.1), (2.0, 3.9), (1.5, 3.2), (3.0, 6.0)
    # noise_var = 2.0, prior_var = 1.0, prior_mean = 0.0
    x_vals = [1.0, 2.0, 1.5, 3.0]
    y_vals = [2.1, 3.9, 3.2, 6.0]
    noise_var = 2.0
    prior_var = 1.0

    sum_xx = sum(x**2 / noise_var for x in x_vals)
    sum_xy = sum(x*y / noise_var for x, y in zip(x_vals, y_vals))

    post_var = 1.0 / ((1.0 / prior_var) + sum_xx)
    post_mean = post_var * sum_xy

    x_star = 3.0
    expected_mean = post_mean * x_star
    expected_var = (x_star**2 * post_var) + noise_var

    actual_mean = data["mean"]
    actual_var = data["variance"]

    assert math.isclose(actual_mean, expected_mean, rel_tol=1e-4), \
        f"Predictive mean is incorrect. Expected ~{expected_mean:.5f}, got {actual_mean}"

    assert math.isclose(actual_var, expected_var, rel_tol=1e-4), \
        f"Predictive variance is incorrect. Expected ~{expected_var:.5f}, got {actual_var}"