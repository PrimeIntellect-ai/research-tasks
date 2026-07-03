# test_final_state.py

import os
import subprocess
import pytest

def test_report_file_exists_and_content_correct():
    report_path = "/home/user/output/report.txt"
    assert os.path.exists(report_path), f"Report file was not created at {report_path}"

    with open(report_path, 'r') as f:
        report_content = f.read()

    expected_temp_line = "Temperature: Min 22.50, Max 24.00, Avg 23.25"
    expected_hum_line = "Humidity: Min 45.00, Max 48.00, Avg 46.50"

    assert expected_temp_line in report_content, f"Temperature metrics incorrect or not formatted properly in {report_path}. Expected to find: '{expected_temp_line}'"
    assert expected_hum_line in report_content, f"Humidity metrics incorrect or not formatted properly in {report_path}. Expected to find: '{expected_hum_line}'"

def test_pipeline_script_exists_and_executable():
    wrapper_path = "/home/user/run_pipeline.sh"
    assert os.path.exists(wrapper_path), f"Wrapper script not found at {wrapper_path}"
    assert os.access(wrapper_path, os.X_OK), f"Wrapper script at {wrapper_path} is not executable"

def test_python_script_exists():
    script_path = "/home/user/process_sensor.py"
    assert os.path.exists(script_path), f"Python script not found at {script_path}"

def test_crontab_configured():
    try:
        crontab_out = subprocess.check_output(["crontab", "-l"]).decode('utf-8')
    except subprocess.CalledProcessError:
        pytest.fail("Crontab was not configured for the user")

    # Check for 15 minute intervals
    valid_schedules = ["*/15 * * * *", "0,15,30,45 * * * *"]
    schedule_found = any(sched in crontab_out for sched in valid_schedules)

    assert schedule_found, "Crontab not scheduled for every 15 mins. Expected '*/15 * * * *' or '0,15,30,45 * * * *'"
    assert "/home/user/run_pipeline.sh" in crontab_out, "Crontab does not execute the wrapper script /home/user/run_pipeline.sh"