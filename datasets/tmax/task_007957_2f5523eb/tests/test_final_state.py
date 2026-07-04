# test_final_state.py

import os
import subprocess
import pytest

PROJECT_DIR = "/home/user/project"
MAKEFILE = os.path.join(PROJECT_DIR, "Makefile")
SCRIPT = "/home/user/build_and_verify.sh"
CHECKSUM_FILE = "/home/user/checksum.txt"

def get_expected_checksum():
    sum1 = 0
    sum2 = 0
    for n in range(1, 51):
        v = (n * n + 3 * n) % 256
        sum1 = (sum1 + v) % 255
        sum2 = (sum2 + sum1) % 255
    return (sum2 << 8) | sum1

def test_makefile_fixed():
    assert os.path.isfile(MAKEFILE), f"{MAKEFILE} is missing"

    # Run make clean to ensure a fresh build
    subprocess.run(["make", "clean"], cwd=PROJECT_DIR, capture_output=True)

    # Run make
    res = subprocess.run(["make"], cwd=PROJECT_DIR, capture_output=True)
    assert res.returncode == 0, f"make failed with output: {res.stderr.decode()}"

    app_path = os.path.join(PROJECT_DIR, "app")
    assert os.path.isfile(app_path), "make did not produce 'app' executable. The Makefile might not be linking correctly."

    # Run app
    res = subprocess.run(["./app"], cwd=PROJECT_DIR, capture_output=True)
    assert res.returncode == 0, f"./app failed with output: {res.stderr.decode()}"

    seq_path = os.path.join(PROJECT_DIR, "sequence.json")
    assert os.path.isfile(seq_path), "./app did not produce sequence.json"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT), f"{SCRIPT} is missing"
    assert os.access(SCRIPT, os.X_OK), f"{SCRIPT} is not executable"

def test_checksum_file():
    assert os.path.isfile(CHECKSUM_FILE), f"{CHECKSUM_FILE} is missing"
    with open(CHECKSUM_FILE, "r") as f:
        content = f.read().strip()

    expected = str(get_expected_checksum())
    assert content == expected, f"Expected checksum {expected}, got {content} in {CHECKSUM_FILE}"

def test_script_execution():
    # Remove the checksum file to ensure the script generates it
    if os.path.exists(CHECKSUM_FILE):
        os.remove(CHECKSUM_FILE)

    res = subprocess.run([SCRIPT], capture_output=True)
    assert res.returncode == 0, f"Script {SCRIPT} failed with exit code {res.returncode}. Error output: {res.stderr.decode()}"

    assert os.path.isfile(CHECKSUM_FILE), f"Script did not generate {CHECKSUM_FILE}"
    with open(CHECKSUM_FILE, "r") as f:
        content = f.read().strip()

    expected = str(get_expected_checksum())
    assert content == expected, f"Script generated incorrect checksum. Expected {expected}, got {content}"