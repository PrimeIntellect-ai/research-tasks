# test_final_state.py

import os
import subprocess

REPORT_FILE = "/home/user/profiler_report.txt"
RUN_SCRIPT = "/home/user/profiler_repo/run_analysis.sh"

def test_profiler_report_exists():
    assert os.path.isfile(REPORT_FILE), f"Report file {REPORT_FILE} does not exist."

def test_profiler_report_content():
    with open(REPORT_FILE, "r") as f:
        lines = [line.strip() for line in f.read().strip().splitlines()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {REPORT_FILE}, found {len(lines)}."

    assert lines[0] == "a9f8b7c6d5e4", f"Line 1 is incorrect. Expected 'a9f8b7c6d5e4', got '{lines[0]}'."
    assert lines[1] == "--dev-xc92k1l8m4n5", f"Line 2 is incorrect. Expected '--dev-xc92k1l8m4n5', got '{lines[1]}'."
    assert lines[2] == "90", f"Line 3 is incorrect. Expected '90', got '{lines[2]}'."

def test_run_analysis_script_fixed():
    assert os.path.isfile(RUN_SCRIPT), f"Script {RUN_SCRIPT} is missing."

    # Run the script with 150 and 100
    result = subprocess.run([RUN_SCRIPT, "150", "100"], capture_output=True, text=True)
    assert result.returncode == 0, f"Script {RUN_SCRIPT} failed to execute."

    output = result.stdout.strip()
    assert output == "90", f"Script {RUN_SCRIPT} did not output the correct value. Expected '90', got '{output}'."