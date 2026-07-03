# test_final_state.py
import os

def test_best_version_file_exists():
    assert os.path.isfile("/home/user/best_version.txt"), "The file /home/user/best_version.txt was not created."

def test_best_version_content():
    with open("/home/user/best_version.txt", "r") as f:
        content = f.read().strip()
    assert content == "1.10.0", f"Expected '1.10.0' in /home/user/best_version.txt, but got '{content}'"