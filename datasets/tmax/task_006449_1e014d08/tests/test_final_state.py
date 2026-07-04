# test_final_state.py
import os
import json
import subprocess

def test_report_content():
    """Verify that the report file exists and contains the correct JSON data."""
    report_path = '/home/user/report.json'
    assert os.path.exists(report_path), f"Report file {report_path} does not exist. Did you run the script?"

    with open(report_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {report_path} is not valid JSON."

    assert "max_downtime_minutes" in data, "Key 'max_downtime_minutes' is missing in report.json."

    # The longest downtime streak is 4 at the end of the array.
    expected_downtime = 4
    actual_downtime = data["max_downtime_minutes"]
    assert actual_downtime == expected_downtime, (
        f"Expected max_downtime_minutes to be {expected_downtime}, "
        f"but got {actual_downtime}. The algorithmic bug might not be fully fixed."
    )

def test_monitor_script_runs_successfully():
    """Verify that the script runs successfully with the virtual environment and correct env variable."""
    script_path = '/home/user/monitor.py'
    python_bin = '/home/user/venv/bin/python'

    assert os.path.exists(python_bin), f"Python binary missing at {python_bin}"
    assert os.path.exists(script_path), f"Monitor script missing at {script_path}"

    env = os.environ.copy()
    env['UPTIME_DATA_PATH'] = '/home/user/uptime_data.json'

    result = subprocess.run(
        [python_bin, script_path],
        env=env,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, (
        f"Script failed to execute. This could be due to unresolved dependency conflicts "
        f"or syntax errors. stderr:\n{result.stderr}"
    )