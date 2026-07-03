# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_verification_log_correct():
    verification_log = "/home/user/log_processor/verification.log"
    assert os.path.isfile(verification_log), f"File {verification_log} is missing."

    expected_lines = [
        "1696161000 Message 1 from Asia",
        "1696161300 Message 1 from EU",
        "1696161600 Message 1 from US",
        "1696161720 Message 2 from EU",
        "1696161900 Message 2 from US",
        "1696162200 Message 2 from Asia"
    ]

    with open(verification_log, "rb") as f:
        content = f.read()

    assert b"\x00" not in content, "Null bytes were not stripped from the final log."

    lines = content.decode("utf-8").strip().split("\n")
    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines, but got {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual.strip() == expected, f"Line {i+1} mismatch. Expected: '{expected}', Got: '{actual.strip()}'"

def test_test_sh_exists_and_passes():
    test_sh = "/home/user/log_processor/test.sh"
    assert os.path.isfile(test_sh), f"File {test_sh} is missing."

    st = os.stat(test_sh)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {test_sh} is not executable."

    result = subprocess.run([test_sh], capture_output=True)
    assert result.returncode == 0, f"test.sh failed with return code {result.returncode}.\nStdout: {result.stdout.decode()}\nStderr: {result.stderr.decode()}"

def test_fixed_script_exists():
    fixed_script = "/home/user/log_processor/process_logs_fixed.sh"
    assert os.path.isfile(fixed_script), f"File {fixed_script} is missing."