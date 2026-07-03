# test_final_state.py

import os
import stat

def test_process_executable_exists():
    """Test that the compiled executable exists and has execute permissions."""
    executable_path = "/home/user/process"
    assert os.path.isfile(executable_path), f"Compiled executable not found at {executable_path}"

    st = os.stat(executable_path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"File {executable_path} is not executable"

def test_answer_correct():
    """Test that answer.txt contains the correct target ID."""
    answer_path = "/home/user/answer.txt"
    assert os.path.isfile(answer_path), f"Output file not found at {answer_path}"

    with open(answer_path, "r") as f:
        content = f.read().strip()

    assert content == "103", f"Expected answer.txt to contain '103', but got '{content}'"

def test_valgrind_no_leaks():
    """Test that valgrind.log confirms no memory leaks."""
    log_path = "/home/user/valgrind.log"
    assert os.path.isfile(log_path), f"Valgrind log not found at {log_path}"

    expected_phrase = "All heap blocks were freed -- no leaks are possible"

    with open(log_path, "r") as f:
        content = f.read()

    assert expected_phrase in content, f"Valgrind log does not contain the expected success message: '{expected_phrase}'"