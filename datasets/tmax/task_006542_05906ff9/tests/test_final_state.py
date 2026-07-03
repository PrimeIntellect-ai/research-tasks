# test_final_state.py

import os
import stat
import subprocess
import time
import socket
import signal

def test_rust_project_exists():
    assert os.path.isfile("/home/user/health_checker/Cargo.toml"), "/home/user/health_checker/Cargo.toml does not exist"
    assert os.path.isfile("/home/user/health_checker/src/main.rs"), "/home/user/health_checker/src/main.rs does not exist"

def test_manager_script_exists_and_executable():
    script_path = "/home/user/manager.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist"
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable"

def test_integration_manager_script():
    # 1. Start a mock server on port 9090
    mock_server = subprocess.Popen(
        ["socat", "TCP-LISTEN:9090,fork,reuseaddr", "SYSTEM:echo -ne 'PONG\\n'"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    manager_proc = None
    try:
        # Give mock server a moment to start
        time.sleep(1)

        # 2. Run manager.sh in the background
        manager_proc = subprocess.Popen(
            ["/home/user/manager.sh"],
            cwd="/home/user",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        # Wait for compilation and first few loops
        # Compilation might take some time (up to 30-60 seconds depending on the system)
        # We'll poll for the proxy.pid file to appear
        pid_file = "/home/user/proxy.pid"
        if os.path.exists(pid_file):
            os.remove(pid_file)

        timeout = 60
        start_time = time.time()
        while time.time() - start_time < timeout:
            if os.path.exists(pid_file):
                break
            time.sleep(1)

        assert os.path.exists(pid_file), "proxy.pid was not created within the timeout (compilation might have failed or script is stuck)"

        # Wait a bit for the first health check to run
        time.sleep(3)

        # 3. Check monitoring.log for HEALTHY
        log_file = "/home/user/monitoring.log"
        assert os.path.exists(log_file), "monitoring.log was not created"
        with open(log_file, "r") as f:
            log_content = f.read()
        assert "HEALTHY" in log_content, "monitoring.log does not contain HEALTHY"

        # 4. Test port forwarding on 8080
        try:
            with socket.create_connection(("127.0.0.1", 8080), timeout=2) as s:
                s.sendall(b"PING\n")
                data = s.recv(1024)
                assert b"PONG" in data, "Did not receive PONG from forwarded port 8080"
        except Exception as e:
            assert False, f"Failed to connect to forwarded port 8080: {e}"

        # 5. Kill the mock server
        mock_server.terminate()
        mock_server.wait(timeout=5)

        # 6. Wait for manager to detect failure
        time.sleep(4)

        # 7. Check if proxy.pid process is dead
        with open(pid_file, "r") as f:
            proxy_pid_str = f.read().strip()

        assert proxy_pid_str.isdigit(), f"Invalid PID in proxy.pid: {proxy_pid_str}"
        proxy_pid = int(proxy_pid_str)

        # Check if process is running
        process_alive = False
        try:
            os.kill(proxy_pid, 0)
            process_alive = True
        except OSError:
            pass

        assert not process_alive, f"socat proxy process (PID {proxy_pid}) is still running after health check failure"

        # 8. Check if manager.sh exited
        retcode = manager_proc.poll()
        assert retcode is not None, "manager.sh did not exit after health check failure"
        assert retcode != 0, f"manager.sh exited with code {retcode}, expected non-zero (1)"

        # 9. Check monitoring.log for UNHEALTHY
        with open(log_file, "r") as f:
            log_content = f.read()
        assert "UNHEALTHY" in log_content, "monitoring.log does not contain UNHEALTHY after failure"

    finally:
        # Cleanup
        if mock_server.poll() is None:
            mock_server.kill()
        if manager_proc and manager_proc.poll() is None:
            manager_proc.kill()

        # Cleanup any stray socat processes
        subprocess.run(["pkill", "-f", "socat TCP-LISTEN:8080"], capture_output=True)