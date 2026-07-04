# test_final_state.py

import os
import stat
import pytest

def test_deploy_fstab_content():
    """Verify that deploy_fstab contains the correct mount configuration."""
    fstab_path = "/home/user/deploy_fstab"
    assert os.path.exists(fstab_path), f"File {fstab_path} does not exist."
    assert os.path.isfile(fstab_path), f"Path {fstab_path} is not a file."

    with open(fstab_path, "r") as f:
        lines = [line.strip() for line in f if line.strip() and not line.strip().startswith("#")]

    assert len(lines) == 1, f"Expected exactly one active line in {fstab_path}, found {len(lines)}."

    parts = lines[0].split()
    expected_parts = [
        "nfs.internal.net:/vol/data",
        "/home/user/worker_data",
        "nfs",
        "defaults,ro",
        "0",
        "0"
    ]

    assert parts == expected_parts, (
        f"The fstab entry is incorrect.\n"
        f"Expected: {' '.join(expected_parts)}\n"
        f"Found:    {' '.join(parts)}"
    )

def test_manager_script_exists_and_executable():
    """Verify that manager.sh exists and is executable."""
    manager_path = "/home/user/manager.sh"
    assert os.path.exists(manager_path), f"File {manager_path} does not exist."
    assert os.path.isfile(manager_path), f"Path {manager_path} is not a file."

    st = os.stat(manager_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {manager_path} is not executable."

def test_alerts_txt_content():
    """Verify that alerts.txt contains exactly 3 crash alerts."""
    alerts_path = "/home/user/mail_spool/alerts.txt"
    assert os.path.exists(alerts_path), f"File {alerts_path} does not exist. Did manager.sh run?"
    assert os.path.isfile(alerts_path), f"Path {alerts_path} is not a file."

    with open(alerts_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_line = "ALERT: Worker crashed with code 42"

    assert len(lines) == 3, f"Expected exactly 3 lines in {alerts_path}, found {len(lines)}."

    for i, line in enumerate(lines):
        assert line == expected_line, f"Line {i+1} in {alerts_path} is incorrect. Expected '{expected_line}', found '{line}'."