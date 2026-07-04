# test_final_state.py
import os
import time
import subprocess
import socket

def run_and_time(script_path):
    start = time.time()
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    duration = time.time() - start
    try:
        output = int(result.stdout.strip())
    except ValueError:
        output = None
    return duration, output

def test_fast_analyzer_speedup_and_correctness():
    fast_script = "/home/user/fast_analyzer.py"
    legacy_script = "/home/user/legacy_analyzer.py"

    assert os.path.isfile(fast_script), f"{fast_script} does not exist."

    legacy_time, legacy_ans = run_and_time(legacy_script)
    fast_time, fast_ans = run_and_time(fast_script)

    assert fast_ans is not None, "fast_analyzer.py did not output a valid integer."
    assert legacy_ans == fast_ans, f"Output mismatch: Legacy={legacy_ans}, Fast={fast_ans}"

    speedup = legacy_time / fast_time
    assert speedup >= 3.0, f"Speedup is {speedup:.2f}x, which is less than the required 3.0x."

def test_ssh_tunnel_running():
    # Check if port 9999 is listening
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('127.0.0.1', 9999))
    sock.close()

    if result != 0:
        # Fallback to checking process list for ssh tunnel
        ps_out = subprocess.run(["ps", "aux"], capture_output=True, text=True).stdout
        assert "9999:localhost:8080" in ps_out or "9999:127.0.0.1:8080" in ps_out, \
            "SSH tunnel forwarding port 9999 to localhost:8080 is not running."

def test_deploy_script_exists_and_executable():
    deploy_script = "/home/user/deploy.sh"
    assert os.path.isfile(deploy_script), f"{deploy_script} does not exist."
    assert os.access(deploy_script, os.X_OK), f"{deploy_script} is not executable."

def test_crontab_configured():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab. Is it configured?"
    cron_jobs = result.stdout
    assert "fast_analyzer.py" in cron_jobs, "fast_analyzer.py not found in crontab."
    assert "nc localhost 9999" in cron_jobs or "nc 127.0.0.1 9999" in cron_jobs, "Output is not piped to nc localhost 9999 in crontab."
    assert "* * * * *" in cron_jobs, "Cron job is not set to run every minute (* * * * *)."