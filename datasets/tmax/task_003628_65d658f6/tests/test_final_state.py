# test_final_state.py

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/polyglot-eval"
BUILD_SH_PATH = os.path.join(PROJECT_DIR, "build.sh")
LOG_PATH = "/home/user/build_out.log"

def test_build_sh_exists_and_executable():
    assert os.path.isfile(BUILD_SH_PATH), f"Script missing: {BUILD_SH_PATH}"
    assert os.access(BUILD_SH_PATH, os.X_OK), f"Script is not executable: {BUILD_SH_PATH}"

def test_build_sh_uses_jq():
    with open(BUILD_SH_PATH, "r") as f:
        content = f.read()
    assert "jq " in content, "build.sh does not appear to use 'jq' to parse ci_config.json"

def test_python_tests_fixed():
    # Run the Python tests to ensure the state isolation issue is fixed
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"

    # Run tests in reverse order or together to trigger the original issue
    # The command provided in the task is: python3 -m unittest discover -s tests
    result = subprocess.run(
        ["python3", "-m", "unittest", "discover", "-s", "tests"],
        cwd=PROJECT_DIR,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert result.returncode == 0, f"Python tests failed or are not isolated.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"
    assert "OK" in result.stderr or "OK" in result.stdout, "Tests did not run successfully."

def test_build_out_log_contents():
    # Run build.sh to ensure it produces the expected log
    result = subprocess.run(
        [BUILD_SH_PATH],
        cwd=PROJECT_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    assert os.path.isfile(LOG_PATH), f"Log file missing: {LOG_PATH}"

    with open(LOG_PATH, "r") as f:
        log_content = f.read()

    assert "BenchmarkEvaluate" in log_content, "Go benchmark output not found in build_out.log"
    assert "OK" in log_content, "Python test success (OK) not found in build_out.log"
    assert "FAILED" not in log_content.upper(), "Found 'FAILED' in build_out.log, tests might be failing."