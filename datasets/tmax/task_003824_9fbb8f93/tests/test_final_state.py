# test_final_state.py

import os
import json
import subprocess
import tempfile
import pytest

def test_process_asset_sh_fixed():
    """Verify that process_asset.sh has been fixed to handle spaces in filenames."""
    script_path = '/home/user/build_env/process_asset.sh'
    assert os.path.isfile(script_path), f"Script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    # Create a temporary file with a space in the name
    with tempfile.TemporaryDirectory() as tmpdir:
        test_file = os.path.join(tmpdir, "test file with spaces.txt")
        with open(test_file, 'w') as f:
            f.write("hello world")

        # Run the script
        result = subprocess.run([script_path, test_file], capture_output=True, text=True)
        assert result.returncode == 0, f"process_asset.sh failed when processing a file with spaces. Error: {result.stderr}"

def test_regression_script_exists_and_runs():
    """Verify that test_regression.py exists, runs successfully, and cleans up after itself."""
    script_path = '/home/user/build_env/test_regression.py'
    assert os.path.isfile(script_path), f"Regression test script {script_path} is missing."

    dummy_file = '/home/user/build_env/mock data file.txt'

    # Ensure dummy file doesn't exist before running
    if os.path.exists(dummy_file):
        os.remove(dummy_file)

    # Run the regression test script
    result = subprocess.run(['python3', script_path], capture_output=True, text=True, cwd='/home/user/build_env')
    assert result.returncode == 0, f"test_regression.py failed to run. Output: {result.stderr or result.stdout}"

    # Verify cleanup
    assert not os.path.exists(dummy_file), "test_regression.py did not clean up the dummy file 'mock data file.txt'."

def test_report_json_correct():
    """Verify that report.json exists and contains the correct findings."""
    report_path = '/home/user/report.json'
    assert os.path.isfile(report_path), f"Report file {report_path} is missing."

    with open(report_path, 'r') as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Report file {report_path} is not valid JSON.")

    assert "failed_uri_from_pcap" in report_data, "Key 'failed_uri_from_pcap' is missing in report.json."
    assert "server_log_timestamp" in report_data, "Key 'server_log_timestamp' is missing in report.json."

    assert report_data["failed_uri_from_pcap"] == "/data%20file.csv", \
        f"Incorrect failed_uri_from_pcap. Expected '/data%20file.csv', got '{report_data['failed_uri_from_pcap']}'."

    assert report_data["server_log_timestamp"] == 1700000005, \
        f"Incorrect server_log_timestamp. Expected 1700000005, got '{report_data['server_log_timestamp']}'."