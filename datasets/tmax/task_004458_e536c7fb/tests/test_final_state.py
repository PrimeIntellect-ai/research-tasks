# test_final_state.py

import os
import subprocess
import pytest

POISON_FILE = "/home/user/poison.txt"
MRE_FILE = "/home/user/mre.py"
EXPECTED_URL = "http://legacy.service.local/health?debug=memleak"

def test_poison_file_exists_and_correct():
    assert os.path.isfile(POISON_FILE), f"Expected file {POISON_FILE} does not exist."

    with open(POISON_FILE, "r") as f:
        content = f.read()

    assert content == EXPECTED_URL, (
        f"Contents of {POISON_FILE} are incorrect.\n"
        f"Expected: {EXPECTED_URL!r}\n"
        f"Got: {content!r}"
    )

def test_mre_script_exists_and_crashes():
    assert os.path.isfile(MRE_FILE), f"Expected file {MRE_FILE} does not exist."

    # Run the MRE script
    env = os.environ.copy()
    env["PYTHONPATH"] = "/home/user"

    result = subprocess.run(
        ["python3", MRE_FILE],
        cwd="/home/user",
        env=env,
        capture_output=True,
        text=True
    )

    # The script is expected to crash, so returncode should be non-zero
    assert result.returncode != 0, "Expected mre.py to crash (return non-zero exit code), but it succeeded."

    # The expected crash is a MemoryError
    assert "MemoryError" in result.stderr, (
        "Expected mre.py to raise a MemoryError, but it did not.\n"
        f"Standard Error output:\n{result.stderr}"
    )