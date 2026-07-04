# test_final_state.py

import os
import subprocess
import socket
import threading
import time
import stat

def test_files_exist_and_permissions():
    """Ensure all required files exist and have correct permissions."""
    assert os.path.isfile("/home/user/lb.c"), "/home/user/lb.c does not exist."

    lb_path = "/home/user/lb"
    assert os.path.isfile(lb_path), "/home/user/lb executable does not exist."
    assert os.access(lb_path, os.X_OK), "/home/user/lb is not executable."

    health_path = "/home/user/health.sh"
    assert os.path.isfile(health_path), "/home/user/health.sh does not exist."
    assert os.access(health_path, os.X_OK), "/home/user/health.sh is not executable."

def test_crontab_installed():
    """Ensure the crontab is installed to run health.sh every minute."""
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "No crontab installed for the user."

    found = False
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "/home/user/health.sh" in line:
            parts = line.split()
            if len(parts) >= 6 and parts[:5] == ["*", "*", "*", "*", "*"]:
                found = True
                break
    assert found, "Crontab does not contain an entry to run /home/user/health.sh every minute (* * * * *)."

def kill_port_8000():
    """Helper to kill any process listening on port 8000."""
    try:
        result = subprocess.run(["lsof", "-t", "-i:8000"], capture_output=True, text=True)
        pids = result.stdout.strip().split()
        for pid in pids:
            if pid:
                subprocess.run(["kill", "-9", pid])
        time.sleep(0.5)
    except Exception:
        pass

def test_health_script_restarts_lb():
    """Ensure health.sh detects a crash, logs it, and restarts the LB."""
    kill_port_8000()

    # Ensure port 8000 is actually free
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        assert s.connect_ex(('127.0.0.1', 8000)) != 0, "Failed to kill process on port 8000 before test."

    # Run the health script
    subprocess.run(["/home/user/health.sh"], check=True)
    time.sleep(1) # Give it a moment to start the LB

    # Check if port 8000 is listening now
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        assert s.connect_ex(('127.0.0.1', 8000)) == 0, "health.sh did not start the load balancer on port 8000."

    # Check log file
    log_path = "/home/user/lb.log"
    assert os.path.isfile(log_path), "/home/user/lb.log was not created."
    with open(log_path, "r") as f:
        content = f.read()
    assert "[CRASH DETECTED] Restarting LB" in content, "health.sh did not append the correct crash detection message to lb.log."

def dummy_backend(port, response_msg, events_list):
    """A dummy backend server that accepts one connection, reads data, sends a response, and closes."""
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('127.0.0.1', port))
        server.listen(1)
        server.settimeout(5)
        conn, addr = server.accept()
        data = conn.recv(1024)
        if data:
            events_list.append((port, data.decode('utf-8')))
            conn.sendall(response_msg.encode('utf-8'))
        conn.close()
        server.close()
    except Exception as e:
        events_list.append((port, f"ERROR: {e}"))

def test_load_balancer_round_robin():
    """Ensure the load balancer correctly alternates between 8001 and 8002."""
    # Ensure LB is running
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(('127.0.0.1', 8000)) != 0:
            subprocess.run(["/home/user/health.sh"])
            time.sleep(1)

    events = []

    for i in range(3):
        # Start backends
        t1 = threading.Thread(target=dummy_backend, args=(8001, "BACKEND1", events))
        t2 = threading.Thread(target=dummy_backend, args=(8002, "BACKEND2", events))
        t1.start()
        t2.start()
        time.sleep(0.5) # Wait for backends to listen

        # Send request to LB
        msg = f"Request {i}"
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
                client.settimeout(5)
                client.connect(('127.0.0.1', 8000))
                client.sendall(msg.encode('utf-8'))
                resp = client.recv(1024)
        except Exception as e:
            assert False, f"Failed to connect and communicate with LB on port 8000: {e}"

        t1.join()
        t2.join()

    # We sent 3 requests. We should have 3 events.
    assert len(events) == 3, f"Expected 3 backend connections, got {len(events)}. Events: {events}"

    ports_hit = [e[0] for e in events]
    assert ports_hit[0] in [8001, 8002], "First request did not hit a valid backend."

    # Check round-robin
    if ports_hit[0] == 8001:
        expected = [8001, 8002, 8001]
    else:
        expected = [8002, 8001, 8002]

    assert ports_hit == expected, f"Load balancer did not strictly alternate. Expected pattern like {expected}, got {ports_hit}"

    # Verify data was transmitted correctly
    for i, (port, data) in enumerate(events):
        assert data == f"Request {i}", f"Data corrupted or not forwarded correctly. Expected 'Request {i}', got '{data}'"