# test_final_state.py
import os
import json
import subprocess
import math

REPORT_FILE = "/home/user/forensics_report.json"
EXPECTED_BAD_COMMIT_FILE = "/tmp/expected_bad_commit.txt"
REPO_DIR = "/home/user/uptime_monitor"
RUN_ANALYSIS_FILE = os.path.join(REPO_DIR, "run_analysis.py")

def test_forensics_report_exists():
    assert os.path.isfile(REPORT_FILE), f"Forensics report is missing at {REPORT_FILE}"

def test_forensics_report_structure_and_values():
    with open(REPORT_FILE, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            assert False, "Forensics report is not valid JSON."

    assert "bad_commit" in report, "Key 'bad_commit' missing in forensics report."
    assert "fixed_metric" in report, "Key 'fixed_metric' missing in forensics report."

    # Validate bad_commit
    assert os.path.isfile(EXPECTED_BAD_COMMIT_FILE), f"Missing {EXPECTED_BAD_COMMIT_FILE}"
    with open(EXPECTED_BAD_COMMIT_FILE, "r") as f:
        expected_bad_commit = f.read().strip()

    assert report["bad_commit"] == expected_bad_commit, \
        f"Expected bad_commit to be {expected_bad_commit}, but got {report['bad_commit']}"

    # Validate fixed_metric
    fixed_metric = report["fixed_metric"]
    assert isinstance(fixed_metric, (int, float)), "fixed_metric must be a numeric value."

    # Calculate expected metric to avoid hardcoding brittle constants
    import random
    random.seed(42)
    latencies = [random.uniform(20, 100) for _ in range(50)]
    alpha = 0.3
    metric = latencies[0]
    for d in latencies[1:]:
        metric = (alpha * d) + ((1 - alpha) * metric)
    expected_metric = round(metric, 2)

    assert math.isclose(fixed_metric, expected_metric, rel_tol=1e-2), \
        f"Expected fixed_metric to be approximately {expected_metric}, but got {fixed_metric}"

def test_script_execution_succeeds():
    # The script should now run without crashing (env var fixed, math fixed)
    result = subprocess.run(
        ["python3", RUN_ANALYSIS_FILE],
        cwd=REPO_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, \
        f"run_analysis.py failed to execute. stderr: {result.stderr}"
    assert "Final metric:" in result.stdout, \
        "run_analysis.py did not print the expected output format."