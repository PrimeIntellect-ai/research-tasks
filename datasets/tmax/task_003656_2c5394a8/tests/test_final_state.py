# test_final_state.py

import os

def test_success_log_exists():
    path = "/home/user/migration/success.log"
    assert os.path.isfile(path), f"File {path} does not exist. Ensure you ran the exact valgrind command to generate this log file."

def test_success_log_output():
    path = "/home/user/migration/success.log"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    assert "Happy Python Migration!" in content, "The log does not contain the correctly processed string 'Happy Python Migration!'. Check if the C extension works correctly."

def test_success_log_valgrind_leak_check():
    path = "/home/user/migration/success.log"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()

    expected_leak_status = "definitely lost: 0 bytes in 0 blocks"
    assert expected_leak_status in content, f"The Valgrind leak check did not report '{expected_leak_status}'. The memory leak might not be fixed properly, or the valgrind command was not run correctly."