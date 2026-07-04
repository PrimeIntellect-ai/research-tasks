# test_final_state.py
import os
import pytest

def test_c2_url_extracted_correctly():
    """Verify that the C2 URL was correctly extracted and saved."""
    output_path = "/home/user/c2_url.txt"
    assert os.path.isfile(output_path), f"The file {output_path} does not exist. Did you save the extracted URL?"

    with open(output_path, "r") as f:
        content = f.read().strip()

    expected_url = "https://malicious-c2.local/gate/v2_init/cmd"
    assert content == expected_url, f"The extracted URL is incorrect. Expected '{expected_url}', but got '{content}'."

def test_mutex_file_created():
    """Verify that the mutex file required to bypass the crash was created."""
    mutex_path = "/tmp/.sys_mutex_lock"
    assert os.path.isfile(mutex_path), f"The mutex file {mutex_path} was not created. The malware would still crash early."