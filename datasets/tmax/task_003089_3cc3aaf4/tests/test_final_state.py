# test_final_state.py

import os
import stat
import pytest

def test_manifests_directory_empty():
    path = "/home/user/manifests"
    assert os.path.isdir(path), f"Directory {path} should exist."
    files = os.listdir(path)
    assert len(files) == 0, f"Directory {path} should be empty, but contains {files}."

def test_processed_manifests_files_and_permissions():
    path_alpha = "/home/user/processed_manifests/cluster-alpha.yaml"
    path_beta = "/home/user/processed_manifests/cluster-beta.yaml"

    assert os.path.isfile(path_alpha), f"File {path_alpha} is missing."
    assert os.path.isfile(path_beta), f"File {path_beta} is missing."

    mode_alpha = stat.S_IMODE(os.stat(path_alpha).st_mode)
    assert mode_alpha == 0o400, f"File {path_alpha} has incorrect permissions: {oct(mode_alpha)}, expected 0o400."

    mode_beta = stat.S_IMODE(os.stat(path_beta).st_mode)
    assert mode_beta == 0o400, f"File {path_beta} has incorrect permissions: {oct(mode_beta)}, expected 0o400."

def test_apply_routes_script():
    path = "/home/user/apply_routes.sh"
    assert os.path.isfile(path), f"File {path} is missing."

    # Check if executable
    assert os.access(path, os.X_OK), f"File {path} is not executable."

    with open(path, "r") as f:
        content = f.read().strip().split('\n')

    # Filter out empty lines
    content = [line.strip() for line in content if line.strip()]

    expected_lines = [
        "ip route add 10.244.0.0/16 via 10.96.0.1",
        "ip route add 192.168.50.0/24 via 10.96.0.1"
    ]

    for expected in expected_lines:
        assert any(expected in line for line in content), f"Expected command '{expected}' not found in {path}."

def test_operator_log():
    path = "/home/user/operator.log"
    assert os.path.isfile(path), f"File {path} is missing."

    with open(path, "r") as f:
        content = f.read().strip().split('\n')

    content = [line.strip() for line in content if line.strip()]

    expected_lines = [
        "PROCESSED cluster-alpha.yaml 10.244.0.0/16",
        "PROCESSED cluster-beta.yaml 192.168.50.0/24"
    ]

    for expected in expected_lines:
        assert any(expected in line for line in content), f"Expected log entry '{expected}' not found in {path}."

def test_k8s_operator_script_exists():
    path = "/home/user/k8s-operator.sh"
    assert os.path.isfile(path), f"File {path} is missing. The script must be saved here."