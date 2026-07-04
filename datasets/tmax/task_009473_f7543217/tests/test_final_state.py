# test_final_state.py

import os
import subprocess
import pytest

def test_server_fixed_exists_and_executable():
    path = '/home/user/server_fixed'
    assert os.path.isfile(path), f"The compiled executable {path} is missing."
    assert os.access(path, os.X_OK), f"The file {path} is not executable."

def test_poison_pill_content():
    path = '/home/user/poison_pill.txt'
    assert os.path.isfile(path), f"The file {path} is missing."
    with open(path, 'r') as f:
        content = f.read().strip()

    assert content.startswith("CMD:"), "The poison pill string must start with 'CMD:' to trigger the vulnerable code path."
    assert ";" not in content, "The poison pill string must not contain a ';' character, as that would prevent the infinite loop in the original code."

def test_server_fixed_no_infinite_loop():
    path = '/home/user/server_fixed'
    pill_path = '/home/user/poison_pill.txt'

    with open(pill_path, 'r') as f:
        pill_content = f.read().strip()

    # We add "QUIT\n" to ensure the program exits cleanly after processing the input
    input_data = f"{pill_content}\nQUIT\n"

    try:
        # Run the server with a strict timeout to ensure it doesn't hang
        result = subprocess.run(
            [path],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=2.0
        )
    except subprocess.TimeoutExpired:
        pytest.fail("The fixed server timed out (infinite loop) when fed the poison pill data.")

    assert result.returncode == 0, "The server did not exit with a 0 return code."

def test_server_fixed_no_memory_leak():
    path = '/home/user/server_fixed'
    pill_path = '/home/user/poison_pill.txt'

    with open(pill_path, 'r') as f:
        pill_content = f.read().strip()

    input_data = f"CMD:VALID;\n{pill_content}\nQUIT\n"

    # Run under valgrind to check for memory leaks
    try:
        result = subprocess.run(
            ['valgrind', '--leak-check=full', '--error-exitcode=1', path],
            input=input_data,
            text=True,
            capture_output=True,
            timeout=5.0
        )
    except FileNotFoundError:
        pytest.fail("valgrind is not installed or not in PATH.")
    except subprocess.TimeoutExpired:
        pytest.fail("The valgrind process timed out.")

    # Valgrind outputs to stderr
    stderr_lower = result.stderr.lower()

    # Check if valgrind detected any leaks
    if "definitely lost:" in stderr_lower or "indirectly lost:" in stderr_lower:
        # If the error-exitcode triggered, or we see lost bytes
        if "definitely lost: 0 bytes" not in stderr_lower:
            pytest.fail(f"Memory leak detected by valgrind:\n{result.stderr}")