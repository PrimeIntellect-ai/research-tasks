# test_final_state.py

import os
import json
import subprocess
import pytest

def test_libdevice_compiled_and_linked():
    lib_path = "/home/user/libdevice.so"
    assert os.path.exists(lib_path), f"Missing file: {lib_path}. The build script was not run or failed."

    # Check if dynamically linked against libm
    result = subprocess.run(['ldd', lib_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to run ldd on {lib_path}"
    assert "libm.so" in result.stdout, f"{lib_path} is not linked against libm.so. The build.sh script was likely not fixed correctly."

def test_proxy_script_exists():
    proxy_path = "/home/user/proxy.py"
    assert os.path.exists(proxy_path), f"Missing file: {proxy_path}. The proxy script was not created."

def test_ci_results_exists_and_correct():
    results_path = "/home/user/ci_results.json"
    assert os.path.exists(results_path), f"Missing file: {results_path}. The pipeline was not executed successfully."

    with open(results_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{results_path} does not contain valid JSON.")

    assert "proxy_header" in data, f"'proxy_header' key missing in {results_path}"
    assert data["proxy_header"] == "1", f"Expected 'proxy_header' to be '1', got '{data['proxy_header']}'. The proxy did not add the X-Proxy-Routed header correctly."

    assert "body" in data, f"'body' key missing in {results_path}"
    body = data["body"]
    assert "sensor_reading" in body, f"'sensor_reading' key missing in the body of {results_path}"
    assert body["sensor_reading"] == 1.0, f"Expected 'sensor_reading' to be 1.0, got {body['sensor_reading']}"