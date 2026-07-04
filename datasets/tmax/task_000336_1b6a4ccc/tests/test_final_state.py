# test_final_state.py
import os
import subprocess
import time
import pytest

def test_run_services_and_memory():
    script_path = "/home/user/run_services.sh"
    assert os.path.isfile(script_path), f"Missing script: {script_path}"

    # Ensure no lingering processes from previous runs
    subprocess.run(["pkill", "-f", "python /app/eval_server.py"], stderr=subprocess.DEVNULL)
    subprocess.run(["pkill", "-f", "python /app/load_tester.py"], stderr=subprocess.DEVNULL)
    subprocess.run(["pkill", "-f", "redis-server"], stderr=subprocess.DEVNULL)

    # Start the script
    process = subprocess.Popen(["bash", script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    peak_rss = 0
    server_pid = None
    load_tester_started = False
    load_tester_finished = False

    start_time = time.time()
    # Monitor for up to 60 seconds
    while time.time() - start_time < 60:
        # Find pid of eval_server.py
        if not server_pid:
            try:
                pid_out = subprocess.check_output(["pgrep", "-f", "eval_server.py"]).decode().strip().split()
                if pid_out:
                    server_pid = pid_out[0]
            except subprocess.CalledProcessError:
                pass

        if server_pid:
            try:
                rss_out = subprocess.check_output(["ps", "-o", "rss=", "-p", server_pid]).decode().strip()
                if rss_out:
                    rss = int(rss_out)
                    if rss > peak_rss:
                        peak_rss = rss
            except subprocess.CalledProcessError:
                # Process might have exited
                pass

        # Check load tester status
        try:
            lt_pid_out = subprocess.check_output(["pgrep", "-f", "load_tester.py"]).decode().strip().split()
            if lt_pid_out:
                load_tester_started = True
        except subprocess.CalledProcessError:
            if load_tester_started:
                # It was running but now is not
                load_tester_finished = True
                break

        time.sleep(0.1)

    # Clean up
    process.terminate()
    process.wait()
    subprocess.run(["pkill", "-f", "python /app/eval_server.py"], stderr=subprocess.DEVNULL)
    subprocess.run(["pkill", "-f", "python /app/load_tester.py"], stderr=subprocess.DEVNULL)
    subprocess.run(["pkill", "-f", "redis-server"], stderr=subprocess.DEVNULL)

    assert load_tester_started, "load_tester.py was never started by the script"
    assert load_tester_finished, "load_tester.py did not finish within the timeout"

    assert peak_rss > 0, "Could not measure memory of eval_server.py"
    assert peak_rss <= 50000, f"Peak RSS memory of eval_server.py was {peak_rss} KB, expected <= 50000 KB"