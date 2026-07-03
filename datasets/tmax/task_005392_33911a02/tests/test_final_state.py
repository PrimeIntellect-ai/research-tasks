# test_final_state.py

import os
import re
import pytest

PROJECT_DIR = "/home/user/sim_project"
PROFILE_SCRIPT = os.path.join(PROJECT_DIR, "profile_runs.sh")
STABLE_TIMES_FILE = os.path.join(PROJECT_DIR, "stable_times.txt")
BOOTSTRAP_SCRIPT = os.path.join(PROJECT_DIR, "bootstrap_ci.sh")
CI_RESULTS_FILE = os.path.join(PROJECT_DIR, "ci_results.txt")

def test_profile_script_exists():
    assert os.path.isfile(PROFILE_SCRIPT), f"File {PROFILE_SCRIPT} does not exist."
    assert os.access(PROFILE_SCRIPT, os.X_OK), f"File {PROFILE_SCRIPT} is not executable."

def test_bootstrap_script_exists():
    assert os.path.isfile(BOOTSTRAP_SCRIPT), f"File {BOOTSTRAP_SCRIPT} does not exist."
    assert os.access(BOOTSTRAP_SCRIPT, os.X_OK), f"File {BOOTSTRAP_SCRIPT} is not executable."

def test_stable_times_file_exists_and_valid():
    assert os.path.isfile(STABLE_TIMES_FILE), f"File {STABLE_TIMES_FILE} does not exist."
    with open(STABLE_TIMES_FILE, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, f"File {STABLE_TIMES_FILE} is empty."

    for line in lines:
        try:
            val = float(line)
            assert val > 0, f"Stable time {val} should be positive."
        except ValueError:
            pytest.fail(f"Invalid non-numeric value found in {STABLE_TIMES_FILE}: {line}")

def test_ci_results_format_and_values():
    assert os.path.isfile(CI_RESULTS_FILE), f"File {CI_RESULTS_FILE} does not exist."

    with open(CI_RESULTS_FILE, 'r') as f:
        content = f.read().strip()

    lines = content.split('\n')
    assert len(lines) == 2, f"{CI_RESULTS_FILE} must contain exactly two lines."

    lower_match = re.match(r"^Lower CI:\s*([0-9.]+)$", lines[0])
    upper_match = re.match(r"^Upper CI:\s*([0-9.]+)$", lines[1])

    assert lower_match, f"First line of {CI_RESULTS_FILE} is malformed. Expected 'Lower CI: <value>'."
    assert upper_match, f"Second line of {CI_RESULTS_FILE} is malformed. Expected 'Upper CI: <value>'."

    lower_val = float(lower_match.group(1))
    upper_val = float(upper_match.group(1))

    assert lower_val <= upper_val, "Lower CI must be less than or equal to Upper CI."

    # Check plausible bounds (approx 50ms to 120ms considering bash overhead)
    assert 40 <= lower_val <= 150, f"Lower CI {lower_val} is outside the plausible range (40-150 ms)."
    assert 40 <= upper_val <= 150, f"Upper CI {upper_val} is outside the plausible range (40-150 ms)."