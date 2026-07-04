# test_final_state.py

import os
import stat
import pytest

def test_tracker_executable():
    executable_path = "/home/user/workspace/tracker"
    assert os.path.isfile(executable_path), f"Executable {executable_path} is missing."
    st = os.stat(executable_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{executable_path} is not executable."

def test_snapshots_exist_and_finite():
    snap1 = "/home/user/workspace/snapshot1.txt"
    snap2 = "/home/user/workspace/snapshot2.txt"

    assert os.path.isfile(snap1), f"Snapshot file {snap1} is missing."
    assert os.path.isfile(snap2), f"Snapshot file {snap2} is missing."

    size1 = os.path.getsize(snap1)
    size2 = os.path.getsize(snap2)

    assert size1 < 100 * 1024, f"{snap1} is too large ({size1} bytes). The infinite loop might not be fixed."
    assert size2 < 100 * 1024, f"{snap2} is too large ({size2} bytes). The infinite loop might not be fixed."

    assert size1 > 0, f"{snap1} is empty."
    assert size2 > 0, f"{snap2} is empty."

def test_configuration_changes():
    settings_path = "/home/user/config_root/app2/settings.conf"
    assert os.path.isfile(settings_path), f"{settings_path} is missing."
    with open(settings_path, "r") as f:
        content = f.read()
    assert "DEBUG=true" in content, f"'DEBUG=true' was not appended to {settings_path}."

    new_config_path = "/home/user/config_root/app1/new_config.txt"
    assert os.path.isfile(new_config_path), f"{new_config_path} is missing."
    with open(new_config_path, "r") as f:
        content = f.read().strip()
    assert content == "version=2", f"{new_config_path} does not contain the correct text."

def test_diff_report():
    report_path = "/home/user/diff_report.txt"
    assert os.path.isfile(report_path), f"Diff report {report_path} is missing."

    with open(report_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "/home/user/config_root/app1/new_config.txt",
        "/home/user/config_root/app2/settings.conf"
    ]

    assert lines == expected_lines, f"Contents of {report_path} do not match the expected sorted diff. Got: {lines}"