# test_final_state.py

import os
import stat
import pytest

def test_operator_executable_exists():
    operator_path = "/home/user/operator"
    assert os.path.isfile(operator_path), f"File {operator_path} does not exist."
    st = os.stat(operator_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {operator_path} is not executable."

def test_sync_manifests_script_exists_and_executable():
    script_path = "/home/user/sync_manifests.sh"
    assert os.path.isfile(script_path), f"File {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"File {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()
    assert "set -e" in content, f"{script_path} must include 'set -e'."
    assert "set -o pipefail" in content, f"{script_path} must include 'set -o pipefail'."

def test_output_yaml_content():
    yaml_path = "/home/user/manifests/output.yaml"
    assert os.path.isfile(yaml_path), f"File {yaml_path} does not exist."
    with open(yaml_path, "r") as f:
        content = f.read()
    expected_path = "upstreamSocket: /home/user/run/upstream.sock"
    assert expected_path in content, f"{yaml_path} does not contain the correct upstreamSocket path."

def test_directories_exist():
    manifests_dir = "/home/user/manifests"
    run_dir = "/home/user/run"
    assert os.path.isdir(manifests_dir), f"Directory {manifests_dir} does not exist."
    assert os.path.isdir(run_dir), f"Directory {run_dir} does not exist."

def test_sync_status_log():
    log_path = "/home/user/sync_status.log"
    assert os.path.isfile(log_path), f"File {log_path} does not exist."
    with open(log_path, "r") as f:
        content = f.read().strip()
    assert content == "SUCCESS", f"{log_path} does not contain exactly 'SUCCESS'."

def test_storage_cleanup_logic():
    manifests_dir = "/home/user/manifests"

    # Check that .bak files are deleted
    assert not os.path.exists(os.path.join(manifests_dir, "dummy3.bak")), "dummy3.bak should have been deleted."
    assert not os.path.exists(os.path.join(manifests_dir, "dummy4.bak")), "dummy4.bak should have been deleted."

    # Check that other files remain
    assert os.path.isfile(os.path.join(manifests_dir, "dummy1.txt")), "dummy1.txt should still exist."
    assert os.path.isfile(os.path.join(manifests_dir, "dummy2.txt")), "dummy2.txt should still exist."