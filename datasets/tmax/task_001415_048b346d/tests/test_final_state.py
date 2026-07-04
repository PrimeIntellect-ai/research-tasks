# test_final_state.py

import os
import json
import pytest

REPORT_PATH = "/home/user/capacity_report.json"
SCRIPT_PATH = "/home/user/net_capacity.py"
PASSWD_PATH = "/home/user/mock_state/passwd"
GROUP_PATH = "/home/user/mock_state/group"
NET_TCP_PATH = "/home/user/mock_state/net_tcp"

def get_expected_state():
    # Parse group file
    gid_to_group = {}
    with open(GROUP_PATH, "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if len(parts) >= 3:
                group_name = parts[0]
                gid = parts[2]
                gid_to_group[gid] = group_name

    # Parse passwd file
    uid_to_group = {}
    with open(PASSWD_PATH, "r") as f:
        for line in f:
            parts = line.strip().split(":")
            if len(parts) >= 4:
                uid = parts[2]
                gid = parts[3]
                if gid in gid_to_group:
                    uid_to_group[uid] = gid_to_group[gid]

    # Parse net_tcp file
    group_counts = {}
    with open(NET_TCP_PATH, "r") as f:
        lines = f.readlines()
        for line in lines[1:]:  # Skip header
            parts = line.split()
            if len(parts) > 7:
                uid = parts[7]
                if uid in uid_to_group:
                    group = uid_to_group[uid]
                    group_counts[group] = group_counts.get(group, 0) + 1

    status = "CRITICAL" if any(count > 10 for count in group_counts.values()) else "OK"
    return {"status": status, "group_counts": group_counts}


def test_script_exists():
    assert os.path.isfile(SCRIPT_PATH), f"The script {SCRIPT_PATH} was not found."

def test_report_exists():
    assert os.path.isfile(REPORT_PATH), f"The output report {REPORT_PATH} was not found. Did you run your script?"

def test_report_format_and_content():
    assert os.path.isfile(REPORT_PATH), f"The output report {REPORT_PATH} was not found."

    with open(REPORT_PATH, "r") as f:
        try:
            report_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {REPORT_PATH} does not contain valid JSON.")

    expected_data = get_expected_state()

    assert "status" in report_data, "The JSON report is missing the 'status' key."
    assert "group_counts" in report_data, "The JSON report is missing the 'group_counts' key."

    assert report_data["status"] == expected_data["status"], \
        f"Expected status '{expected_data['status']}', but got '{report_data['status']}'."

    assert isinstance(report_data["group_counts"], dict), "The 'group_counts' key must be a dictionary."

    # Verify counts
    expected_counts = expected_data["group_counts"]
    actual_counts = report_data["group_counts"]

    for group, count in expected_counts.items():
        assert group in actual_counts, f"Group '{group}' is missing from 'group_counts'."
        assert actual_counts[group] == count, \
            f"Expected {count} connections for group '{group}', but got {actual_counts[group]}."

    for group in actual_counts:
        assert group in expected_counts, f"Group '{group}' should not be in 'group_counts' as it has 0 connections or is invalid."