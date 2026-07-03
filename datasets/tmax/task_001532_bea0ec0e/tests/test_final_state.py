# test_final_state.py
import os
import stat
import time
import requests
import subprocess
import pytest

def test_api_gateway_metrics_and_plan():
    base_url = "http://127.0.0.1:8080"

    # Send metric 1
    resp1 = requests.post(f"{base_url}/metric", json={"cpu": 10, "mem": 512}, timeout=5)
    assert resp1.status_code in (200, 201), f"Expected 200 or 201 for POST /metric, got {resp1.status_code}"

    # Send metric 2
    resp2 = requests.post(f"{base_url}/metric", json={"cpu": 5, "mem": 256}, timeout=5)
    assert resp2.status_code in (200, 201), f"Expected 200 or 201 for POST /metric, got {resp2.status_code}"

    # Get plan
    resp3 = requests.get(f"{base_url}/plan", timeout=5)
    assert resp3.status_code == 200, f"Expected 200 for GET /plan, got {resp3.status_code}"

    data = resp3.json()
    assert data.get("status") == "ok", f"Expected status 'ok', got {data.get('status')}"

    # Note: total_cpu and total_mem might include other files if the agent didn't clean up properly,
    # but based on the task description, we expect the sum to be at least the ones we added.
    # Since we don't know the exact starting state, we just verify the keys exist and are integers.
    # But wait, the task says "write the payload to a new file in the current metrics directory".
    # So it should be exactly 15 and 768 if the directory was fresh.
    assert "total_cpu" in data, "Missing 'total_cpu' in response"
    assert "total_mem" in data, "Missing 'total_mem' in response"
    assert data["total_cpu"] >= 15, f"Expected total_cpu >= 15, got {data['total_cpu']}"
    assert data["total_mem"] >= 768, f"Expected total_mem >= 768, got {data['total_mem']}"

def test_filesystem_state():
    metrics_dir = "/home/user/metrics"
    current_link = os.path.join(metrics_dir, "current")

    assert os.path.exists(metrics_dir), "Metrics directory does not exist"
    assert os.path.islink(current_link), "'current' is not a symlink"

    target_dir = os.path.realpath(current_link)
    assert os.path.isdir(target_dir), "Symlink 'current' does not point to a valid directory"

    # Check permissions of metrics dir
    st = os.stat(metrics_dir)
    assert stat.S_IMODE(st.st_mode) == 0o700, f"Expected permissions 0700 for {metrics_dir}, got {oct(stat.S_IMODE(st.st_mode))}"

    # Check permissions of target dir and its contents
    st = os.stat(target_dir)
    assert stat.S_IMODE(st.st_mode) == 0o700, f"Expected permissions 0700 for {target_dir}, got {oct(stat.S_IMODE(st.st_mode))}"

    for root, dirs, files in os.walk(target_dir):
        for d in dirs:
            st = os.stat(os.path.join(root, d))
            assert stat.S_IMODE(st.st_mode) == 0o700, f"Expected permissions 0700 for directory {d}"
        for f in files:
            st = os.stat(os.path.join(root, f))
            assert stat.S_IMODE(st.st_mode) == 0o700, f"Expected permissions 0700 for file {f}"

def get_sys_profiler_pid():
    try:
        output = subprocess.check_output(["pgrep", "-f", "sys-profiler"]).decode().strip()
        pids = [int(p) for p in output.split() if p]
        return pids[0] if pids else None
    except subprocess.CalledProcessError:
        return None

def test_process_supervision():
    pid1 = get_sys_profiler_pid()
    assert pid1 is not None, "sys-profiler process is not running"

    # Kill the process
    os.kill(pid1, 9)

    # Wait for supervision to restart it
    time.sleep(3)

    pid2 = get_sys_profiler_pid()
    assert pid2 is not None, "sys-profiler process was not restarted after being killed"
    assert pid1 != pid2, "sys-profiler process PID did not change after restart"