# test_final_state.py

import os
import socket
import time
import subprocess
import pytest

def is_process_running(proc_name):
    try:
        output = subprocess.check_output(["ps", "-A", "-o", "comm="], text=True)
        return proc_name in output.splitlines()
    except subprocess.CalledProcessError:
        return False

def send_message(host, port, message, expected_reply=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5.0)
        s.connect((host, port))
        s.sendall(message.encode('utf-8'))
        reply = s.recv(1024).decode('utf-8')
        if expected_reply:
            assert expected_reply in reply, f"Expected '{expected_reply}' in reply, got '{reply}'"

def test_processes_running():
    """Verify that supervisord and haproxy are running."""
    assert is_process_running("supervisord"), "supervisord is not running"
    assert is_process_running("haproxy"), "haproxy is not running"

def test_mail_routing_and_recovery():
    """Test routing, crashing, recovery, and file outputs."""
    host = '127.0.0.1'
    port = 8080

    # Step 2: Send first message
    send_message(host, port, "ROUTE user1@test.com\nHello 1\n", "DELIVERED\n")

    # Step 3: Send second message
    send_message(host, port, "ROUTE user2@test.com\nHello 2\n", "DELIVERED\n")

    # Step 4: Send crash command
    send_message(host, port, "CRASH\n\n", "BYE\n")

    # Step 5: Wait for supervisord to restart the crashed instance
    time.sleep(2)

    # Step 6: Send third message
    send_message(host, port, "ROUTE user1@test.com\nHello 3\n", "DELIVERED\n")

    # Step 7: Verify user1@test.com.log
    user1_log = "/home/user/mail_spool/user1@test.com.log"
    assert os.path.isfile(user1_log), f"{user1_log} does not exist."
    with open(user1_log, 'r') as f:
        content1 = f.read()
    assert "Hello 1\n" in content1, "user1 log missing 'Hello 1'"
    assert "Hello 3\n" in content1, "user1 log missing 'Hello 3'"

    # Step 8: Verify user2@test.com.log
    user2_log = "/home/user/mail_spool/user2@test.com.log"
    assert os.path.isfile(user2_log), f"{user2_log} does not exist."
    with open(user2_log, 'r') as f:
        content2 = f.read()
    assert "Hello 2\n" in content2, "user2 log missing 'Hello 2'"