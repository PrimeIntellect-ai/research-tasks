# test_final_state.py
import os
import time
import subprocess
import urllib.request
import signal
import pytest

def test_files_exist_and_executable():
    assert os.path.isfile("/home/user/supervisor.sh"), "/home/user/supervisor.sh does not exist"
    assert os.access("/home/user/supervisor.sh", os.X_OK), "/home/user/supervisor.sh is not executable"

    assert os.path.isfile("/home/user/deploy.sh"), "/home/user/deploy.sh does not exist"
    assert os.access("/home/user/deploy.sh", os.X_OK), "/home/user/deploy.sh is not executable"

def test_health_server_c_has_loop():
    with open("/home/user/health_server.c", "r") as f:
        content = f.read()
    assert any(keyword in content for keyword in ["while", "for", "goto"]), "health_server.c does not appear to contain a loop"

def test_supervisor_and_deploy():
    # Compile the initial server to ensure it exists before supervisor starts
    compile_proc = subprocess.run(["gcc", "/home/user/health_server.c", "-o", "/home/user/health_server"], capture_output=True)
    assert compile_proc.returncode == 0, f"Failed to compile health_server.c: {compile_proc.stderr.decode()}"

    # Start supervisor in a new process group
    supervisor_proc = subprocess.Popen(["/home/user/supervisor.sh"], preexec_fn=os.setsid, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    try:
        # Give it time to start up and write PIDs
        time.sleep(2)

        assert os.path.isfile("/home/user/supervisor.pid"), "/home/user/supervisor.pid was not created"
        assert os.path.isfile("/home/user/server.pid"), "/home/user/server.pid was not created"
        assert os.path.isfile("/home/user/server.log"), "/home/user/server.log was not created"

        with open("/home/user/server.pid", "r") as f:
            server_pid_1 = f.read().strip()

        assert server_pid_1.isdigit(), "/home/user/server.pid does not contain a valid PID"

        # Test if server handles multiple requests
        for _ in range(3):
            req = urllib.request.Request("http://localhost:9090")
            try:
                with urllib.request.urlopen(req, timeout=2) as response:
                    assert response.status == 200
                    assert response.read().decode().strip() == "OK"
            except Exception as e:
                pytest.fail(f"Failed to connect to health_server: {e}")

        with open("/home/user/server.pid", "r") as f:
            server_pid_2 = f.read().strip()

        assert server_pid_1 == server_pid_2, "Server PID changed after connections. It may have crashed after handling a request."

        # Run deploy script
        deploy_res = subprocess.run(["/home/user/deploy.sh"], capture_output=True, text=True)
        assert deploy_res.returncode == 0, f"/home/user/deploy.sh failed: {deploy_res.stderr}"

        # Wait for the supervisor to restart the server
        time.sleep(3)

        with open("/home/user/server.pid", "r") as f:
            server_pid_3 = f.read().strip()

        assert server_pid_2 != server_pid_3, "Server PID did not change after deploy.sh; server was not restarted by the supervisor."

        # Check if it still handles requests after restart
        req = urllib.request.Request("http://localhost:9090")
        try:
            with urllib.request.urlopen(req, timeout=2) as response:
                assert response.status == 200
                assert response.read().decode().strip() == "OK"
        except Exception as e:
            pytest.fail(f"Failed to connect to health_server after deployment: {e}")

    finally:
        # Cleanup
        try:
            os.killpg(os.getpgid(supervisor_proc.pid), signal.SIGKILL)
        except Exception:
            pass

        try:
            if os.path.isfile("/home/user/server.pid"):
                with open("/home/user/server.pid", "r") as f:
                    spid = int(f.read().strip())
                os.kill(spid, signal.SIGKILL)
        except Exception:
            pass