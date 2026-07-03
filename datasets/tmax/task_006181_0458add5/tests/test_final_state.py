# test_final_state.py
import os
import re
import socket
import subprocess
import sys

def test_nginx_listening_8090():
    """Check if Nginx (or some process) is listening on port 8090."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 8090))
    sock.close()
    assert result == 0, "Nothing is listening on 127.0.0.1:8090 (Nginx expected)."

def test_failed_artifacts_log():
    """Check if failed_artifacts.log exists and has the correct format."""
    log_path = "/home/user/failed_artifacts.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) > 0 and lines[0] != "", "Log file is empty."

    pattern = re.compile(r"^build-\d+,\d+,\d+(\.\d+)?$")
    valid_lines = 0
    for line in lines:
        if not line.strip():
            continue
        if pattern.match(line):
            valid_lines += 1

    assert valid_lines > 0, "No correctly formatted lines found in the log file (expected format: build-X,123,45.6)."

def test_client_script_and_function():
    """Verify client.py exists and contains the required function."""
    client_path = "/home/user/client.py"
    assert os.path.isfile(client_path), f"{client_path} does not exist."

    sys.path.insert(0, "/home/user")
    try:
        import client
    except ImportError:
        assert False, "Could not import client.py"

    assert hasattr(client, "parse_and_transform"), "client.py is missing the parse_and_transform function."

    # Test the function logic briefly
    func = client.parse_and_transform
    valid_json = '{"artifact_id": "build-123", "status": "failure", "metrics": {"size_bytes": 1024, "build_time_sec": 45.2}}'
    assert func(valid_json) == "build-123,1024,45.2", "parse_and_transform did not return correct CSV for failure."

    success_json = '{"artifact_id": "build-124", "status": "success", "metrics": {"size_bytes": 1024, "build_time_sec": 45.2}}'
    assert func(success_json) is None, "parse_and_transform should return None for non-failure status."

    invalid_json = '{"artifact_id": "build-125"'
    assert func(invalid_json) is None, "parse_and_transform should return None on JSONDecodeError."

def test_pytest_hypothesis_suite():
    """Run the user's test_client.py and ensure it passes."""
    test_path = "/home/user/test_client.py"
    assert os.path.isfile(test_path), f"{test_path} does not exist."

    # Check if hypothesis is imported
    with open(test_path, "r") as f:
        content = f.read()
    assert "hypothesis" in content, "test_client.py does not appear to use hypothesis."

    # Run pytest
    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"pytest on {test_path} failed:\n{result.stdout}\n{result.stderr}"