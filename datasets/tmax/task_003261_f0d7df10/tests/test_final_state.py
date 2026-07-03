# test_final_state.py

import os
import time
import subprocess
import requests
import pytest

def test_service_ready_file_exists():
    """Check if the service ready signal file exists."""
    assert os.path.isfile("/tmp/service_ready"), "/tmp/service_ready file was not created by the service"

def test_http_endpoint_validation():
    """Test the HTTP endpoint for correct validation logic."""
    # Wait a moment for the service to actually bind if it just created the file
    time.sleep(1)

    url = "http://127.0.0.1:8080/validate"

    test_cases = [
        {"version": "1.5.4", "expected": True},
        {"version": "2.0.0", "expected": False},
        {"version": "1.1.9", "expected": False},
    ]

    for case in test_cases:
        try:
            response = requests.post(url, json={"version": case["version"]}, timeout=5)
            assert response.status_code == 200, f"Expected HTTP 200 for version {case['version']}, got {response.status_code}"

            data = response.json()
            assert "allowed" in data, f"Response JSON missing 'allowed' key for version {case['version']}"
            assert data["allowed"] == case["expected"], f"Expected allowed={case['expected']} for version {case['version']}, got {data['allowed']}"
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Failed to connect to the HTTP service or request failed: {e}")

def test_cargo_tests_pass():
    """Check if cargo test passes, verifying the proptest and logic."""
    project_dir = "/home/user/policy-service"
    result = subprocess.run(["cargo", "test"], cwd=project_dir, capture_output=True, text=True)
    assert result.returncode == 0, f"cargo test failed:\n{result.stdout}\n{result.stderr}"

def test_proptest_used():
    """Check if proptest is actually used in semver.rs."""
    semver_rs = "/home/user/policy-service/src/semver.rs"
    assert os.path.isfile(semver_rs), f"{semver_rs} does not exist"

    with open(semver_rs, "r") as f:
        content = f.read()
        assert "proptest" in content, "proptest crate is not used in src/semver.rs"
        assert "proptest!" in content or "#[proptest]" in content, "proptest macro is not used in src/semver.rs"