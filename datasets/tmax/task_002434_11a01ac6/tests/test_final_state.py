# test_final_state.py

import os

def test_results_log_exists():
    path = "/home/user/results.log"
    assert os.path.isfile(path), f"The file {path} does not exist. Did you run the Python server and the Rust client?"

def test_results_log_content():
    path = "/home/user/results.log"
    assert os.path.isfile(path), f"The file {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    expected = "SUCCESS: Protocol complete and validated.\n"
    assert content == expected, f"Expected the log file to contain exactly '{expected}', but got '{content}'."