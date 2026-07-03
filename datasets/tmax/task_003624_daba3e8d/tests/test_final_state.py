# test_final_state.py
import os
import subprocess
import time
import urllib.request
import urllib.error
import pytest

def test_cicd_script_exists_and_executable():
    """Verify that cicd.sh exists and is executable."""
    script_path = "/home/user/cicd.sh"
    assert os.path.isfile(script_path), f"FAIL: {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"FAIL: {script_path} is not executable."

def test_haproxy_running_and_listening():
    """Verify HAProxy is running and listening on port 8080."""
    try:
        output = subprocess.check_output(["pgrep", "-x", "haproxy"]).decode()
        assert output.strip() != "", "FAIL: HAProxy is not running."
    except subprocess.CalledProcessError:
        pytest.fail("FAIL: HAProxy is not running.")

    try:
        output = subprocess.check_output(["ss", "-tuln"]).decode()
        assert ":8080" in output, "FAIL: Port 8080 is not listening."
    except subprocess.CalledProcessError:
        pytest.fail("FAIL: Failed to check listening ports.")

def test_operator_listening():
    """Verify operators are listening on ports 8081 and 8082."""
    try:
        output = subprocess.check_output(["ss", "-tuln"]).decode()
        assert ":8081" in output, "FAIL: Port 8081 is not listening."
        assert ":8082" in output, "FAIL: Port 8082 is not listening."
    except subprocess.CalledProcessError:
        pytest.fail("FAIL: Failed to check listening ports.")

def test_cicd_execution_and_operator_logic():
    """Execute cicd.sh and verify that it triggers the operator to create the processed file."""
    script_path = "/home/user/cicd.sh"
    processed_file = "/home/user/mail_spool/deployment.yaml.processed"

    # Remove the file if it exists to ensure a fresh test
    if os.path.exists(processed_file):
        os.remove(processed_file)

    # Execute the script
    try:
        subprocess.run(["bash", script_path], check=True, timeout=5)
    except subprocess.CalledProcessError:
        pytest.fail(f"FAIL: Execution of {script_path} failed.")
    except subprocess.TimeoutExpired:
        pytest.fail(f"FAIL: Execution of {script_path} timed out.")

    # Give it a moment to process
    time.sleep(1)

    # Check if the processed file exists
    assert os.path.isfile(processed_file), f"FAIL: Processed file {processed_file} not found after running cicd.sh."

    # Check the content of the processed file
    with open(processed_file, "r") as f:
        content = f.read().strip()

    expected_content = "Processed deployment.yaml"
    assert content == expected_content, f"FAIL: Incorrect content in processed file. Expected '{expected_content}', got '{content}'."

def test_operator_direct_http_response():
    """Test the operator directly to ensure it returns the correct HTTP response."""
    # Create a dummy manifest to trigger processing
    dummy_manifest = "/home/user/manifests/dummy.yaml"
    with open(dummy_manifest, "w") as f:
        f.write("dummy")

    try:
        req = urllib.request.Request("http://127.0.0.1:8081/sync")
        with urllib.request.urlopen(req, timeout=2) as response:
            body = response.read().decode()
            assert "OK" in body, "FAIL: Operator on port 8081 did not return OK."
    except Exception as e:
        pytest.fail(f"FAIL: Direct request to operator on port 8081 failed: {e}")