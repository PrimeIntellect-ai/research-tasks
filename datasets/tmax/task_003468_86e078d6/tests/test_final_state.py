# test_final_state.py

import os
import subprocess
import time
import signal
import glob

def test_supervisor_lifecycle():
    cpp_file = "/home/user/workspace/mda_supervisor.cpp"
    exe_file = "/home/user/workspace/mda_supervisor"
    log_file = "/home/user/dashboard_metrics.log"
    outbox_dir = "/home/user/mail/outbox"
    next_version_file = "/home/user/next_version.txt"

    assert os.path.exists(cpp_file), f"Source file {cpp_file} not found."

    # 1. Compile the C++ program
    compile_cmd = ["g++", "-std=c++11", cpp_file, "-o", exe_file]
    res = subprocess.run(compile_cmd, capture_output=True, text=True)
    assert res.returncode == 0, f"Compilation failed:\n{res.stderr}"

    # Clean up state from previous runs if any
    if os.path.exists(log_file):
        os.remove(log_file)
    for f in glob.glob(os.path.join(outbox_dir, "alert_*.eml")):
        os.remove(f)

    # 2. Run supervisor in the background
    proc = subprocess.Popen([exe_file])
    try:
        time.sleep(2) # Wait for initial startup

        assert os.path.exists(log_file), "Dashboard metrics log not created."
        with open(log_file, "r") as f:
            logs = f.read()

        start_count = logs.count("EVENT START")
        assert start_count >= 3, f"Expected at least 3 START events initially, found {start_count}."

        def get_children(ppid):
            try:
                out = subprocess.check_output(["pgrep", "-P", str(ppid)], text=True)
                return [int(x) for x in out.strip().split()]
            except subprocess.CalledProcessError:
                return []

        children = get_children(proc.pid)
        assert len(children) == 3, f"Expected 3 child processes running, found {len(children)}"

        # 3. Trigger a crash on Instance 1 (kill twice to trigger alert)
        child_to_kill = children[0]
        os.kill(child_to_kill, signal.SIGKILL)
        time.sleep(1)

        new_children = get_children(proc.pid)
        new_child_list = [c for c in new_children if c not in children]
        assert len(new_child_list) > 0, "Child process was not restarted after the first crash."

        child_to_kill_2 = new_child_list[0]
        os.kill(child_to_kill_2, signal.SIGKILL)
        time.sleep(1)

        with open(log_file, "r") as f:
            logs = f.read()

        crash_count = logs.count("EVENT CRASH")
        assert crash_count >= 2, f"Crash recovery not logged properly. Expected >= 2 CRASH events, found {crash_count}."

        # Check for email alert
        alerts = glob.glob(os.path.join(outbox_dir, "alert_*.eml"))
        assert len(alerts) > 0, "Alert email not generated in outbox after 2 crashes."

        with open(alerts[0], "r") as f:
            alert_content = f.read()
        assert "Crash loop detected" in alert_content, "Alert email content does not contain 'Crash loop detected'."

        # 4. Trigger rolling deployment
        with open(next_version_file, "w") as f:
            f.write("v2.0\n")

        os.kill(proc.pid, signal.SIGUSR1)
        time.sleep(3) # Wait for rolling deployment to complete

        with open(log_file, "r") as f:
            logs = f.read()

        graceful_count = logs.count("EVENT GRACEFUL_STOP")
        v2_start_count = logs.count("VERSION v2.0 EVENT START")

        assert graceful_count >= 3, f"Expected at least 3 GRACEFUL_STOP events during rolling deployment, found {graceful_count}."
        assert v2_start_count >= 3, f"Expected at least 3 START events for v2.0 during rolling deployment, found {v2_start_count}."

    finally:
        proc.kill()
        proc.wait()