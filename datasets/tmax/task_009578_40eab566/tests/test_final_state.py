# test_final_state.py

import os
import subprocess
import pytest

def get_accounts():
    accounts = []
    accounts_file = "/home/user/accounts.txt"
    if not os.path.exists(accounts_file):
        return accounts
    with open(accounts_file, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = line.split(":")
                if len(parts) >= 2:
                    accounts.append((parts[0], parts[1]))
    return accounts

def test_directories_and_symlinks():
    accounts = get_accounts()
    assert len(accounts) > 0, "/home/user/accounts.txt is missing or empty."

    for username, department in accounts:
        base_dir = f"/home/user/site_users/{username}"
        workspace = os.path.join(base_dir, "workspace")
        shared_data = os.path.join(base_dir, "shared_data")
        dept_link = os.path.join(base_dir, "dept_link")

        assert os.path.isdir(workspace), f"Workspace directory missing for {username}: {workspace}"
        assert os.path.isdir(shared_data), f"Shared data directory missing for {username}: {shared_data}"

        assert os.path.islink(dept_link), f"Symlink missing for {username}: {dept_link}"
        target = os.readlink(dept_link)
        expected_target = f"/home/user/departments/{department}"
        assert target == expected_target, f"Symlink for {username} points to {target}, expected {expected_target}"

def test_report_content():
    report_file = "/home/user/report.txt"
    assert os.path.isfile(report_file), f"Report file {report_file} is missing."

    accounts = get_accounts()
    expected_lines = sorted([f"{u} -> {d}" for u, d in accounts])

    with open(report_file, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, "Report file content does not match expected output."

def test_fstab_and_script_idempotency():
    fstab_file = "/home/user/custom_fstab"
    script_file = "/home/user/setup_mounts.sh"

    assert os.path.isfile(fstab_file), f"fstab file {fstab_file} is missing."
    assert os.path.isfile(script_file), f"Script {script_file} is missing."
    assert os.access(script_file, os.X_OK), f"Script {script_file} is not executable."

    accounts = get_accounts()
    expected_mounts = [
        f"/home/user/global_share /home/user/site_users/{u}/shared_data none bind 0 0" 
        for u, _ in accounts
    ]

    with open(fstab_file, "r") as f:
        fstab_content = f.read()

    # Check original lines are intact
    assert "/dev/sda1 / ext4 defaults 1 1" in fstab_content, "Original fstab lines were removed or modified."
    assert "/dev/sdb1 /home ext4 defaults 1 2" in fstab_content, "Original fstab lines were removed or modified."

    # Check current mounts
    fstab_lines = [line.strip() for line in fstab_content.splitlines() if line.strip()]
    for mount in expected_mounts:
        count = fstab_lines.count(mount)
        assert count == 1, f"Expected exactly 1 occurrence of '{mount}' in fstab, found {count}."

    # Run script again to test idempotency
    subprocess.run([script_file], check=True)

    with open(fstab_file, "r") as f:
        new_fstab_lines = [line.strip() for line in f.read().splitlines() if line.strip()]

    for mount in expected_mounts:
        count = new_fstab_lines.count(mount)
        assert count == 1, f"Script is not idempotent! Found {count} occurrences of '{mount}' after running script again."