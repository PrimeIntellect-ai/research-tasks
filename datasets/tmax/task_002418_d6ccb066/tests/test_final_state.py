# test_final_state.py

import os
import stat
import pytest

def test_fuzz_script_exists_and_executable():
    path = '/home/user/fuzz.sh'
    assert os.path.isfile(path), f"Fuzzing script {path} does not exist."

    st = os.stat(path)
    assert bool(st.st_mode & (stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)), f"Fuzzing script {path} is not executable."

def test_final_timeline_log():
    path = '/home/user/final_timeline.log'
    assert os.path.isfile(path), f"Final timeline log {path} does not exist."

    expected_lines = [
        "1672531200 [INFO] Service A started",
        "1672531202 [INFO] Service B started",
        "1672531205 [DEBUG] Connecting to DB",
        "1672531210 [WARN] High memory usage",
        "1672531215 [INFO] DB connected",
        "1672531220 [INFO] Shutdown"
    ]

    with open(path, 'r') as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"Contents of {path} do not match the expected merged output.\n"
        f"Expected: {expected_lines}\n"
        f"Actual: {actual_lines}"
    )

def test_merge_timeline_script_fixed():
    path = '/home/user/merge_timeline.sh'
    assert os.path.isfile(path), f"Script {path} does not exist."

    # We can do a basic test to see if it works with empty files (fixing the crash)
    # and if it outputs the correct number of lines. But since the prompt specifies
    # checking the final_timeline.log and fuzz.sh, we will rely primarily on those.
    # However, to be robust, we can run the script on empty files to ensure it doesn't crash.
    import subprocess

    empty1 = '/tmp/empty1.log'
    empty2 = '/tmp/empty2.log'
    open(empty1, 'w').close()
    open(empty2, 'w').close()

    try:
        result = subprocess.run([path, empty1, empty2], capture_output=True, text=True)
        assert result.returncode == 0, f"{path} still crashes (non-zero exit code) on empty files."
    finally:
        if os.path.exists(empty1):
            os.remove(empty1)
        if os.path.exists(empty2):
            os.remove(empty2)