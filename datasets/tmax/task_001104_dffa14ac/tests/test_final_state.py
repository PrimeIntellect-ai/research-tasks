# test_final_state.py

import json
import hashlib
import requests
import pytest

def get_expected_status(module_name: str) -> str:
    h = hashlib.md5(module_name.encode()).hexdigest()
    first_char = h[0]
    if int(first_char, 16) % 2 == 0:
        return "APPROVED"
    else:
        return "REJECTED"

def test_analyze_endpoint():
    payload = """Compiling artifact_manager v0.1.0 (/home/user/project)
error[E0106]: missing lifetime specifier
  --> src/state_machine.rs:22:12
   |
22 |     parser: &Parser,
   |             ^ expected named lifetime parameter

error[E0502]: cannot borrow `*pipeline` as mutable because it is also borrowed as immutable
  --> src/cicd_runner.rs:45:5
"""

    try:
        response = requests.post(
            "http://127.0.0.1:8080/analyze",
            data=payload,
            headers={"Content-Type": "text/plain"},
            timeout=5
        )
    except requests.exceptions.ConnectionError:
        pytest.fail("Could not connect to the HTTP server at 127.0.0.1:8080. Is it running?")
    except requests.exceptions.Timeout:
        pytest.fail("Request to 127.0.0.1:8080/analyze timed out.")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except json.JSONDecodeError:
        pytest.fail(f"Response is not valid JSON. Response text: {response.text}")

    assert "failing_modules" in data, "Response JSON is missing 'failing_modules' key"
    assert "checker_results" in data, "Response JSON is missing 'checker_results' key"

    expected_modules = ["state_machine", "cicd_runner"]
    assert set(data["failing_modules"]) == set(expected_modules), \
        f"Expected failing_modules to contain {expected_modules}, got {data['failing_modules']}"

    expected_results = {
        mod: get_expected_status(mod) for mod in expected_modules
    }

    assert data["checker_results"] == expected_results, \
        f"Expected checker_results to be {expected_results}, got {data['checker_results']}"