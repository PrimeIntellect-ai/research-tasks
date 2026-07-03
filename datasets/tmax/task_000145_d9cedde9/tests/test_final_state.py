# test_final_state.py
import os

def test_result_file_exists():
    """Check if the result file was created."""
    assert os.path.isfile("/home/user/result.txt"), "The file /home/user/result.txt does not exist. Did you run the script?"

def test_result_file_content():
    """Check if the result file contains the correct total bytes."""
    assert os.path.isfile("/home/user/result.txt"), "The file /home/user/result.txt does not exist."
    with open("/home/user/result.txt", "r") as f:
        content = f.read().strip()

    assert content == "381000", f"Expected total bytes to be '381000', but got '{content}'. The script might still have bugs."