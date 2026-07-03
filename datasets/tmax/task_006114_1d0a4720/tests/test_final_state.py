# test_final_state.py

import os

def test_blocked_ip_file():
    file_path = "/home/user/blocked_ip.txt"

    assert os.path.exists(file_path), f"Error: The file {file_path} does not exist. Did the script run successfully?"
    assert os.path.isfile(file_path), f"Error: {file_path} is not a valid file."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_ip = "10.5.22.114"
    assert content == expected_ip, f"Error: The blocked IP is incorrect. Expected '{expected_ip}', but found '{content}'."

def test_malicious_filename_file():
    file_path = "/home/user/malicious_filename.txt"

    assert os.path.exists(file_path), f"Error: The file {file_path} does not exist. Did the script extract the filename?"
    assert os.path.isfile(file_path), f"Error: {file_path} is not a valid file."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_filename = "../../../../etc/shadow"
    assert content == expected_filename, f"Error: The extracted malicious filename is incorrect. Expected '{expected_filename}', but found '{content}'."