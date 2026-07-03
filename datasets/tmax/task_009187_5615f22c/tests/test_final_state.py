# test_final_state.py
import os
import time
import socket
import subprocess
import signal
import pytest

def send_data(port, data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect(('127.0.0.1', port))
        s.sendall(data)
        return s.recv(1024)
    except Exception:
        return b""
    finally:
        s.close()

def test_edge_proxy_behavior():
    proxy_script = '/home/user/edge_proxy.py'
    assert os.path.exists(proxy_script), f"{proxy_script} does not exist."

    # Start the proxy
    proxy_proc = subprocess.Popen(['python3', proxy_script])
    try:
        time.sleep(1.5) # Wait for processes to start and bind ports

        # Test 1: Valid port forwarding
        res_valid = send_data(8888, b"VALID_TEST")
        assert b"SENSOR_ACK: VALID_TEST" in res_valid, "Port forwarding failed for valid data. Expected 'SENSOR_ACK: VALID_TEST' in response."

        # Test 2: Firewall rule
        res_banned = send_data(8888, b"HELLO BANNED_DEVICE 123")
        assert res_banned == b"", "Firewall failed to drop the connection for banned payload. Expected empty response."

        # Test 3: Log rotation
        for _ in range(10):
            send_data(8888, b"BANNED_DEVICE spam")
            time.sleep(0.1)

        assert os.path.exists('/home/user/proxy.log'), "/home/user/proxy.log not found. Logging may not be implemented."
        assert os.path.exists('/home/user/proxy.log.1'), "/home/user/proxy.log.1 not found. Log rotation may have failed."

        with open('/home/user/proxy.log', 'r') as f:
            log_content = f.read()
            assert "FIREWALL - Blocked connection" in log_content, "Correct log message 'FIREWALL - Blocked connection' not found in proxy.log."

        # Test 4: Process Lifecycle / Supervision
        pgrep = subprocess.run(['pgrep', '-f', 'sensor_server.py'], stdout=subprocess.PIPE)
        assert pgrep.returncode == 0, "sensor_server.py child process not found. The proxy should supervise this process."

        # Send SIGTERM to proxy
        proxy_proc.send_signal(signal.SIGTERM)
        try:
            proxy_proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proxy_proc.kill()
            pytest.fail("edge_proxy.py did not exit within 5 seconds after receiving SIGTERM.")

        # Verify sensor_server.py is dead
        time.sleep(0.5)
        pgrep_after = subprocess.run(['pgrep', '-f', 'sensor_server.py'], stdout=subprocess.PIPE)
        assert pgrep_after.returncode != 0, "sensor_server.py was not terminated by the supervisor upon SIGTERM."

    finally:
        # Cleanup just in case
        if proxy_proc.poll() is None:
            proxy_proc.kill()
            proxy_proc.wait()
        subprocess.run(['pkill', '-f', 'sensor_server.py'])