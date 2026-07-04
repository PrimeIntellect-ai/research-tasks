# test_final_state.py

import os
import pytest
import requests
import time

def test_compiled_executable_exists():
    assert os.path.isfile("/app/seq_stats"), "The C program was not compiled to /app/seq_stats."
    assert os.access("/app/seq_stats", os.X_OK), "/app/seq_stats is not executable."

def test_gc_data_exists():
    assert os.path.isfile("/app/gc_data.txt"), "The output file /app/gc_data.txt does not exist."
    with open("/app/gc_data.txt", "r") as f:
        lines = f.readlines()
    assert len(lines) > 0, "The /app/gc_data.txt file is empty."

def test_http_service_prior_params():
    url = "http://127.0.0.1:9090/prior_params"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP service at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail(f"Failed to parse JSON from response: {response.text}")

    assert "mu" in data, "JSON response missing 'mu' key."
    assert "sigma" in data, "JSON response missing 'sigma' key."

    assert abs(data["mu"] - 0.45) < 1e-4, f"Expected mu to be 0.45, got {data['mu']}"
    assert abs(data["sigma"] - 0.08) < 1e-4, f"Expected sigma to be 0.08, got {data['sigma']}"

def test_http_service_posterior_mean():
    url = "http://127.0.0.1:9090/posterior_mean"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the HTTP service at {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    text = response.text.strip()
    assert text == "0.5849", f"Expected posterior mean to be '0.5849', got '{text}'"