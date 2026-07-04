# test_final_state.py

import os
import stat
import subprocess
import time

def test_directories_exist():
    """Check if required directories were created."""
    assert os.path.isdir("/home/user/obs/logs"), "/home/user/obs/logs directory is missing."
    assert os.path.isdir("/home/user/obs/config"), "/home/user/obs/config directory is missing."

def test_acl_permissions():
    """Check if ACLs on /home/user/obs/logs are correctly set for the games group."""
    result = subprocess.run(["getfacl", "/home/user/obs/logs"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to run getfacl on /home/user/obs/logs."

    # Looking for default:group:games:r-- and group:games:r-x
    # getfacl output might have 'default:group:games:r--' or 'default:group:games:r-x' (if they gave execute by mistake, but strict check is r--)
    # The prompt says default read (r) for files, and read and execute for the directory.
    # getfacl output format:
    # group:games:r-x
    # default:group:games:r--

    lines = result.stdout.splitlines()
    has_group_r_x = any(line.startswith("group:games:r-x") or line.startswith("group:games:rwx") for line in lines)
    has_default_group_r = any(line.startswith("default:group:games:r--") or line.startswith("default:group:games:r-x") for line in lines)

    assert has_group_r_x, "The games group does not have r-x permissions on the directory itself."
    assert has_default_group_r, "The games group does not have default r-- permissions for newly created files."

def test_tune_script():
    """Check if tune.sh works interactively and creates the correct config file."""
    script_path = "/home/user/obs/tune.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    config_file = "/home/user/obs/config/test_service.env"
    if os.path.exists(config_file):
        os.remove(config_file)

    # Run the script with simulated inputs
    # The script should prompt "Service name: " and "Log level: "
    result = subprocess.run(
        [script_path],
        input="test_service\nWARN\n",
        capture_output=True,
        text=True
    )

    assert os.path.isfile(config_file), f"Config file {config_file} was not created by tune.sh."
    with open(config_file, "r") as f:
        content = f.read().strip()

    assert content == "LEVEL=WARN", f"Expected 'LEVEL=WARN' in {config_file}, got '{content}'."

def test_log_rotator_script():
    """Check if log_rotator.sh correctly rotates logs > 100 bytes."""
    script_path = "/home/user/obs/log_rotator.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    log_dir = "/home/user/obs/logs"
    test_log = os.path.join(log_dir, "test_rotate.log")
    test_log_1 = test_log + ".1"
    test_log_2 = test_log + ".2"

    # Cleanup before test
    for f in [test_log, test_log_1, test_log_2]:
        if os.path.exists(f):
            os.remove(f)

    # Create a small log file (should not be rotated)
    small_content = "a" * 50
    with open(test_log, "w") as f:
        f.write(small_content)

    subprocess.run([script_path], check=True)
    assert os.path.exists(test_log), "Small log file was deleted."
    assert os.path.getsize(test_log) == 50, "Small log file was rotated/truncated incorrectly."
    assert not os.path.exists(test_log_1), "Small log file was rotated."

    # Create a large log file
    large_content = "b" * 150
    with open(test_log, "w") as f:
        f.write(large_content)

    # First rotation
    subprocess.run([script_path], check=True)
    assert os.path.getsize(test_log) == 0, "Original log file was not truncated to 0 bytes."
    assert os.path.exists(test_log_1), ".1 log file was not created."
    with open(test_log_1, "r") as f:
        assert f.read() == large_content, "Content of .1 log file is incorrect."

    # Second rotation
    large_content_2 = "c" * 120
    with open(test_log, "w") as f:
        f.write(large_content_2)

    subprocess.run([script_path], check=True)
    assert os.path.getsize(test_log) == 0, "Original log file was not truncated."
    assert os.path.exists(test_log_2), ".2 log file was not created."
    with open(test_log_2, "r") as f:
        assert f.read() == large_content, "Content of .2 log file is incorrect (should be from old .1)."
    with open(test_log_1, "r") as f:
        assert f.read() == large_content_2, "Content of .1 log file is incorrect (should be from old .log)."

def test_systemd_user_service():
    """Check if the systemd user service and timer are configured and active."""
    service_file = "/home/user/.config/systemd/user/log-rotator.service"
    timer_file = "/home/user/.config/systemd/user/log-rotator.timer"

    assert os.path.isfile(service_file), f"Service file {service_file} is missing."
    assert os.path.isfile(timer_file), f"Timer file {timer_file} is missing."

    # Check if timer is enabled
    enabled_check = subprocess.run(
        ["systemctl", "--user", "is-enabled", "log-rotator.timer"],
        capture_output=True, text=True
    )
    assert enabled_check.stdout.strip() == "enabled", "log-rotator.timer is not enabled."

    # Check if timer is active
    active_check = subprocess.run(
        ["systemctl", "--user", "is-active", "log-rotator.timer"],
        capture_output=True, text=True
    )
    assert active_check.stdout.strip() == "active", "log-rotator.timer is not active."