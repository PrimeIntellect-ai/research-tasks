# test_final_state.py
import os
import stat
import subprocess
import time
import json
import base64
import urllib.request
import urllib.error
import pytest

MATH_SERVICE_DIR = "/home/user/math_service"
SERVER_FILE = os.path.join(MATH_SERVICE_DIR, "server.py")
TEST_FILE = os.path.join(MATH_SERVICE_DIR, "test_server.py")
CI_SCRIPT = os.path.join(MATH_SERVICE_DIR, "ci_run.sh")

def test_files_exist():
    assert os.path.isdir(MATH_SERVICE_DIR), f"Directory {MATH_SERVICE_DIR} does not exist."
    assert os.path.isfile(SERVER_FILE), f"File {SERVER_FILE} does not exist."
    assert os.path.isfile(TEST_FILE), f"File {TEST_FILE} does not exist."
    assert os.path.isfile(CI_SCRIPT), f"File {CI_SCRIPT} does not exist."

def test_ci_script_executable():
    st = os.stat(CI_SCRIPT)
    assert st.st_mode & stat.S_IXUSR, f"{CI_SCRIPT} is not executable."

def test_ci_script_runs_successfully():
    result = subprocess.run(["bash", CI_SCRIPT], cwd=MATH_SERVICE_DIR, capture_output=True, text=True)
    assert result.returncode == 0, f"ci_run.sh failed with exit code {result.returncode}.\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

@pytest.fixture(scope="module")
def server_process():
    # Start the server
    proc = subprocess.Popen(
        ["python3", SERVER_FILE],
        cwd=MATH_SERVICE_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Wait for server to start
    url = "http://127.0.0.1:8080/evaluate"
    started = False
    for _ in range(30):
        try:
            req = urllib.request.Request(url, method="POST")
            req.add_header("Content-Type", "application/json")
            data = json.dumps({"payload": base64.b64encode(b"1+1").decode('utf-8')}).encode('utf-8')
            urllib.request.urlopen(req, data=data, timeout=1)
            started = True
            break
        except urllib.error.HTTPError as e:
            if e.code in [200, 400, 405, 429]:
                started = True
                break
        except Exception:
            time.sleep(0.5)

    if not started:
        proc.terminate()
        proc.wait()
        pytest.fail("Server failed to start on 127.0.0.1:8080")

    yield proc

    proc.terminate()
    proc.wait()

def send_request(payload_str):
    url = "http://127.0.0.1:8080/evaluate"
    req = urllib.request.Request(url, method="POST")
    req.add_header("Content-Type", "application/json")
    # Add a custom header or change IP if possible? No, we just test from 127.0.0.1
    b64_payload = base64.b64encode(payload_str.encode('utf-8')).decode('utf-8')
    data = json.dumps({"payload": b64_payload}).encode('utf-8')
    try:
        response = urllib.request.urlopen(req, data=data, timeout=2)
        return response.getcode(), json.loads(response.read().decode('utf-8'))
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode('utf-8'))

def test_server_valid_evaluation(server_process):
    code, data = send_request("2 + 2")
    assert code == 200, f"Expected 200 OK, got {code}"
    assert "result" in data, "Response missing 'result' key"
    assert data["result"] == 4, f"Expected result 4, got {data['result']}"

def test_server_invalid_characters(server_process):
    code, data = send_request("import os")
    assert code == 400, f"Expected 400 Bad Request, got {code}"
    assert "error" in data, "Response missing 'error' key"

def test_server_division_by_zero(server_process):
    code, data = send_request("1 / 0")
    assert code == 400, f"Expected 400 Bad Request for division by zero, got {code}"

def test_server_rate_limiting(server_process):
    # Send 5 valid requests, they should all pass (or some might fail if we already sent 2, wait, let's use a different endpoint or just rely on the count)
    # The server rate limits per IP. The fixture already sent 1 request. The valid test sent 1. Invalid sent 1. Div by zero sent 1.
    # That's 4 requests. If we send 2 more, the 2nd should fail.
    # To be robust, let's just send requests until we get a 429, but no more than 10.

    got_429 = False
    for _ in range(10):
        code, data = send_request("1 + 1")
        if code == 429:
            got_429 = True
            assert "error" in data, "Response missing 'error' key on 429"
            break

    assert got_429, "Rate limit (429) was not enforced after multiple requests."