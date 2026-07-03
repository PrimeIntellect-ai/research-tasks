# test_final_state.py
import os
import json
import subprocess
import urllib.request
import urllib.error

def test_data_logs_directory_exists():
    path = "/home/user/data/logs"
    assert os.path.isdir(path), f"Directory {path} does not exist. The directory structure was not fixed."

def test_result_json_exists_and_correct():
    path = "/home/user/data/logs/result.json"
    assert os.path.isfile(path), f"File {path} does not exist. The script might not have run successfully."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {path} does not contain valid JSON."

    assert data.get("success") is True, f"result.json 'success' key is not True. Got: {data.get('success')}"
    assert data.get("data") == "BACKEND_OK", f"result.json 'data' key is not 'BACKEND_OK'. Got: {data.get('data')}"

def test_port_forwarding_active():
    try:
        req = urllib.request.urlopen("http://127.0.0.1:9999/health", timeout=2)
        res = req.read().decode('utf-8')
        assert "BACKEND_OK" in res, "Port 9999 did not return the expected backend response."
    except urllib.error.URLError as e:
        assert False, f"Port forwarding to 9999 is not working. Connection failed: {e}"

def test_checker_script_absolute_path_fix():
    # Run checker.py from /tmp to verify it doesn't rely on relative paths
    result = subprocess.run(
        ["python3", "/home/user/service/checker.py"],
        cwd="/tmp",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"checker.py failed when run from /tmp. Exit code: {result.returncode}\nStdout: {result.stdout}\nStderr: {result.stderr}"