# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_success_file():
    success_path = "/home/user/success.txt"
    assert os.path.isfile(success_path), f"File {success_path} does not exist."

    with open(success_path, "r") as f:
        content = f.read()

    assert content == "/mnt/nfs_backup\n", f"Expected /mnt/nfs_backup in {success_path}, but got: {repr(content)}"

def test_logs_content():
    for stage in ["canary", "prod"]:
        log_path = f"/home/user/logs/{stage}.log"
        assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

        with open(log_path, "r") as f:
            lines = f.readlines()

        assert len(lines) >= 10, f"Log file {log_path} has fewer than 10 lines."
        for line in lines[:10]:
            assert line.strip() == "HEARTBEAT /mnt/nfs_backup", f"Unexpected log line in {log_path}: {line.strip()}"

def test_scripts_executable():
    for script in ["daemon.sh", "supervisor.sh"]:
        script_path = f"/home/user/{script}"
        assert os.path.isfile(script_path), f"Script {script_path} does not exist."

        st = os.stat(script_path)
        assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_background_processes_running():
    try:
        output = subprocess.check_output(["ps", "aux"]).decode("utf-8")
    except subprocess.CalledProcessError:
        pytest.fail("Failed to run 'ps aux' to check running processes.")

    canary_found = False
    prod_found = False

    for line in output.splitlines():
        if "supervisor.sh" in line and "canary" in line and "grep" not in line:
            canary_found = True
        if "supervisor.sh" in line and "prod" in line and "grep" not in line:
            prod_found = True

    assert canary_found, "Could not find a running background process for 'supervisor.sh canary'."
    assert prod_found, "Could not find a running background process for 'supervisor.sh prod'."