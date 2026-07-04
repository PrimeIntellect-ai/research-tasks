# test_final_state.py
import os

def test_link_target_content():
    target_file = "/home/user/link_target.txt"
    assert os.path.isfile(target_file), f"Expected output file {target_file} is missing."

    with open(target_file, "r") as f:
        content = f.read()

    expected_content = "/home/user/mirror/libcore-1.10.0.so"
    assert content == expected_content, f"Content of {target_file} is incorrect. Expected '{expected_content}', got '{content}'."

def test_resolve_script_exists():
    script_file = "/home/user/resolve.py"
    assert os.path.isfile(script_file), f"Expected script {script_file} is missing."