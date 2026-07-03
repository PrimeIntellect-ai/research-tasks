# test_final_state.py

import os
import stat
import pytest

def test_clean_data_script_exists_and_executable():
    script_path = "/home/user/clean_data.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"The script {script_path} is not executable."

def test_clean_telemetry_output():
    output_path = "/home/user/clean_telemetry.csv"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

    expected_content = """timestamp,sensor_id,masked_ip,temperature
2023-10-01T10:00:00Z,S1,192.168.1.XXX,22.1
2023-10-01T10:01:00Z,S2,10.0.0.XXX,24.5
2023-10-01T10:03:00Z,S3,172.16.0.XXX,21.0
2023-10-01T10:04:00Z,S4,8.8.8.XXX,-5.4"""

    with open(output_path, "r", encoding="utf-8") as f:
        actual_content = f.read().strip()

    # Normalize line endings just in case
    actual_lines = [line.strip() for line in actual_content.splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.splitlines() if line.strip()]

    assert actual_lines == expected_lines, f"The content of {output_path} does not match the expected output."