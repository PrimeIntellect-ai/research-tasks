# test_final_state.py

import os
import pytest
import requests

def test_vendored_package_fixed():
    cargo_path = "/app/outlier_detect/Cargo.toml"
    assert os.path.isfile(cargo_path), f"{cargo_path} is missing."
    with open(cargo_path, "r") as f:
        cargo_content = f.read()
    assert "[dependencies]" in cargo_content, "Cargo.toml should have the typo '[dependencis]' fixed to '[dependencies]'."
    assert "[dependencis]" not in cargo_content, "Cargo.toml still contains the typo '[dependencis]'."

    lib_path = "/app/outlier_detect/src/lib.rs"
    assert os.path.isfile(lib_path), f"{lib_path} is missing."
    with open(lib_path, "r") as f:
        lib_content = f.read()

    # Check for the missing semicolon fix on the variance line
    assert "sum::<f64>() / data.len() as f64;" in lib_content or "sum::<f64>() / (data.len() as f64);" in lib_content or "as f64;\n" in lib_content, "lib.rs still seems to be missing the semicolon on the variance calculation."

def test_service_unauthorized():
    url = "http://127.0.0.1:8080/process"
    payload = [{"id": 1, "val": 10.0}]

    # Missing header
    try:
        resp = requests.post(url, json=payload, timeout=5)
        assert resp.status_code == 401, f"Expected 401 Unauthorized for missing header, got {resp.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

    # Incorrect header
    headers = {"Authorization": "Bearer wrong_token"}
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=5)
        assert resp.status_code == 401, f"Expected 401 Unauthorized for incorrect token, got {resp.status_code}"
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service: {e}")

def test_service_processing():
    url = "http://127.0.0.1:8080/process"
    headers = {"Authorization": "Bearer secret_token_999"}
    payload = [
        {"id": 1, "val": 10.0},
        {"id": 2, "val": 12.0},
        {"id": 3, "val": None},
        {"id": 4, "val": 11.0},
        {"id": 5, "val": 1000.0},
        {"id": 6, "val": 9.0}
    ]

    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to the service or request timed out: {e}")

    assert resp.status_code == 200, f"Expected status code 200, got {resp.status_code}. Response: {resp.text}"

    try:
        data = resp.json()
    except ValueError:
        pytest.fail(f"Response is not valid JSON: {resp.text}")

    assert "cleaned_count" in data, "Response JSON missing 'cleaned_count'"
    assert "mean_ci" in data, "Response JSON missing 'mean_ci'"

    assert data["cleaned_count"] == 5, f"Expected cleaned_count to be 5, got {data['cleaned_count']}"

    mean_ci = data["mean_ci"]
    assert isinstance(mean_ci, list) and len(mean_ci) == 2, "mean_ci must be a list of two floats"

    lower_bound, upper_bound = mean_ci
    assert isinstance(lower_bound, (int, float)), "Lower bound must be a number"
    assert isinstance(upper_bound, (int, float)), "Upper bound must be a number"

    # Statistically plausible bounds based on the truth data
    assert 8.0 <= lower_bound <= 50.0, f"Lower bound {lower_bound} is outside the plausible range [8.0, 50.0]"
    assert 50.0 <= upper_bound <= 200.0, f"Upper bound {upper_bound} is outside the plausible range [50.0, 200.0]"
    assert lower_bound < upper_bound, "Lower bound must be less than upper bound"