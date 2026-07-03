# test_final_state.py

import os
import stat
import time
import socket
import subprocess
import tempfile
import pytest

def test_directories_and_repo():
    """Verify directories and bare git repository exist."""
    assert os.path.isdir('/home/user/repo/app.git/refs'), "Bare git repository not found at /home/user/repo/app.git"
    assert os.path.isdir('/home/user/deployments'), "/home/user/deployments directory missing"
    assert os.path.isdir('/home/user/logs'), "/home/user/logs directory missing"

def test_git_hook():
    """Verify post-receive hook is an executable Python script."""
    hook_path = '/home/user/repo/app.git/hooks/post-receive'
    assert os.path.isfile(hook_path), f"Hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), "Hook is not executable"

    with open(hook_path, 'r') as f:
        first_line = f.readline()
        assert 'python' in first_line.lower(), "Hook does not appear to be a Python script (missing python in shebang)"

def test_logrotate_conf():
    """Verify logrotate configuration for app.log."""
    conf_path = '/home/user/logrotate.conf'
    assert os.path.isfile(conf_path), f"logrotate.conf not found at {conf_path}"

    with open(conf_path, 'r') as f:
        conf = f.read()

    assert 'rotate 5' in conf, "logrotate.conf missing 'rotate 5'"
    assert 'copytruncate' in conf, "logrotate.conf missing 'copytruncate'"
    assert 'compress' in conf, "logrotate.conf missing 'compress'"
    assert 'daily' in conf, "logrotate.conf missing 'daily'"
    assert '/home/user/logs/app.log' in conf, "logrotate.conf missing target /home/user/logs/app.log"

def is_running(pid_file):
    if not os.path.exists(pid_file):
        return False
    with open(pid_file, 'r') as f:
        try:
            pid = int(f.read().strip())
        except ValueError:
            return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False

def test_background_processes():
    """Verify proxy and monitor processes are running."""
    assert is_running('/home/user/proxy.pid'), "Proxy process is not running or proxy.pid is missing/invalid"
    assert is_running('/home/user/monitor.pid'), "Monitor process is not running or monitor.pid is missing/invalid"

def test_full_workflow():
    """Test the git push, proxy forwarding, and monitor restart."""
    server_code = """#!/usr/bin/env python3
import socket
import sys

def run():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 9090))
    s.listen(5)
    print("Server started on 9090")
    sys.stdout.flush()
    while True:
        conn, addr = s.accept()
        data = conn.recv(1024)
        if data:
            conn.sendall(b"MOCK_SERVER_RESPONSE")
        conn.close()

if __name__ == '__main__':
    run()
"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a local git repo
        subprocess.run(['git', 'init'], cwd=tmpdir, check=True, capture_output=True)
        subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=tmpdir, check=True)
        subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=tmpdir, check=True)

        server_path = os.path.join(tmpdir, 'server.py')
        with open(server_path, 'w') as f:
            f.write(server_code)
        os.chmod(server_path, 0o755)

        subprocess.run(['git', 'add', 'server.py'], cwd=tmpdir, check=True)
        subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=tmpdir, check=True, capture_output=True)
        subprocess.run(['git', 'remote', 'add', 'origin', '/home/user/repo/app.git'], cwd=tmpdir, check=True)

        # Push to trigger hook
        push_res = subprocess.run(['git', 'push', 'origin', 'master'], cwd=tmpdir, capture_output=True)
        assert push_res.returncode == 0, f"Git push failed: {push_res.stderr.decode()}"

    # Wait a bit for the hook to execute and server to start
    time.sleep(2)

    # Check deployment files
    assert os.path.isfile('/home/user/deployments/app/server.py'), "server.py not checked out to /home/user/deployments/app"
    assert os.path.islink('/home/user/current_app'), "/home/user/current_app is not a symlink"
    assert os.readlink('/home/user/current_app') == '/home/user/deployments/app', "Symlink does not point to /home/user/deployments/app"

    # Test proxy forwarding
    def check_proxy():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect(('127.0.0.1', 8080))
            s.sendall(b"PING")
            data = s.recv(1024)
            s.close()
            return data == b"MOCK_SERVER_RESPONSE"
        except Exception:
            return False

    assert check_proxy(), "Proxy did not forward traffic to the server correctly"

    # Kill the server.py process
    subprocess.run(['pkill', '-f', 'server.py'])

    # Wait for monitor to restart it (monitor runs every 5 seconds)
    time.sleep(7)

    # Check proxy again to see if monitor restarted the server
    assert check_proxy(), "Monitor did not restart server.py after it was killed"

    # Check log file
    log_path = '/home/user/logs/app.log'
    assert os.path.isfile(log_path), "Log file /home/user/logs/app.log not created"
    assert os.path.getsize(log_path) > 0, "Log file /home/user/logs/app.log is empty"