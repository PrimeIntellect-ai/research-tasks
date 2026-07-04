# test_final_state.py
import os
import subprocess
import random
import time
import socket
import pytest

def wait_for_port(port, timeout=10):
    start_time = time.time()
    while time.time() - start_time < timeout:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(('127.0.0.1', port)) == 0:
                return True
        time.sleep(0.2)
    return False

def test_start_services_script():
    script_path = "/home/user/pipeline/start_services.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

def test_fuzz_equivalence():
    agent_bin = "/home/user/pipeline/aggregator"
    oracle_bin = "/app/oracle_aggregator"
    script_path = "/home/user/pipeline/start_services.sh"

    assert os.path.isfile(agent_bin), f"Compiled binary {agent_bin} is missing."
    assert os.access(agent_bin, os.X_OK), f"Compiled binary {agent_bin} is not executable."

    # Start services using the student's script
    # Use preexec_fn to put them in a new process group for easier cleanup
    proc = subprocess.Popen([script_path], preexec_fn=os.setsid)

    try:
        assert wait_for_port(5000), "Graph API (port 5000) did not become healthy in time."
        assert wait_for_port(5001), "Event Stream (port 5001) did not become healthy in time."

        random.seed(42)

        for i in range(100):
            num_nodes = random.randint(1, 50)
            nodes = [str(random.randint(1, 100)) for _ in range(num_nodes)]
            input_data = "\n".join(nodes) + "\n"

            oracle_proc = subprocess.run([oracle_bin], input=input_data, text=True, capture_output=True)
            agent_proc = subprocess.run([agent_bin], input=input_data, text=True, capture_output=True)

            assert agent_proc.returncode == oracle_proc.returncode, (
                f"Agent exit code {agent_proc.returncode} does not match oracle {oracle_proc.returncode} on input:\n{input_data}"
            )

            assert agent_proc.stdout == oracle_proc.stdout, (
                f"Output mismatch on iteration {i}.\n"
                f"Input:\n{input_data}\n"
                f"Oracle Output:\n{oracle_proc.stdout}\n"
                f"Agent Output:\n{agent_proc.stdout}\n"
            )

    finally:
        # Cleanup
        try:
            os.killpg(os.getpgid(proc.pid), 9)
        except Exception:
            pass
        subprocess.run(["pkill", "-9", "-f", "graph_api.py"], capture_output=True)
        subprocess.run(["pkill", "-9", "-f", "event_tcp.py"], capture_output=True)