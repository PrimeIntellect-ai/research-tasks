# test_final_state.py
import os
import json
import stat

def test_start_worker_script():
    script_path = "/home/user/app/start_worker.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR) or bool(st.st_mode & stat.S_IXGRP) or bool(st.st_mode & stat.S_IXOTH), \
        f"Script {script_path} is not executable."

def test_worker_pid_and_process():
    pid_file = "/home/user/app/worker.pid"
    assert os.path.isfile(pid_file), f"PID file {pid_file} is missing."

    with open(pid_file, "r") as f:
        content = f.read().strip()

    assert content.isdigit(), f"PID file {pid_file} does not contain a valid integer PID."
    pid = int(content)

    proc_dir = f"/proc/{pid}"
    assert os.path.isdir(proc_dir), f"Process with PID {pid} is not running."

def test_worker_log_exists():
    log_file = "/home/user/data/worker.log"
    assert os.path.isfile(log_file), f"Worker log {log_file} is missing. The worker might not be writing to the correct DATA_DIR."

def test_health_check_script_exists():
    script_path = "/home/user/app/health_check.py"
    assert os.path.isfile(script_path), f"Health check script {script_path} is missing."

def test_health_json_content():
    json_file = "/home/user/app/health.json"
    assert os.path.isfile(json_file), f"Health JSON file {json_file} is missing."

    with open(json_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_file} does not contain valid JSON."

    assert "status" in data, f"Key 'status' is missing from {json_file}."
    assert data["status"] == "healthy", f"Expected status 'healthy', got '{data['status']}'."

    pid_file = "/home/user/app/worker.pid"
    if os.path.isfile(pid_file):
        with open(pid_file, "r") as f:
            content = f.read().strip()
            if content.isdigit():
                expected_pid = int(content)
                assert "pid" in data, f"Key 'pid' is missing from {json_file}."
                assert data["pid"] == expected_pid, f"Expected pid {expected_pid}, got {data['pid']}."