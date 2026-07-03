# test_final_state.py
import os
import requests

def test_malicious_tag_extracted():
    """Verify that the malicious tag was properly extracted to the required file."""
    path = "/home/user/malicious_tag.txt"
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    expected = "len=128;payload=recursive_doom"
    assert content == expected, f"Expected tag content '{expected}', but got '{content}'."

def test_fuzz_test_exists():
    """Verify that a Go fuzz test was written in parser_test.go."""
    path = "/app/healthd/parser_test.go"
    assert os.path.exists(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "testing.F" in content, f"Fuzz test must use 'testing.F', not found in {path}."
    assert "func Fuzz" in content, f"Fuzz test function (e.g., func Fuzz...) not found in {path}."

def test_healthd_good_request():
    """Verify that the healthd service correctly handles a good target."""
    url = "http://127.0.0.1:8080/check?url=http://127.0.0.1:8081/good"
    try:
        resp = requests.get(url, timeout=5)
    except requests.RequestException as e:
        assert False, f"Request to healthd failed: {e}. Is the service running?"

    assert resp.status_code == 200, f"Expected HTTP 200 OK, got {resp.status_code}. Body: {resp.text}"
    assert "status: healthy" in resp.text, f"Expected 'status: healthy' in response body, got: {resp.text}"

def test_healthd_bad_request_does_not_crash():
    """Verify that the healthd service handles the malicious payload without crashing."""
    bad_url = "http://127.0.0.1:8080/check?url=http://127.0.0.1:8081/bad"
    try:
        # This request might return 200 OK (with handled empty tags) or 500, but it MUST NOT timeout/crash.
        resp = requests.get(bad_url, timeout=5)
    except requests.exceptions.ReadTimeout:
        assert False, "Request timed out. The service likely entered an infinite loop."
    except requests.exceptions.ConnectionError:
        assert False, "Connection error. The service likely crashed (stack overflow)."
    except requests.RequestException as e:
        assert False, f"Request failed unexpectedly: {e}"

    # Verify the service is still alive by making another good request
    good_url = "http://127.0.0.1:8080/check?url=http://127.0.0.1:8081/good"
    try:
        resp_good = requests.get(good_url, timeout=5)
        assert resp_good.status_code == 200, f"Service is up but returned {resp_good.status_code} after bad request."
    except requests.RequestException as e:
        assert False, f"Service crashed or became unresponsive after malicious payload: {e}"