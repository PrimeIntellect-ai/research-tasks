# test_final_state.py

import os
import subprocess
import re
import pytest

def test_nginx_config_updated():
    """Check that the NGINX config was updated with the correct socket path."""
    nginx_conf_path = "/home/user/nginx.conf"
    assert os.path.exists(nginx_conf_path), f"Missing required file: {nginx_conf_path}"

    with open(nginx_conf_path, "r") as f:
        content = f.read()

    expected_socket = "unix:/tmp/secure_app_v4.sock"
    assert expected_socket in content, f"The nginx.conf does not contain the correct socket path. Expected to find: {expected_socket}"

def test_ci_test_script_metric():
    """Execute the CI script and verify the success rate metric."""
    script_path = "/home/user/ci_test.py"
    assert os.path.exists(script_path), f"Missing required file: {script_path}"

    try:
        result = subprocess.run(
            ["python3", script_path],
            capture_output=True,
            text=True,
            timeout=60
        )
    except subprocess.TimeoutExpired:
        pytest.fail("ci_test.py timed out after 60 seconds.")

    assert result.returncode == 0, f"ci_test.py failed with return code {result.returncode}.\nStderr: {result.stderr}"

    output = result.stdout.strip()
    assert output, "ci_test.py produced no standard output."

    # Try to parse the output as a float. 
    # The instructions say "Print ONLY the success rate as a float".
    # We will extract the last numeric value in case of extraneous warnings.
    matches = re.findall(r"[-+]?\d*\.\d+|\d+", output)
    assert matches, f"Could not find a numeric value in the output of ci_test.py. Output: {output}"

    try:
        metric_value = float(matches[-1])
    except ValueError:
        pytest.fail(f"Could not parse '{matches[-1]}' as a float. Full output: {output}")

    threshold = 0.95
    assert metric_value >= threshold, f"Success rate metric {metric_value} is below the threshold of {threshold}."