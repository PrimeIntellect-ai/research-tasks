# test_final_state.py
import os
import re

def test_migration_fstab_exists_and_content():
    fstab_path = "/home/user/migration_fstab.txt"
    assert os.path.isfile(fstab_path), f"File {fstab_path} does not exist."

    with open(fstab_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "service_v1 /home/user/deployments/v1 8001 0",
        "service_v2 /home/user/deployments/v2 8002 3",
        "service_v3 /home/user/deployments/v3 8003 6"
    ]

    lines = [line.strip() for line in content.splitlines() if line.strip()]
    assert lines == expected_lines, f"Contents of {fstab_path} do not match the expected configuration."

def test_deployment_directories_and_info():
    services = ["v1", "v2", "v3"]
    for i, version in enumerate(services, 1):
        dir_path = f"/home/user/deployments/{version}"
        assert os.path.isdir(dir_path), f"Directory {dir_path} does not exist."

        info_path = os.path.join(dir_path, "info.txt")
        assert os.path.isfile(info_path), f"File {info_path} does not exist."

        with open(info_path, "r") as f:
            content = f.read().strip()

        expected_content = f"service_v{i}"
        assert content == expected_content, f"Content of {info_path} should be '{expected_content}', but got '{content}'."

def test_live_service_symlink():
    symlink_path = "/home/user/live_service"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."

    target = os.readlink(symlink_path)
    expected_target = "/home/user/deployments/v3"
    assert target == expected_target, f"Symlink {symlink_path} points to {target}, expected {expected_target}."

def test_migration_events_log():
    log_path = "/home/user/migration_events.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "DEPLOYED service_v1 TO /home/user/deployments/v1 ON PORT 8001",
        "DEPLOYED service_v2 TO /home/user/deployments/v2 ON PORT 8002",
        "DEPLOYED service_v3 TO /home/user/deployments/v3 ON PORT 8003"
    ]

    lines = [line.strip() for line in content.splitlines() if line.strip()]
    assert lines == expected_lines, f"Contents of {log_path} do not match the expected deployment logs."

def test_deploy_monitor_c_exists():
    c_path = "/home/user/deploy_monitor.c"
    assert os.path.isfile(c_path), f"File {c_path} does not exist."

    with open(c_path, "r") as f:
        content = f.read()

    assert "#include" in content, f"{c_path} does not appear to contain valid C code."