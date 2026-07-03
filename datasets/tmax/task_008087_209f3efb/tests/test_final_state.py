# test_final_state.py

import os
import base64

def test_malicious_paths_file():
    """Test that malicious_paths.txt exists and contains the correct sorted paths."""
    file_path = "/home/user/malicious_paths.txt"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_paths = [
        "../../tmp/hidden.sh",
        "../../var/www/html/shell.php",
        "../../../etc/passwd"
    ]

    # The instructions specified sorting alphabetically
    expected_paths.sort()

    assert lines == expected_paths, f"The contents of {file_path} do not match the expected sorted malicious paths. Found: {lines}"

def test_payload_file():
    """Test that test_payload.txt exists and contains the correct Base64 encoded payload."""
    file_path = "/home/user/test_payload.txt"
    assert os.path.isfile(file_path), f"The file {file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip()

    target_path = "../../../../home/user/proof.txt"
    expected_base64 = base64.b64encode(target_path.encode('utf-8')).decode('utf-8')

    assert content == expected_base64, f"The content of {file_path} does not match the expected Base64 payload. Expected '{expected_base64}', got '{content}'."