# test_final_state.py

import os
import re
import subprocess
import pytest

SIM_PROJECT_DIR = "/home/user/sim_project"
INTEGRATOR_SCRIPT = os.path.join(SIM_PROJECT_DIR, "integrator.sh")
RUN_ALL_SCRIPT = os.path.join(SIM_PROJECT_DIR, "run_all.sh")
RESULTS_FILE = os.path.join(SIM_PROJECT_DIR, "results.txt")
BOOTSTRAP_SCRIPT = os.path.join(SIM_PROJECT_DIR, "bootstrap.sh")
CI_LOG_FILE = os.path.join(SIM_PROJECT_DIR, "ci.log")
TEST_SCRIPT = os.path.join(SIM_PROJECT_DIR, "test.sh")

def test_integrator_script():
    assert os.path.isfile(INTEGRATOR_SCRIPT), f"File {INTEGRATOR_SCRIPT} is missing."
    assert os.access(INTEGRATOR_SCRIPT, os.X_OK), f"File {INTEGRATOR_SCRIPT} is not executable."

    with open(INTEGRATOR_SCRIPT, "r") as f:
        content = f.read()

    assert "0.5" in content, "integrator.sh does not appear to use 0.5 for dt calculation."
    assert "awk" in content, "integrator.sh does not appear to use awk for floating point math."

def test_run_all_script():
    assert os.path.isfile(RUN_ALL_SCRIPT), f"File {RUN_ALL_SCRIPT} is missing."
    assert os.access(RUN_ALL_SCRIPT, os.X_OK), f"File {RUN_ALL_SCRIPT} is not executable."

    with open(RUN_ALL_SCRIPT, "r") as f:
        content = f.read()

    assert re.search(r"xargs\s+-P\s*4", content), "run_all.sh does not contain 'xargs -P 4' or 'xargs -P4'."

def test_results_txt():
    assert os.path.isfile(RESULTS_FILE), f"File {RESULTS_FILE} is missing. Did run_all.sh execute?"

    with open(RESULTS_FILE, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 100, f"{RESULTS_FILE} should contain exactly 100 lines, found {len(lines)}."

    for line in lines:
        try:
            float(line)
        except ValueError:
            pytest.fail(f"Line '{line}' in {RESULTS_FILE} is not a valid float.")

def test_bootstrap_script():
    assert os.path.isfile(BOOTSTRAP_SCRIPT), f"File {BOOTSTRAP_SCRIPT} is missing."
    assert os.access(BOOTSTRAP_SCRIPT, os.X_OK), f"File {BOOTSTRAP_SCRIPT} is not executable."

def test_ci_log():
    assert os.path.isfile(CI_LOG_FILE), f"File {CI_LOG_FILE} is missing. Did bootstrap.sh execute?"

    with open(CI_LOG_FILE, "r") as f:
        content = f.read().strip()

    match = re.fullmatch(r"([0-9\.]+),([0-9\.]+)", content)
    assert match, f"{CI_LOG_FILE} does not match the required format 'lower_bound,upper_bound'."

    lower, upper = float(match.group(1)), float(match.group(2))
    assert lower <= upper, "Lower bound is greater than upper bound in ci.log."

def test_test_script():
    assert os.path.isfile(TEST_SCRIPT), f"File {TEST_SCRIPT} is missing."
    assert os.access(TEST_SCRIPT, os.X_OK), f"File {TEST_SCRIPT} is not executable."

    result = subprocess.run([TEST_SCRIPT], cwd=SIM_PROJECT_DIR, capture_output=True)
    assert result.returncode == 0, f"test.sh failed with exit code {result.returncode}. Output: {result.stderr.decode()}"