# test_final_state.py

import os

def test_net_check_cpp_exists():
    """Verify that /home/user/net_check.cpp exists."""
    path = "/home/user/net_check.cpp"
    assert os.path.isfile(path), f"File {path} does not exist."

def test_net_check_binary_exists_and_executable():
    """Verify that /home/user/net_check exists and is executable."""
    path = "/home/user/net_check"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_monitor_script_exists_and_executable():
    """Verify that /home/user/monitor.sh exists and is executable."""
    path = "/home/user/monitor.sh"
    assert os.path.isfile(path), f"File {path} does not exist."
    assert os.access(path, os.X_OK), f"File {path} is not executable."

    with open(path, "r") as f:
        content = f.read()
    assert "America/New_York" in content, f"Timezone 'America/New_York' not found in {path}."

def test_net_status_log_contents():
    """Verify that /home/user/logs/net_status.log exists and has the correct contents."""
    path = "/home/user/logs/net_status.log"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    expected_content = "CONNECT_SUCCESS\ndefault via 10.0.0.1 dev eth0 proto dhcp metric 100"

    assert content == expected_content, f"Contents of {path} do not match the expected output. Got:\n{content}"