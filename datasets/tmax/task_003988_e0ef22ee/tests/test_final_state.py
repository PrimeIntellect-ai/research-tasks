# test_final_state.py
import os
import re
import stat
import pytest

def test_monitor_rs_exists():
    """Verify that the Rust source file exists."""
    file_path = "/home/user/monitor.rs"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

def test_ci_step_sh_exists_and_executable():
    """Verify that the CI script exists and is executable."""
    file_path = "/home/user/ci_step.sh"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    st = os.stat(file_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {file_path} is not executable."

def test_build_log_exists_and_format():
    """Verify that build.log exists and contains the correct FAIL message with the date format."""
    log_path = "/home/user/build.log"
    assert os.path.isfile(log_path), f"File {log_path} is missing. Did you run the script?"

    with open(log_path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) > 0, f"File {log_path} is empty."

    # The last line should be the one appended by the script
    last_line = lines[-1].strip()

    # Expected format: Status: FAIL - YYYY-MM-DD HH:MM:SS
    # Since the payload is 6000 bytes, it should FAIL.
    pattern = r"^Status: FAIL - \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$"

    match = re.match(pattern, last_line)
    assert match is not None, (
        f"The last line in {log_path} does not match the expected format or status. "
        f"Expected pattern '{pattern}', but got: '{last_line}'"
    )

def test_compiled_binary_exists():
    """Verify that the Rust program was compiled."""
    binary_path = "/home/user/monitor"
    assert os.path.isfile(binary_path), f"Compiled binary {binary_path} is missing. The CI script should compile monitor.rs."

    st = os.stat(binary_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Compiled binary {binary_path} is not executable."