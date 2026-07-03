# test_final_state.py

import os
import re
import subprocess
import urllib.request
import urllib.error
import pytest

def test_rust_server_compiles():
    """Check if the Rust server compiles successfully."""
    project_dir = "/home/user/artifact_server"
    assert os.path.isdir(project_dir), f"Directory {project_dir} does not exist."

    try:
        # Run cargo check to verify compilation without necessarily building the full binary
        result = subprocess.run(
            ["cargo", "check", "--release"],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        assert result.returncode == 0, f"Rust project failed to compile. Error:\n{result.stderr}"
    except FileNotFoundError:
        pytest.fail("cargo command not found. Is Rust installed?")
    except subprocess.TimeoutExpired:
        pytest.fail("cargo check timed out.")

def test_rust_server_running_and_correct():
    """Check if the Rust server is running on port 8080 and responds correctly."""
    url = "http://127.0.0.1:8080/artifact/v2/linux?id=test_99"
    try:
        req = urllib.request.Request(url, method="GET")
        with urllib.request.urlopen(req, timeout=5) as response:
            assert response.status == 200, f"Expected HTTP 200, got {response.status}"
            body = response.read().decode('utf-8')
            assert body == "ArtifactData_test_99", f"Expected 'ArtifactData_test_99', got '{body}'"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to the Rust server at {url}. Is it running in the background? Error: {e}")
    except Exception as e:
        pytest.fail(f"Unexpected error when communicating with the Rust server: {e}")

def test_benchmark_script_exists():
    """Check if the benchmark script exists."""
    script_path = "/home/user/benchmark.py"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

def test_p95_result_exists_and_format():
    """Check if the p95_result.txt exists and contains a valid float formatted to 2 decimal places."""
    result_path = "/home/user/p95_result.txt"
    assert os.path.isfile(result_path), f"The result file {result_path} does not exist."

    with open(result_path, 'r') as f:
        content = f.read().strip()

    assert content, f"The file {result_path} is empty."

    # Check if it's a valid float
    try:
        float_val = float(content)
    except ValueError:
        pytest.fail(f"The content of {result_path} ('{content}') is not a valid float.")

    # Check if it has exactly 2 decimal places
    assert re.match(r"^\d+\.\d{2}$", content), f"The value '{content}' is not rounded to exactly 2 decimal places."