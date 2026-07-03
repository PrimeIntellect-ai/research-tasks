# test_final_state.py

import os
import subprocess
import time
import socket

def test_deploy_script_exists_and_executable():
    deploy_script = "/home/user/deploy.sh"
    assert os.path.isfile(deploy_script), f"{deploy_script} is missing."
    assert os.access(deploy_script, os.X_OK), f"{deploy_script} is not executable."

def test_proxy_functionality_and_idempotency():
    # Start mock backends
    backend_proc = subprocess.Popen(["python3", "/home/user/run_backends.py"])
    time.sleep(1)

    try:
        # Run deploy.sh as the user
        res = subprocess.run(["su", "-", "user", "-c", "bash /home/user/deploy.sh"], capture_output=True, text=True)
        assert res.returncode == 0, f"deploy.sh failed to execute. stderr: {res.stderr}"
        time.sleep(2)

        pid_file = "/home/user/proxy.pid"
        assert os.path.isfile(pid_file), f"{pid_file} does not exist after running deploy.sh."

        with open(pid_file, "r") as f:
            pid1 = f.read().strip()

        assert pid1.isdigit(), f"PID file does not contain a valid numeric PID, got: {pid1}"

        def hit_proxy():
            for _ in range(5):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(2)
                    s.connect(("127.0.0.1", 8888))
                    data = s.recv(1024).decode()
                    s.close()
                    if data:
                        return data
                except Exception:
                    time.sleep(1)
            return ""

        resp1 = hit_proxy()
        assert "BACKEND_" in resp1, f"Proxy did not return expected backend response, got: '{resp1}'"

        # Run deploy.sh again to test idempotency
        res2 = subprocess.run(["su", "-", "user", "-c", "bash /home/user/deploy.sh"], capture_output=True, text=True)
        assert res2.returncode == 0, f"deploy.sh failed on second execution. stderr: {res2.stderr}"
        time.sleep(2)

        with open(pid_file, "r") as f:
            pid2 = f.read().strip()

        assert pid1 != pid2, "deploy.sh did not restart the process (PID in proxy.pid is the same)."

        resp2 = hit_proxy()
        assert "BACKEND_" in resp2, f"Proxy did not return expected backend response after restart, got: '{resp2}'"

    finally:
        # Cleanup backends
        backend_proc.terminate()
        backend_proc.wait()

        # Cleanup proxy
        if os.path.isfile("/home/user/proxy.pid"):
            with open("/home/user/proxy.pid", "r") as f:
                pid = f.read().strip()
            if pid.isdigit():
                subprocess.run(["kill", "-9", pid], stderr=subprocess.DEVNULL)