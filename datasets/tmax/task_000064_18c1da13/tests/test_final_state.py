# test_final_state.py
import os
import subprocess
import pytest

def test_script_exists_and_executable():
    """Test that the port_analyzer.sh script exists and is executable."""
    script_path = "/home/user/port_analyzer.sh"
    assert os.path.isfile(script_path), f"Script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_gitlab_ci_generated():
    """Test that the .gitlab-ci.yml file was generated with the required components."""
    ci_path = "/home/user/.gitlab-ci.yml"
    assert os.path.isfile(ci_path), f"CI config missing at {ci_path}"
    with open(ci_path, "r") as f:
        content = f.read().lower()

    assert "alpine" in content, "alpine image not found in .gitlab-ci.yml"
    assert "ffmpeg" in content, "ffmpeg not found in .gitlab-ci.yml"
    assert "bash" in content, "bash not found in .gitlab-ci.yml"

def test_script_output():
    """Test that the script outputs the correct frame number within the allowed metric threshold."""
    script_path = "/home/user/port_analyzer.sh"
    result = subprocess.run(["bash", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}. Stderr: {result.stderr}"

    stdout = result.stdout.strip()
    try:
        predicted = int(stdout)
    except ValueError:
        pytest.fail(f"Output is not a valid integer: '{stdout}'. Stderr: {result.stderr}")

    truth = 402
    error = abs(truth - predicted)
    assert error <= 2, f"Metric threshold failed: Error {error} > 2. Predicted frame {predicted}, expected around {truth}."