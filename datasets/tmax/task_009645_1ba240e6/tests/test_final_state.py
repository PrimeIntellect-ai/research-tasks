# test_final_state.py

import os
import stat
import subprocess
import glob

def test_directories_and_files_exist():
    assert os.path.isdir("/home/user/backups"), "Directory /home/user/backups does not exist."
    assert os.path.isfile("/home/user/monitor.py"), "/home/user/monitor.py does not exist."
    assert os.path.isfile("/home/user/start_service.sh"), "/home/user/start_service.sh does not exist."

def test_wrapper_is_executable():
    st = os.stat("/home/user/start_service.sh")
    assert bool(st.st_mode & stat.S_IXUSR), "/home/user/start_service.sh is not executable."

def test_monitor_no_backup_dir_env():
    # Run monitor.py without BACKUP_DIR
    env = os.environ.copy()
    if "BACKUP_DIR" in env:
        del env["BACKUP_DIR"]

    result = subprocess.run(["python3", "/home/user/monitor.py"], env=env)
    assert result.returncode == 2, f"Expected exit code 2 when BACKUP_DIR is not set, got {result.returncode}."

def test_wrapper_no_backups():
    # Clean up any existing .bak files
    for f in glob.glob("/home/user/backups/*.bak"):
        os.remove(f)

    # Remove log files to ensure fresh state
    if os.path.exists("/home/user/monitor.err"):
        os.remove("/home/user/monitor.err")
    if os.path.exists("/home/user/monitor.log"):
        os.remove("/home/user/monitor.log")

    # Run wrapper
    result = subprocess.run(["/home/user/start_service.sh"])
    assert result.returncode == 1, f"Expected exit code 1 when no backups exist, got {result.returncode}."

    assert os.path.isfile("/home/user/monitor.err"), "/home/user/monitor.err was not created."
    with open("/home/user/monitor.err", "r") as f:
        err_content = f.read()

    assert "CRITICAL: Backup missing" in err_content, "monitor.err does not contain the expected CRITICAL message."

def test_wrapper_with_backups():
    # Create a dummy backup file
    test_bak = "/home/user/backups/test.bak"
    with open(test_bak, "w") as f:
        f.write("dummy")

    # Run wrapper
    result = subprocess.run(["/home/user/start_service.sh"])
    assert result.returncode == 0, f"Expected exit code 0 when backup exists, got {result.returncode}."

    assert os.path.isfile("/home/user/monitor.log"), "/home/user/monitor.log was not created."
    with open("/home/user/monitor.log", "r") as f:
        lines = f.readlines()

    assert len(lines) > 0, "/home/user/monitor.log is empty."
    assert "OK: Backup present" in lines[-1], "The last line of monitor.log does not contain the expected OK message."

    # Cleanup
    os.remove(test_bak)