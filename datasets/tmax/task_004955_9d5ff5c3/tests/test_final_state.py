# test_final_state.py
import os
import pytest

def test_max_timestamp_file_exists_and_correct():
    path = "/home/user/uptime_monitor/max_timestamp.txt"
    assert os.path.isfile(path), f"Output file {path} does not exist. Did you run the script?"

    with open(path, 'r') as f:
        content = f.read().strip()

    expected_value = "3000000000"
    assert content == expected_value, f"Expected max timestamp to be {expected_value}, but got {content}"

def test_process_heartbeats_script_fixed():
    path = "/home/user/uptime_monitor/process_heartbeats.py"
    assert os.path.isfile(path), f"Python script {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    assert "struct.unpack('>I'" in content or "struct.unpack(\">I\"" in content or "struct.unpack( '>I'" in content, \
        "The script does not appear to use the correct unsigned integer format (>I) for unpacking the timestamp."
    assert "struct.unpack('>i'" not in content, \
        "The script still contains the buggy signed integer format (>i)."