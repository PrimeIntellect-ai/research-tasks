# test_final_state.py

import os
import time
import pytest
import requests

SERVER_URL = "http://127.0.0.1:5000"
AUTH_HEADER = {"X-MLOps-Auth": "track-me"}
WRONG_AUTH_HEADER = {"X-MLOps-Auth": "wrong-auth"}

def test_server_ready_file_exists():
    """Test that the server ready file was created."""
    ready_file = "/home/user/server_ready.txt"
    assert os.path.exists(ready_file), f"The file {ready_file} was not created, indicating the server might not be ready."

def test_auth_failure():
    """Test that requests without proper auth fail."""
    response = requests.get(f"{SERVER_URL}/config", headers=WRONG_AUTH_HEADER, timeout=5)
    assert response.status_code in (401, 403), f"Expected 401 or 403 for wrong auth, got {response.status_code}."

    response_no_auth = requests.get(f"{SERVER_URL}/config", timeout=5)
    assert response_no_auth.status_code in (401, 403), f"Expected 401 or 403 for missing auth, got {response_no_auth.status_code}."

def test_config_endpoint():
    """Test the /config endpoint for correct extracted and computed values."""
    response = requests.get(f"{SERVER_URL}/config", headers=AUTH_HEADER, timeout=5)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}."

    data = response.json()
    assert "seed" in data, "Missing 'seed' in /config response."
    assert "target_variance" in data, "Missing 'target_variance' in /config response."
    assert "n_components" in data, "Missing 'n_components' in /config response."

    assert data["seed"] == 8128, f"Expected seed 8128, got {data['seed']}."
    assert abs(data["target_variance"] - 0.9) < 1e-4, f"Expected target_variance 0.9, got {data['target_variance']}."
    assert data["n_components"] == 32, f"Expected n_components 32, got {data['n_components']}."

def test_covariance_endpoint():
    """Test the /covariance endpoint for correct PCA covariance values."""
    response = requests.get(f"{SERVER_URL}/covariance", headers=AUTH_HEADER, timeout=5)
    assert response.status_code == 200, f"Expected status 200, got {response.status_code}."

    data = response.json()
    for key in ["cov_00", "cov_01", "cov_10", "cov_11"]:
        assert key in data, f"Missing '{key}' in /covariance response."

    assert abs(data["cov_00"] - 13.9189) < 1e-3, f"Expected cov_00 ~13.9189, got {data['cov_00']}."
    assert abs(data["cov_01"]) < 1e-3, f"Expected cov_01 ~0.0, got {data['cov_01']}."
    assert abs(data["cov_10"]) < 1e-3, f"Expected cov_10 ~0.0, got {data['cov_10']}."
    assert abs(data["cov_11"] - 7.0427) < 1e-3, f"Expected cov_11 ~7.0427, got {data['cov_11']}."