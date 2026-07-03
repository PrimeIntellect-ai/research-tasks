# test_final_state.py

import os
import stat
import subprocess
import random
import string
import pytest

def test_setup_restore_script_exists():
    script_path = "/home/user/setup_restore.sh"
    assert os.path.exists(script_path), f"Missing script: {script_path}"
    assert os.path.isfile(script_path), f"Not a file: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_setup_restore_state():
    # Execute the script to ensure it's idempotent and sets up the state correctly
    script_path = "/home/user/setup_restore.sh"
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with error: {result.stderr}"

    releases_dir = "/home/user/backup_staging/releases"
    v1_dir = "/home/user/backup_staging/releases/v1"
    v2_dir = "/home/user/backup_staging/releases/v2"
    current_link = "/home/user/backup_staging/current"

    assert os.path.isdir(releases_dir), f"Missing directory: {releases_dir}"
    assert os.path.isdir(v1_dir), f"Missing directory: {v1_dir}"
    assert os.path.isdir(v2_dir), f"Missing directory: {v2_dir}"

    assert stat.S_IMODE(os.stat(releases_dir).st_mode) == 0o755, f"Incorrect permissions on {releases_dir}"
    assert stat.S_IMODE(os.stat(v1_dir).st_mode) == 0o700, f"Incorrect permissions on {v1_dir}"
    assert stat.S_IMODE(os.stat(v2_dir).st_mode) == 0o700, f"Incorrect permissions on {v2_dir}"

    assert os.path.islink(current_link), f"Not a symlink: {current_link}"
    target = os.readlink(current_link)
    assert target == "/home/user/backup_staging/releases/v1", f"Symlink points to wrong target: {target}"

def test_path_validator_fuzz_equivalence():
    agent_bin = "/home/user/path_validator"
    oracle_bin = "/app/oracle_validator"

    assert os.path.exists(agent_bin), f"Missing agent executable: {agent_bin}"
    assert os.access(agent_bin, os.X_OK), f"Agent executable is not executable: {agent_bin}"
    assert os.path.exists(oracle_bin), f"Missing oracle executable: {oracle_bin}"

    random.seed(42)
    charset = string.ascii_letters + string.digits + "/._-"

    inputs = []
    for _ in range(150):
        length = random.randint(5, 60)
        inputs.append("".join(random.choice(charset) for _ in range(length)))

    # Add specific inputs to trigger edge cases
    inputs.append("/restricted/foo/bar")
    inputs.append("/restricted")
    inputs.append("foo/bar/KRAKEN99/baz")
    inputs.append("/restricted/KRAKEN99")
    inputs.append("KRAKEN99")
    inputs.append("/restricted/../KRAKEN99")
    inputs.append("/foo/../restricted")

    for _ in range(43):
        length = random.randint(5, 60)
        inputs.append("".join(random.choice(charset) for _ in range(length)))

    for i, inp in enumerate(inputs):
        oracle_res = subprocess.run([oracle_bin, inp], capture_output=True, text=True)
        agent_res = subprocess.run([agent_bin, inp], capture_output=True, text=True)

        assert oracle_res.returncode == agent_res.returncode, f"Return code mismatch on input '{inp}'"
        assert agent_res.stdout == oracle_res.stdout, f"Output mismatch on input '{inp}'. Expected '{oracle_res.stdout}', got '{agent_res.stdout}'"