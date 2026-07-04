# test_final_state.py

import os
import requests
import time
import pytest

def test_build_rs_fixed():
    """Verify that the build.rs file contains the fixed configuration."""
    build_rs_path = "/app/ab_service/build.rs"
    assert os.path.isfile(build_rs_path), f"The file {build_rs_path} does not exist."

    with open(build_rs_path, "r") as f:
        content = f.read()

    expected_line = 'println!("cargo:rustc-env=MATH_CONFIG=bayes_v1");'
    assert expected_line in content, "The build.rs file was not fixed correctly."

def test_csv_file_created_correctly():
    """Verify that the data.csv file was created with the exact content."""
    csv_path = "/home/user/data.csv"
    assert os.path.isfile(csv_path), f"The file {csv_path} does not exist."

    with open(csv_path, "r") as f:
        content = f.read().strip()

    expected_content = "variant_name,trials,successes\ncontrol,1000,150\ntreatment,1000,180"

    # Normalize line endings for comparison
    content_normalized = "\n".join([line.strip() for line in content.splitlines() if line.strip()])
    expected_normalized = "\n".join([line.strip() for line in expected_content.splitlines() if line.strip()])

    assert content_normalized == expected_normalized, "The data.csv file does not have the expected content."

def test_service_running_and_responding():
    """Verify that the service is running, listening on 8888, and responds correctly to the HTTP request."""
    url = "http://127.0.0.1:8888/stats"
    headers = {"Authorization": "Token stat_token_99"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the service at 127.0.0.1:8888. Is it running?")
    except requests.exceptions.Timeout:
        pytest.fail("Request to the service timed out.")

    assert response.status_code == 200, f"Expected status code 200, but got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        pytest.fail("The response from the service was not valid JSON.")

    assert "treatment_better_prob" in response.text, "The response JSON does not contain 'treatment_better_prob'."