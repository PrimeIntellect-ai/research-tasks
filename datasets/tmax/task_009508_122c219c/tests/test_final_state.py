# test_final_state.py
import os
import subprocess
import urllib.request
import urllib.error
import pytest

def test_valgrind_log_contents():
    log_path = "/home/user/valgrind.log"
    assert os.path.isfile(log_path), f"Valgrind log file {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read()
    assert "0 errors from 0 contexts" in content, "Valgrind log does not report '0 errors from 0 contexts'."
    assert "All heap blocks were freed -- no leaks are possible" in content, "Valgrind log does not report that all heap blocks were freed."

def test_solver_binary_no_leaks():
    binary_path = "/home/user/app/solver"
    assert os.path.isfile(binary_path), f"Solver binary {binary_path} does not exist."
    assert os.access(binary_path, os.X_OK), f"Solver binary {binary_path} is not executable."

    # Run valgrind on the compiled binary to ensure it was actually fixed
    cmd = ["valgrind", "--leak-check=full", "--error-exitcode=1", binary_path, "8"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stderr
    except subprocess.CalledProcessError as e:
        output = e.stderr
        pytest.fail(f"Valgrind reported errors or leaks when running the fixed solver:\n{output}")

    assert "0 errors from 0 contexts" in output, "Dynamic valgrind check failed: errors found."
    assert "All heap blocks were freed -- no leaks are possible" in output, "Dynamic valgrind check failed: leaks found."

def test_services_running():
    # Check if backend.py is running
    try:
        subprocess.run(["pgrep", "-f", "backend.py"], check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        pytest.fail("Python backend (backend.py) is not running.")

    # Check if nginx is running
    try:
        subprocess.run(["pgrep", "nginx"], check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        pytest.fail("Nginx is not running.")

def test_response_txt():
    response_path = "/home/user/response.txt"
    assert os.path.isfile(response_path), f"Response file {response_path} does not exist."
    with open(response_path, "r") as f:
        content = f.read().strip()
    assert content == "14200", f"Expected response.txt to contain '14200', but got '{content}'."

def test_nginx_proxy_endpoint():
    url = "http://127.0.0.1:8000/qa/8"
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=5) as response:
            body = response.read().decode('utf-8').strip()
            assert body == "92", f"Expected proxy endpoint to return '92' for N=8, but got '{body}'"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to Nginx reverse proxy at {url}: {e}")