# test_final_state.py
import os
import socket
import subprocess
import re
import pytest

def test_proxy_executable_exists():
    proxy_path = "/home/user/proxy"
    assert os.path.isfile(proxy_path), f"Proxy executable {proxy_path} does not exist."
    assert os.access(proxy_path, os.X_OK), f"Proxy executable {proxy_path} is not executable."

def test_proxy_is_listening():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    result = sock.connect_ex(('127.0.0.1', 8080))
    sock.close()
    assert result == 0, "Proxy service is not listening on 127.0.0.1:8080."

def test_proxy_accuracy_metric():
    verifier_path = "/app/verifier.py"
    assert os.path.isfile(verifier_path), f"Verifier script {verifier_path} is missing."

    try:
        result = subprocess.run(
            ["python3", verifier_path],
            capture_output=True,
            text=True,
            timeout=60
        )
    except subprocess.TimeoutExpired:
        pytest.fail("Verifier script timed out after 60 seconds.")

    output = result.stdout + "\n" + result.stderr

    match = re.search(r"METRIC_ACCURACY_SCORE:\s*([0-9]*\.?[0-9]+)", output)
    assert match is not None, f"Could not find METRIC_ACCURACY_SCORE in verifier output.\nOutput:\n{output}"

    accuracy = float(match.group(1))
    threshold = 0.98

    assert accuracy >= threshold, (
        f"Proxy accuracy is too low. "
        f"Expected >= {threshold}, but got {accuracy}.\n"
        f"Verifier output:\n{output}"
    )