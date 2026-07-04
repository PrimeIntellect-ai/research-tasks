# test_final_state.py
import os
import pytest

def test_culprit_ip_file_exists():
    file_path = "/home/user/culprit_ip.txt"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

def test_culprit_ip_content():
    file_path = "/home/user/culprit_ip.txt"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_ip = "192.168.205.77"
    assert content == expected_ip, f"Expected IP '{expected_ip}', but found '{content}' in {file_path}."