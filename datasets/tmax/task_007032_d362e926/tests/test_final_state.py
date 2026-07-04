# test_final_state.py

import os
import stat
import subprocess
import re
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/analyze_sensors.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_script_execution_and_output():
    script_path = "/home/user/analyze_sensors.sh"
    report_path = "/home/user/analysis_report.txt"

    # Remove report if it already exists to verify the script creates it
    if os.path.exists(report_path):
        os.remove(report_path)

    # Execute the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed to execute. stderr: {result.stderr}"

    # Verify report creation
    assert os.path.isfile(report_path), f"Report {report_path} was not created by the script."

    # Read report content
    with open(report_path, "r") as f:
        content = f.read()

    # Parse metrics
    match_pca = re.search(r"PC1_Variance_Ratio:\s*([0-9.]+)", content)
    match_ttest = re.search(r"T-Test_P-Value:\s*([0-9.]+)", content)

    assert match_pca is not None, f"PC1_Variance_Ratio not found in report. Content was:\n{content}"
    assert match_ttest is not None, f"T-Test_P-Value not found in report. Content was:\n{content}"

    pca_val = float(match_pca.group(1))
    ttest_val = float(match_ttest.group(1))

    # Assert values within tolerance
    assert abs(pca_val - 0.9351) <= 0.0015, f"PC1_Variance_Ratio expected ~0.9351, got {pca_val}"
    assert abs(ttest_val - 0.1160) <= 0.0015, f"T-Test_P-Value expected ~0.1160, got {ttest_val}"