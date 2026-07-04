# test_final_state.py

import os
import re
import pytest

def test_scripts_exist_and_executable():
    process_script = "/home/user/process.sh"
    run_tests_script = "/home/user/run_tests.sh"

    assert os.path.isfile(process_script), f"The script {process_script} does not exist."
    assert os.access(process_script, os.X_OK), f"The script {process_script} is not executable."

    assert os.path.isfile(run_tests_script), f"The script {run_tests_script} does not exist."
    assert os.access(run_tests_script, os.X_OK), f"The script {run_tests_script} is not executable."

def test_plots_generated():
    plot1 = "/home/user/plots/exp_1_spectrum.png"
    plot2 = "/home/user/plots/exp_2_spectrum.png"

    assert os.path.isfile(plot1), f"The plot {plot1} was not generated."
    assert os.path.getsize(plot1) > 0, f"The plot {plot1} is empty."

    assert os.path.isfile(plot2), f"The plot {plot2} was not generated."
    assert os.path.getsize(plot2) > 0, f"The plot {plot2} is empty."

def test_regression_report_content():
    report_file = "/home/user/regression_report.txt"
    assert os.path.isfile(report_file), f"The report file {report_file} does not exist."

    with open(report_file, "r") as f:
        content = f.read()

    # Check for exp_1.log
    match1 = re.search(r'\[(PASS|FAIL)\]\s+exp_1\.log:\s+Expected\s+315\.83,\s+Got\s+([0-9\.]+)', content)
    assert match1 is not None, "Could not find properly formatted report line for exp_1.log in regression_report.txt."

    status1, got1_str = match1.groups()
    got1 = float(got1_str)
    assert abs(got1 - 315.83) <= 5.0, f"Calculated k for exp_1.log ({got1}) is not within 5.0 of expected 315.83."
    assert status1 == "PASS", f"Expected PASS for exp_1.log, but got {status1}."

    # Check for exp_2.log
    match2 = re.search(r'\[(PASS|FAIL)\]\s+exp_2\.log:\s+Expected\s+725\.71,\s+Got\s+([0-9\.]+)', content)
    assert match2 is not None, "Could not find properly formatted report line for exp_2.log in regression_report.txt."

    status2, got2_str = match2.groups()
    got2 = float(got2_str)
    assert abs(got2 - 725.71) <= 5.0, f"Calculated k for exp_2.log ({got2}) is not within 5.0 of expected 725.71."
    assert status2 == "PASS", f"Expected PASS for exp_2.log, but got {status2}."