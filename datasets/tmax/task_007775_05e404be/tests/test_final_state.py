# test_final_state.py
import os

def test_final_uptime_file_exists():
    """Check if the final output file was created."""
    assert os.path.isfile("/home/user/final_uptime.txt"), "The file /home/user/final_uptime.txt does not exist. Did you run the script and redirect its output?"

def test_final_uptime_content():
    """Check if the final output file contains the correct uptime percentage."""
    with open("/home/user/final_uptime.txt", "r") as f:
        content = f.read().strip()
    expected = "System Uptime: 99.9950%"
    assert content == expected, f"Expected the file to contain exactly '{expected}', but got '{content}'. Check your C++ precision logic and environment variables."

def test_uptime_monitor_executable_exists():
    """Check if the C++ program was recompiled."""
    executable_path = "/home/user/uptime_monitor"
    assert os.path.isfile(executable_path), f"The compiled executable {executable_path} does not exist. Did you recompile the C++ file?"
    assert os.access(executable_path, os.X_OK), f"The file {executable_path} is not executable."

def test_run_monitor_script_fixed():
    """Verify that the run_monitor.sh script was updated to point to the correct log directory."""
    script_path = "/home/user/run_monitor.sh"
    assert os.path.isfile(script_path), f"File {script_path} is missing."
    with open(script_path, "r") as f:
        content = f.read()

    assert "/home/user/container_logs/app_prod" in content, "The run_monitor.sh script does not appear to point to the correct log directory (/home/user/container_logs/app_prod)."