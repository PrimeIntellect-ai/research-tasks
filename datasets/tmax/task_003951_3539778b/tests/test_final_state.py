# test_final_state.py

import os
import ssl
import json
import time
import socket
import urllib.request
import subprocess
import pytest

def test_qemu_running_and_pid_file():
    """Verify QEMU is running, PID file exists, and PID matches."""
    pid_file = '/home/user/vm.pid'
    assert os.path.exists(pid_file), "PID file /home/user/vm.pid does not exist."

    with open(pid_file, 'r') as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), "PID file does not contain a valid integer."
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        pytest.fail(f"Process with PID {pid} from vm.pid is not running.")

    # Check if it's actually qemu
    cmdline_file = f'/proc/{pid}/cmdline'
    assert os.path.exists(cmdline_file), f"Process {pid} does not exist in /proc."
    with open(cmdline_file, 'r') as f:
        cmdline = f.read().replace('\x00', ' ')

    assert 'qemu-system-x86_64' in cmdline, f"Process {pid} is not qemu-system-x86_64. Cmdline: {cmdline}"

def test_vnc_port_listening():
    """Verify VNC server is listening on port 5905."""
    port = 5905
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('127.0.0.1', port))
        assert result == 0, f"QEMU VNC server is not listening on port {port}."

def test_https_server_running_and_certs():
    """Verify HTTPS server is running on 8443 and serving files with TLS."""
    cert_file = '/home/user/web/cert.pem'
    key_file = '/home/user/web/key.pem'
    server_script = '/home/user/web/server.py'

    assert os.path.exists(cert_file), "Certificate file cert.pem missing."
    assert os.path.exists(key_file), "Key file key.pem missing."
    assert os.path.exists(server_script), "Python server script server.py missing."

    port = 8443
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        result = s.connect_ex(('127.0.0.1', port))
        assert result == 0, f"HTTPS server is not listening on port {port}."

    # Fetch status.txt via HTTPS
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request(f"https://127.0.0.1:{port}/status.txt")
        with urllib.request.urlopen(req, context=ctx, timeout=5) as response:
            content = response.read().decode('utf-8')
            assert content == "VNC_PORT=5905\nSTATUS=RUNNING\n", "Served status.txt content is incorrect."
    except Exception as e:
        pytest.fail(f"Failed to fetch status.txt via HTTPS: {e}")

def test_monitor_c_program_and_dynamic_behavior():
    """Verify C program exists, initial state is RUNNING, then STOPPED after kill."""
    c_file = '/home/user/monitor.c'
    exe_file = '/home/user/monitor'
    status_file = '/home/user/web/status.txt'
    pid_file = '/home/user/vm.pid'

    assert os.path.exists(c_file), "monitor.c does not exist."
    assert os.path.exists(exe_file), "monitor executable does not exist."
    assert os.path.exists(status_file), "status.txt does not exist."

    with open(status_file, 'r') as f:
        content = f.read()
    assert content == "VNC_PORT=5905\nSTATUS=RUNNING\n", f"Initial status.txt content is wrong: {repr(content)}"

    # Dynamic test: kill QEMU
    with open(pid_file, 'r') as f:
        pid = int(f.read().strip())

    try:
        os.kill(pid, 9)
    except OSError:
        pass # Already dead?

    # Give it a moment to die
    time.sleep(0.5)

    # Run monitor
    subprocess.run([exe_file], check=True)

    # Check status.txt again
    with open(status_file, 'r') as f:
        new_content = f.read()

    assert new_content == "STATUS=STOPPED\n", f"Updated status.txt content is wrong after killing QEMU: {repr(new_content)}"