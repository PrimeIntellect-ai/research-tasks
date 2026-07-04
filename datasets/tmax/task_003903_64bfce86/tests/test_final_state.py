# test_final_state.py
import os
import subprocess

def test_output_txt_exists_and_correct():
    output_path = "/home/user/output.txt"
    assert os.path.isfile(output_path), f"{output_path} does not exist."

    with open(output_path, "r") as f:
        content = f.read().strip().splitlines()

    expected_lines = [
        "ID 1: 3.000000",
        "ID 3: 4.000000",
        "ID 4: 5.000000"
    ]

    assert len(content) == len(expected_lines), f"Expected {len(expected_lines)} lines in output.txt, but got {len(content)}."

    for i, (actual, expected) in enumerate(zip(content, expected_lines)):
        assert actual.strip() == expected, f"Line {i+1} mismatch: expected '{expected}', got '{actual.strip()}'"

def test_executable_exists():
    exe_path = "/home/user/processor"
    assert os.path.isfile(exe_path), f"Compiled binary {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable."

def test_no_memory_leaks():
    # Run valgrind to check for memory leaks
    exe_path = "/home/user/processor"
    assert os.path.isfile(exe_path), f"Compiled binary {exe_path} does not exist."

    try:
        result = subprocess.run(
            ["valgrind", "--leak-check=full", "--error-exitcode=1", exe_path],
            capture_output=True,
            text=True,
            cwd="/home/user"
        )
        assert result.returncode == 0, f"Valgrind reported memory leaks or errors:\n{result.stderr}"
    except FileNotFoundError:
        # If valgrind is not installed, we can't test this, but we assume it's available in the environment
        pass