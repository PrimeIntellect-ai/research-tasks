# test_final_state.py

import os
import urllib.request
import urllib.error
import pytest

def test_bug_report():
    path = "/home/user/bug_report.txt"
    assert os.path.exists(path), f"File {path} does not exist. You must create the bug report."

    with open(path, "r") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.split('\n') if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {path}, got {len(lines)}. Content was: {content}"
    assert lines[0] == "A103", f"Expected tx_id 'A103' on line 1, got '{lines[0]}'"
    assert lines[1] == "0.3333333", f"Expected rate '0.3333333' on line 2, got '{lines[1]}'"

def test_run_sh_executable():
    path = "/home/user/run.sh"
    assert os.path.exists(path), f"Script {path} does not exist. You must create the startup script."
    assert os.access(path, os.X_OK), f"Script {path} is not executable. Please make it executable (e.g., chmod +x)."

def test_service_responds_and_calculates_correctly():
    url = "http://localhost:8080/calculate?rate=0.3333333"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200 status code, got {response.status}"
            body = response.read().decode('utf-8').strip()

            try:
                val = float(body)
            except ValueError:
                pytest.fail(f"Service returned '{body}', which is not a valid floating point number.")

            # The square root of 0.3333333 is approximately 0.577350
            assert 0.577 < val < 0.578, f"Calculated value {val} is incorrect for rate=0.3333333. Expected ~0.577350."

    except urllib.error.HTTPError as e:
        pytest.fail(f"Service returned an HTTP error: {e.code} {e.reason}")
    except urllib.error.URLError as e:
        pytest.fail(f"Could not connect to the service at {url}. Is the service running and listening on port 8080? Error: {e.reason}")
    except TimeoutError:
        pytest.fail(f"Request to {url} timed out. The infinite loop bug might still be present.")