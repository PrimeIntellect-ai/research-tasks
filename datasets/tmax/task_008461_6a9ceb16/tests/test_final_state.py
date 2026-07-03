# test_final_state.py

import os
import subprocess
import time

def test_01_main_cpp_exists():
    path = "/home/user/exporter/main.cpp"
    assert os.path.isfile(path), f"C++ source file {path} does not exist."

def test_02_lifecycle_script_exists_and_executable():
    path = "/home/user/exporter/lifecycle.sh"
    assert os.path.isfile(path), f"Lifecycle script {path} does not exist."
    assert os.access(path, os.X_OK), f"Lifecycle script {path} is not executable."

def test_03_bin_exists_and_executable():
    path = "/home/user/exporter/bin"
    assert os.path.isfile(path), f"Executable {path} does not exist. Did you run './lifecycle.sh build'?"
    assert os.access(path, os.X_OK), f"Executable {path} is not executable."

def get_directory_size(path):
    total_size = 0
    for dirpath, _, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def test_04_metrics_file_content():
    metrics_path = "/home/user/metrics.prom"
    container_path = "/home/user/mock_container"

    # Wait a moment to ensure the daemon had time to write
    time.sleep(1.5)

    assert os.path.isfile(metrics_path), f"Metrics file {metrics_path} does not exist. Is the daemon running?"

    expected_size = get_directory_size(container_path)
    expected_line = f'mock_container_storage_bytes{{path="{container_path}"}} {expected_size}'

    with open(metrics_path, "r") as f:
        content = f.read().strip()

    assert content == expected_line, f"Metrics file content does not match expected.\nExpected: '{expected_line}'\nFound: '{content}'"

def test_05_pidfile_and_process():
    pidfile_path = "/home/user/exporter/pidfile"
    assert os.path.isfile(pidfile_path), f"Pidfile {pidfile_path} does not exist."

    with open(pidfile_path, "r") as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), f"Pidfile does not contain a valid PID: '{pid_str}'"
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} is not running.")

def test_06_lifecycle_stop():
    pidfile_path = "/home/user/exporter/pidfile"
    assert os.path.isfile(pidfile_path), "Pidfile missing before stop command."

    with open(pidfile_path, "r") as f:
        pid = int(f.read().strip())

    script_path = "/home/user/exporter/lifecycle.sh"
    result = subprocess.run([script_path, "stop"], capture_output=True, text=True)
    assert result.returncode == 0, f"Stop command failed with return code {result.returncode}\nStderr: {result.stderr}"

    time.sleep(1)

    # Verify process is terminated
    process_running = True
    try:
        os.kill(pid, 0)
    except OSError:
        process_running = False

    assert not process_running, f"Process with PID {pid} is still running after stop command."
    assert not os.path.isfile(pidfile_path), f"Pidfile {pidfile_path} was not deleted after stop command."