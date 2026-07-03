# test_final_state.py

import os
import stat

def test_setup_script_exists():
    """Verify that the setup wrapper script exists."""
    script_path = "/home/user/setup_monitor.sh"
    assert os.path.isfile(script_path), f"Setup script {script_path} is missing."

def test_python_script_exists():
    """Verify that the Python monitoring script exists."""
    script_path = "/home/user/generate_fallback.py"
    assert os.path.isfile(script_path), f"Python script {script_path} is missing."

def test_monitor_log_content():
    """Verify the contents of the monitor log."""
    log_path = "/home/user/monitor.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing."

    with open(log_path, "r") as f:
        content = f.read()

    expected_alert = "[ALERT] Primary down. Generated fallback to lo."
    assert expected_alert in content, f"Expected alert message not found in {log_path}. Found: {content}"

def test_remedy_script_content_and_permissions():
    """Verify the contents and permissions of the remedy script."""
    remedy_path = "/home/user/remedy.sh"
    assert os.path.isfile(remedy_path), f"Remedy script {remedy_path} is missing."

    # Check executable permission
    st = os.stat(remedy_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Remedy script {remedy_path} is not executable."

    with open(remedy_path, "r") as f:
        content = f.read().strip()

    expected_content = "ip route replace default dev lo"
    assert content == expected_content, f"Remedy script content is incorrect. Expected: '{expected_content}', Found: '{content}'"