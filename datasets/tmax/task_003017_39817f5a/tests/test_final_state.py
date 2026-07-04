# test_final_state.py

import os
import stat
import json

def test_run_monitor_sh_exists_and_executable():
    """Test that the run_monitor.sh wrapper script exists and is executable."""
    path = "/home/user/migration/run_monitor.sh"
    assert os.path.isfile(path), f"Wrapper script {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Wrapper script {path} is not executable."

def test_monitor_py_exists():
    """Test that the monitor.py script exists."""
    path = "/home/user/migration/monitor.py"
    assert os.path.isfile(path), f"Python script {path} does not exist."

def test_mount_directories_created():
    """Test that the mount directories specified in fstab_mock were created."""
    assert os.path.isdir("/home/user/data_vol1"), "Directory /home/user/data_vol1 was not created."
    assert os.path.isdir("/home/user/data_vol2"), "Directory /home/user/data_vol2 was not created."

def test_status_json_exists_and_correct():
    """Test that the output JSON exists in the correct directory and has the correct content."""
    path = "/home/user/migration/logs/status.json"
    assert os.path.isfile(path), f"JSON output file {path} does not exist. Ensure the wrapper script creates the logs directory and sets LOG_DIR properly."

    with open(path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {path} does not contain valid JSON."

    expected = {
        "/home/user/data_vol1": {
            "fs_type": "ext4",
            "backup_reachable": True
        },
        "/home/user/data_vol2": {
            "fs_type": "xfs",
            "backup_reachable": False
        }
    }

    assert data == expected, f"JSON content in {path} does not match expected output.\nExpected: {expected}\nGot: {data}"