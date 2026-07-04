# test_final_state.py
import os
import subprocess
import time
import urllib.request
import json

def test_conflict_txt():
    path = "/home/user/mobile_build/conflict.txt"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 1, f"Expected exactly one symbol in conflict.txt, found {len(lines)}."
    assert lines[0] == "calculate_metric", f"Expected 'calculate_metric' in conflict.txt, got '{lines[0]}'."

def test_build_and_app_output():
    build_script = "/home/user/mobile_build/build.sh"
    assert os.path.isfile(build_script), f"File {build_script} does not exist."

    # Run build.sh
    res = subprocess.run(["bash", "build.sh"], cwd="/home/user/mobile_build", capture_output=True, text=True)
    assert res.returncode == 0, f"build.sh failed to execute. stderr: {res.stderr}"

    app_path = "/home/user/mobile_build/app"
    assert os.path.isfile(app_path), f"File {app_path} was not created by build.sh."

    # Run app
    res_app = subprocess.run(["./app"], cwd="/home/user/mobile_build", capture_output=True, text=True)
    assert res_app.returncode == 0, f"./app failed to execute. stderr: {res_app.stderr}"
    assert res_app.stdout.strip() == "10", f"Expected app output to be '10', got '{res_app.stdout.strip()}'."

def test_shared_library_symbols():
    so_path = "/home/user/mobile_build/libmath_beta.so"
    assert os.path.isfile(so_path), f"File {so_path} does not exist."

    # Verify that calculate_metric is no longer exported in libmath_beta.so
    res = subprocess.run(["nm", "-D", "--defined-only", so_path], capture_output=True, text=True)
    assert res.returncode == 0, "Failed to run nm on libmath_beta.so"
    assert "calculate_metric" not in res.stdout, "calculate_metric is still exported dynamically in libmath_beta.so. The ABI was not properly managed."

def test_api_response():
    api_script = "/home/user/mobile_build/api.sh"
    assert os.path.isfile(api_script), f"File {api_script} does not exist."

    url = "http://localhost:8080/api/math/result"

    def fetch_api():
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.read().decode('utf-8')

    success = False
    body = ""
    # Try fetching in case the user left the server running
    try:
        body = fetch_api()
        success = True
    except Exception:
        pass

    # If not running, start it
    proc = None
    if not success:
        proc = subprocess.Popen(["bash", "api.sh"], cwd="/home/user/mobile_build")
        time.sleep(1) # Give it a moment to bind to port 8080
        try:
            body = fetch_api()
            success = True
        except Exception as e:
            assert False, f"Failed to connect to API on {url} or read response: {e}"
        finally:
            proc.terminate()
            proc.wait()

    assert success, "Could not retrieve response from API."

    # Validate JSON payload
    try:
        data = json.loads(body)
    except json.JSONDecodeError:
        assert False, f"API response is not valid JSON: {body}"

    assert data.get("status") == "success", f"Expected status 'success', got {data.get('status')}"
    assert data.get("result") == 10, f"Expected result 10, got {data.get('result')}"