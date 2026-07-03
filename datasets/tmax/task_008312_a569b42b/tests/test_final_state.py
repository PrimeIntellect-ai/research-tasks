# test_final_state.py

import os
import subprocess
import pytest

ACCOUNTS = [
    ("dev_alpha", 12),
    ("dev_beta", 25),
    ("ops_gamma", 40),
]

WORKSPACES_DIR = "/home/user/workspaces"
PROVISIONER_DIR = "/home/user/account_provisioner"

def test_rust_project_exists():
    assert os.path.exists(PROVISIONER_DIR), f"Rust project directory {PROVISIONER_DIR} does not exist"
    cargo_toml = os.path.join(PROVISIONER_DIR, "Cargo.toml")
    assert os.path.exists(cargo_toml), f"Cargo.toml not found in {PROVISIONER_DIR}"

    # Check if it builds
    result = subprocess.run(
        ["cargo", "build"],
        cwd=PROVISIONER_DIR,
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Rust project failed to build:\n{result.stderr}"

def test_workspace_directories_and_files():
    for username, _ in ACCOUNTS:
        user_dir = os.path.join(WORKSPACES_DIR, username)
        logs_dir = os.path.join(user_dir, "logs")
        data_dir = os.path.join(user_dir, "data")
        latest_log = os.path.join(logs_dir, "latest.log")
        active_log = os.path.join(user_dir, "active_log")

        assert os.path.isdir(logs_dir), f"Logs directory missing for {username}: {logs_dir}"
        assert os.path.isdir(data_dir), f"Data directory missing for {username}: {data_dir}"

        assert os.path.isfile(latest_log), f"latest.log missing for {username}: {latest_log}"

        assert os.path.islink(active_log), f"active_log is not a symlink for {username}: {active_log}"
        target = os.readlink(active_log)
        assert target == "logs/latest.log", f"active_log symlink target incorrect for {username}. Expected 'logs/latest.log', got '{target}'"

def test_setup_tunnels_script():
    script_path = os.path.join(WORKSPACES_DIR, "setup_tunnels.sh")
    assert os.path.isfile(script_path), f"Script missing: {script_path}"
    assert os.access(script_path, os.X_OK), f"Script is not executable: {script_path}"

def test_socat_processes_running():
    # Check if socat processes are running for the expected ports
    try:
        output = subprocess.check_output(["pgrep", "-f", "socat TCP-LISTEN"], text=True)
    except subprocess.CalledProcessError:
        output = ""

    running_pids = output.strip().split()

    for _, port_offset in ACCOUNTS:
        port = 8000 + port_offset
        # Check if any running socat process contains the port
        try:
            cmd_output = subprocess.check_output(["pgrep", "-f", f"socat TCP-LISTEN:{port}"], text=True)
            pids = cmd_output.strip().split()
            assert len(pids) == 1, f"Expected exactly 1 socat process for port {port}, found {len(pids)}"
        except subprocess.CalledProcessError:
            pytest.fail(f"No socat process running for port {port}")