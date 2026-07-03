# test_final_state.py

import os
import stat
import pytest

BASE_DIR = "/home/user/microservice"
V1_DIR = os.path.join(BASE_DIR, "releases/v1")
V2_DIR = os.path.join(BASE_DIR, "releases/v2")
SHARED_DIR = os.path.join(BASE_DIR, "shared")
CURRENT_LINK = os.path.join(BASE_DIR, "current")

def test_directories_exist():
    for d in [V1_DIR, V2_DIR, SHARED_DIR]:
        assert os.path.isdir(d), f"Directory {d} does not exist."

def test_symlink_points_to_v2():
    assert os.path.islink(CURRENT_LINK), f"{CURRENT_LINK} is not a symlink."
    target = os.readlink(CURRENT_LINK)
    # Target could be absolute or relative, resolve it
    abs_target = os.path.abspath(os.path.join(BASE_DIR, target))
    assert abs_target == V2_DIR, f"Symlink {CURRENT_LINK} points to {abs_target}, expected {V2_DIR}."

def test_config_files_and_permissions():
    configs = [
        (os.path.join(V1_DIR, "config.ini"), "MODE=blue"),
        (os.path.join(V2_DIR, "config.ini"), "MODE=green")
    ]
    for path, expected_content in configs:
        assert os.path.isfile(path), f"Config file {path} does not exist."
        with open(path, "r") as f:
            content = f.read().strip()
        assert content == expected_content, f"Config file {path} content is '{content}', expected '{expected_content}'."

        mode = stat.S_IMODE(os.stat(path).st_mode)
        assert mode == 0o400, f"Permissions for {path} are {oct(mode)}, expected 0o400."

def test_worker_scripts_executable():
    for d in [V1_DIR, V2_DIR]:
        script_path = os.path.join(d, "worker.sh")
        assert os.path.isfile(script_path), f"Worker script {script_path} does not exist."
        assert os.access(script_path, os.X_OK), f"Worker script {script_path} is not executable."

def test_deploy_log():
    deploy_log = os.path.join(SHARED_DIR, "deploy.log")
    assert os.path.isfile(deploy_log), f"Deploy log {deploy_log} does not exist."
    with open(deploy_log, "r") as f:
        content = f.read().strip()
    assert content == "Deployment of v2 successful", f"Deploy log content is incorrect: '{content}'"

def test_app_log_sequence():
    app_log = os.path.join(SHARED_DIR, "app.log")
    assert os.path.isfile(app_log), f"App log {app_log} does not exist."

    with open(app_log, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    assert "Heartbeat: blue" in lines, "Missing 'Heartbeat: blue' in app.log."
    assert "Shutting down gracefully" in lines, "Missing 'Shutting down gracefully' in app.log."
    assert "Heartbeat: green" in lines, "Missing 'Heartbeat: green' in app.log."

    # Check sequence
    blue_indices = [i for i, line in enumerate(lines) if line == "Heartbeat: blue"]
    shutdown_indices = [i for i, line in enumerate(lines) if line == "Shutting down gracefully"]
    green_indices = [i for i, line in enumerate(lines) if line == "Heartbeat: green"]

    assert len(shutdown_indices) == 1, "Expected exactly one 'Shutting down gracefully' message."

    first_blue = blue_indices[0]
    shutdown = shutdown_indices[0]

    assert first_blue < shutdown, "'Heartbeat: blue' must appear before 'Shutting down gracefully'."