# test_final_state.py

import os

def test_crash_packet_file_exists():
    """Check that the crash_packet.txt file has been created."""
    file_path = "/home/user/crash_packet.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist. Did you save the packet number?"

def test_crash_packet_content():
    """Verify that the crash_packet.txt file contains the correct packet number."""
    file_path = "/home/user/crash_packet.txt"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, 'r') as f:
        content = f.read().strip()

    assert content == "42", f"Expected crash packet number '42', but got '{content}'."