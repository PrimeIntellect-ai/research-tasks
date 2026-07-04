# test_final_state.py

import os
import subprocess
import pytest

def test_directories_exist():
    """Verify that all source and target directories have been created."""
    expected_dirs = [
        "/home/user/storage/raw",
        "/home/user/storage/processed",
        "/home/user/workspace/mnt/raw",
        "/home/user/workspace/mnt/processed"
    ]
    for d in expected_dirs:
        assert os.path.isdir(d), f"Directory missing: {d}"

def test_fstab_conf_contents():
    """Verify the contents of the simulated fstab.conf file."""
    fstab_path = "/home/user/workspace/fstab.conf"
    assert os.path.isfile(fstab_path), f"File missing: {fstab_path}"

    with open(fstab_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "/home/user/storage/processed /home/user/workspace/mnt/processed none bind 0 0",
        "/home/user/storage/raw /home/user/workspace/mnt/raw none bind 0 0"
    ]

    assert lines == expected_lines, f"Contents of {fstab_path} do not match expected output."

def test_env_sh_contents():
    """Verify the contents of the env.sh file."""
    env_path = "/home/user/workspace/env.sh"
    assert os.path.isfile(env_path), f"File missing: {env_path}"

    with open(env_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        'export DATA_PIPELINE_ENV="production"',
        'export WORKSPACE_ROOT="/home/user/workspace"'
    ]

    assert lines == expected_lines, f"Contents of {env_path} do not match expected output."

def test_bashrc_and_idempotency():
    """Verify that .bashrc contains exactly one instance of the source line, even after re-running."""
    bashrc_path = "/home/user/.bashrc"
    source_line = "source /home/user/workspace/env.sh"

    assert os.path.isfile(bashrc_path), f"File missing: {bashrc_path}"

    with open(bashrc_path, "r") as f:
        content = f.read()

    count = content.count(source_line)
    assert count == 1, f"Expected exactly 1 instance of '{source_line}' in {bashrc_path}, found {count}."

    # Test idempotency by re-running the provision script
    provision_script = "/home/user/provision.py"
    assert os.path.isfile(provision_script), f"Provision script missing: {provision_script}"

    result = subprocess.run(["python3", provision_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Running {provision_script} a second time failed:\n{result.stderr}"

    with open(bashrc_path, "r") as f:
        content = f.read()

    count = content.count(source_line)
    assert count == 1, f"Idempotency failed: Expected exactly 1 instance of '{source_line}' in {bashrc_path} after re-running, found {count}."