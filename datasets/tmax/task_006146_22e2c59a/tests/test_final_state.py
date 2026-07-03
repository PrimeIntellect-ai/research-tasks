# test_final_state.py
import os
import stat
import subprocess
import socket
import threading
import time
import pytest

class DummySMTPServer(threading.Thread):
    def __init__(self, host='127.0.0.1', port=8025):
        super().__init__()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        self.sock.settimeout(10)
        self.data_received = ""
        self.error = None

    def run(self):
        try:
            conn, addr = self.sock.accept()
            conn.settimeout(5)
            conn.sendall(b"220 localhost ESMTP\r\n")
            in_data = False
            while True:
                try:
                    data = conn.recv(4096).decode('utf-8', errors='ignore')
                    if not data:
                        break
                    self.data_received += data

                    lines = data.split('\n')
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        if in_data:
                            if line == ".":
                                in_data = False
                                conn.sendall(b"250 OK\r\n")
                        else:
                            upper_line = line.upper()
                            if upper_line.startswith("HELO") or upper_line.startswith("EHLO"):
                                conn.sendall(b"250 Hello\r\n")
                            elif upper_line.startswith("MAIL FROM"):
                                conn.sendall(b"250 OK\r\n")
                            elif upper_line.startswith("RCPT TO"):
                                conn.sendall(b"250 OK\r\n")
                            elif upper_line.startswith("DATA"):
                                conn.sendall(b"354 End data with <CR><LF>.<CR><LF>\r\n")
                                in_data = True
                            elif upper_line.startswith("QUIT"):
                                conn.sendall(b"221 Bye\r\n")
                                return
                except socket.timeout:
                    break
            conn.close()
        except socket.timeout:
            pass
        except Exception as e:
            self.error = e
        finally:
            self.sock.close()

def test_expect_script_exists_and_executable():
    path = "/home/user/check_link.exp"
    assert os.path.exists(path), f"Expect script {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{path} is not executable."

def test_monitor_script_exists_and_executable():
    path = "/home/user/monitor.sh"
    assert os.path.exists(path), f"Bash script {path} does not exist."
    st = os.stat(path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{path} is not executable."

def test_git_repo_and_hook_exists():
    repo_dir = "/home/user/net-logs"
    hook_path = os.path.join(repo_dir, ".git/hooks/post-commit")
    assert os.path.isdir(os.path.join(repo_dir, ".git")), f"Git repository not initialized at {repo_dir}."
    assert os.path.exists(hook_path), f"post-commit hook does not exist at {hook_path}."
    st = os.stat(hook_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"post-commit hook {hook_path} is not executable."

def test_workflow_up_and_down_states():
    force_down_path = "/home/user/force_down"
    repo_dir = "/home/user/net-logs"
    status_file = os.path.join(repo_dir, "status.txt")
    monitor_script = "/home/user/monitor.sh"

    # Ensure force_down is removed for the UP test
    if os.path.exists(force_down_path):
        os.remove(force_down_path)

    # Run monitor.sh
    result = subprocess.run([monitor_script], capture_output=True, text=True)
    assert result.returncode == 0, f"{monitor_script} failed with output: {result.stderr}"

    # Check status.txt for UP
    assert os.path.exists(status_file), f"{status_file} was not created."
    with open(status_file, "r") as f:
        status_content = f.read().strip()
    assert status_content == "UP", f"Expected 'UP' in {status_file}, got '{status_content}'"

    # Check git commit message for UP
    git_log = subprocess.run(["git", "log", "-1", "--pretty=%B"], cwd=repo_dir, capture_output=True, text=True)
    assert "Status: UP" in git_log.stdout, f"Expected commit message 'Status: UP', got '{git_log.stdout.strip()}'"

    # Start dummy SMTP server for DOWN test
    smtp_server = DummySMTPServer()
    smtp_server.start()
    time.sleep(0.5) # Give the server time to bind and listen

    try:
        # Create force_down
        with open(force_down_path, "w") as f:
            f.write("")

        # Run monitor.sh
        result = subprocess.run([monitor_script], capture_output=True, text=True)
        assert result.returncode == 0, f"{monitor_script} failed on DOWN test with output: {result.stderr}"

        # Check status.txt for DOWN
        with open(status_file, "r") as f:
            status_content = f.read().strip()
        assert status_content == "DOWN", f"Expected 'DOWN' in {status_file}, got '{status_content}'"

        # Check git commit message for DOWN
        git_log = subprocess.run(["git", "log", "-1", "--pretty=%B"], cwd=repo_dir, capture_output=True, text=True)
        assert "Status: DOWN" in git_log.stdout, f"Expected commit message 'Status: DOWN', got '{git_log.stdout.strip()}'"

    finally:
        # Cleanup
        if os.path.exists(force_down_path):
            os.remove(force_down_path)

    smtp_server.join(timeout=5)

    # Check email payload
    email_data = smtp_server.data_received
    assert "monitor@local.net" in email_data, "Sender 'monitor@local.net' not found in SMTP transaction."
    assert "net-admins@local.net" in email_data, "Recipient 'net-admins@local.net' not found in SMTP transaction."
    assert "Subject: ALERT: Link is DOWN" in email_data, "Subject 'ALERT: Link is DOWN' not found in SMTP transaction."