# test_final_state.py

import os
import pytest

def test_script_exists_and_executable():
    script_path = "/home/user/generate_configs.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_generated_files_content():
    requests_path = "/home/user/requests.txt"
    assert os.path.isfile(requests_path), f"Input file {requests_path} is missing."

    expected_errors = []
    expected_fstab = []
    expected_iptables = []

    with open(requests_path, "r") as f:
        for line in f:
            line_stripped = line.strip('\n')
            if not line_stripped:
                continue

            parts = line_stripped.split(',')
            if len(parts) == 3:
                username, port, path = parts
                expected_fstab.append(f"/data/common_share {path} none bind,ro 0 0")
                expected_iptables.append(f"iptables -t nat -A PREROUTING -p tcp --dport {port} -j DNAT --to-destination 10.0.0.5:22")
            else:
                expected_errors.append(line_stripped)

    # Check error.log
    error_log_path = "/home/user/error.log"
    if expected_errors:
        assert os.path.isfile(error_log_path), f"Expected {error_log_path} to be created."
        with open(error_log_path, "r") as f:
            actual_errors = [line.strip('\n') for line in f if line.strip('\n')]
        assert actual_errors == expected_errors, f"Content of {error_log_path} is incorrect."
    else:
        if os.path.exists(error_log_path):
            assert os.path.getsize(error_log_path) == 0, f"{error_log_path} should be empty."

    # Check fstab_generated
    fstab_path = "/home/user/fstab_generated"
    if expected_fstab:
        assert os.path.isfile(fstab_path), f"Expected {fstab_path} to be created."
        with open(fstab_path, "r") as f:
            actual_fstab = [line.strip('\n') for line in f if line.strip('\n')]
        assert actual_fstab == expected_fstab, f"Content of {fstab_path} is incorrect."

    # Check port_forwards.rules
    iptables_path = "/home/user/port_forwards.rules"
    if expected_iptables:
        assert os.path.isfile(iptables_path), f"Expected {iptables_path} to be created."
        with open(iptables_path, "r") as f:
            actual_iptables = [line.strip('\n') for line in f if line.strip('\n')]
        assert actual_iptables == expected_iptables, f"Content of {iptables_path} is incorrect."