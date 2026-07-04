# test_final_state.py
import os
import subprocess
import pytest

def test_proxy_source_exists():
    path = "/home/user/audit_proxy.cpp"
    assert os.path.exists(path), f"The proxy source code is missing at {path}."
    assert os.path.isfile(path), f"The path {path} is not a file."

def test_proxy_binary_exists_and_executable():
    path = "/home/user/audit_proxy"
    assert os.path.exists(path), f"The compiled proxy binary is missing at {path}."
    assert os.path.isfile(path), f"The path {path} is not a file."
    assert os.access(path, os.X_OK), f"The file at {path} is not executable."

def test_proxy_accuracy_metric():
    script_path = "/verify/run_eval.py"
    assert os.path.exists(script_path), f"Verifier script missing at {script_path}"

    try:
        result = subprocess.run(
            ["python3", script_path],
            capture_output=True,
            text=True,
            timeout=60,
            check=True
        )
    except subprocess.TimeoutExpired:
        pytest.fail("The verifier script timed out after 60 seconds.")
    except subprocess.CalledProcessError as e:
        pytest.fail(f"The verifier script failed with exit code {e.returncode}.\nStdout: {e.stdout}\nStderr: {e.stderr}")

    output = result.stdout.strip()

    # The script is expected to output a single float representing the accuracy
    # It may have other output, so we take the last line if there are multiple
    last_line = output.splitlines()[-1] if output else ""

    try:
        accuracy = float(last_line)
    except ValueError:
        pytest.fail(f"Could not parse accuracy metric from verifier output. Output was:\n{output}")

    threshold = 0.95
    assert accuracy >= threshold, f"Proxy accuracy {accuracy} is below the required threshold of {threshold}."