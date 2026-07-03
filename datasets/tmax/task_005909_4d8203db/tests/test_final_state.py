# test_final_state.py
import os
import time
import json
import signal
import subprocess

def test_directories_exist():
    assert os.path.isdir('/home/user/requests'), "/home/user/requests directory does not exist."
    assert os.path.isdir('/home/user/mail/outbox'), "/home/user/mail/outbox directory does not exist."

def test_files_exist_and_executable():
    assert os.path.isfile('/home/user/worker'), "/home/user/worker does not exist."
    assert os.access('/home/user/worker', os.X_OK), "/home/user/worker is not executable."

    assert os.path.isfile('/home/user/supervisor.sh'), "/home/user/supervisor.sh does not exist."
    assert os.access('/home/user/supervisor.sh', os.X_OK), "/home/user/supervisor.sh is not executable."

    assert os.path.isfile('/home/user/supervisor.pid'), "/home/user/supervisor.pid does not exist."

def test_supervisor_running():
    with open('/home/user/supervisor.pid', 'r') as f:
        pid_str = f.read().strip()

    assert pid_str.isdigit(), "PID file does not contain a valid integer."
    pid = int(pid_str)

    # Check if process is running
    try:
        os.kill(pid, 0)
    except OSError:
        assert False, f"Supervisor process with PID {pid} is not running."

def test_worker_functionality_and_supervisor_restart():
    requests_dir = '/home/user/requests'
    outbox_dir = '/home/user/mail/outbox'

    # Clean up any existing files from previous runs
    for f in os.listdir(requests_dir):
        os.remove(os.path.join(requests_dir, f))
    for f in os.listdir(outbox_dir):
        os.remove(os.path.join(outbox_dir, f))

    # 1. Normal processing
    alice_json = os.path.join(requests_dir, 'alice.json')
    alice_eml = os.path.join(outbox_dir, 'alice.eml')

    with open(alice_json, 'w') as f:
        json.dump({"username": "alice", "email": "alice@test.domain"}, f)

    time.sleep(3)

    assert not os.path.exists(alice_json), "alice.json was not deleted after processing."
    assert os.path.exists(alice_eml), "alice.eml was not created."

    with open(alice_eml, 'r') as f:
        content = f.read()

    expected_content = (
        "From: admin@system.local\n"
        "To: alice@test.domain\n"
        "Subject: Welcome to the system, alice\n\n"
        "Your account has been provisioned.\n"
    )
    assert content.strip() == expected_content.strip(), f"alice.eml content is incorrect. Got:\n{content}"

    # 2. Crash scenario
    bob_json = os.path.join(requests_dir, 'bob.json')
    with open(bob_json, 'w') as f:
        json.dump({"username": "bob", "crash": True}, f)

    time.sleep(3)

    assert os.path.exists(bob_json), "bob.json was deleted, but it should have caused a crash and been left alone."

    # 3. Recovery scenario
    charlie_json = os.path.join(requests_dir, 'charlie.json')
    charlie_eml = os.path.join(outbox_dir, 'charlie.eml')

    with open(charlie_json, 'w') as f:
        json.dump({"username": "charlie", "email": "charlie@test.domain"}, f)

    time.sleep(3)

    assert os.path.exists(charlie_eml), "charlie.eml was not created. The supervisor may not have restarted the worker after the crash."
    assert not os.path.exists(charlie_json), "charlie.json was not deleted after processing."

def test_cleanup():
    # Attempt to clean up the supervisor process
    if os.path.exists('/home/user/supervisor.pid'):
        with open('/home/user/supervisor.pid', 'r') as f:
            pid_str = f.read().strip()
        if pid_str.isdigit():
            pid = int(pid_str)
            try:
                os.kill(pid, signal.SIGTERM)
                # Also kill any remaining worker processes
                subprocess.run(['pkill', '-f', 'worker'], capture_output=True)
            except OSError:
                pass