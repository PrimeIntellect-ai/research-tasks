# test_final_state.py

import os
import subprocess
import pytest

def test_deployment_structure():
    """Verify the deployment directory structure and files exist."""
    assert os.path.exists("/home/user/deploy/bin/waf_analyzer"), "waf_analyzer executable is missing in /home/user/deploy/bin/"
    assert os.path.exists("/home/user/deploy/lib/libwafparser.so"), "libwafparser.so is missing in /home/user/deploy/lib/"

    # Ensure they are executable/shared objects
    assert os.access("/home/user/deploy/bin/waf_analyzer", os.X_OK), "waf_analyzer is not executable"

def test_rpath_configuration():
    """Verify that the waf_analyzer binary has the correct RPATH/RUNPATH set."""
    binary_path = "/home/user/deploy/bin/waf_analyzer"

    try:
        output = subprocess.check_output(["readelf", "-d", binary_path], universal_newlines=True)
    except Exception as e:
        pytest.fail(f"Failed to run readelf on {binary_path}: {e}")

    has_rpath = False
    for line in output.splitlines():
        if "RPATH" in line or "RUNPATH" in line:
            if "$ORIGIN/../lib" in line:
                has_rpath = True
                break

    assert has_rpath, "waf_analyzer does not have RPATH or RUNPATH set to exactly '$ORIGIN/../lib'"

def test_analysis_results():
    """Verify the output of the waf_analyzer log processing."""
    results_file = "/home/user/deploy/analysis_results.log"
    assert os.path.exists(results_file), f"{results_file} does not exist. Did you run the analyzer?"

    expected_lines = [
        'ALLOWED: GET /index.html HTTP/1.1',
        'BLOCKED: POST /login HTTP/1.1 payload="admin\' OR 1=1 --"',
        'BLOCKED: GET /search?q=<script>alert(1)</script> HTTP/1.1',
        'ALLOWED: GET /about HTTP/1.1',
        'BLOCKED: POST /api/data HTTP/1.1 payload="DROP TABLE users;"'
    ]

    with open(results_file, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, "The contents of analysis_results.log do not match the expected output. Ensure the patch was applied correctly and the binary was run against requests.log."