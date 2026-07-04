# test_final_state.py

import os
import stat
import subprocess
import tempfile
import threading
import socket
import time
import shutil

def test_bare_repo_exists():
    """Verify that /home/user/deploy.git is a bare git repository."""
    repo_path = "/home/user/deploy.git"
    assert os.path.isdir(repo_path), f"Directory {repo_path} does not exist."
    assert os.path.isdir(os.path.join(repo_path, "objects")), f"{repo_path} is not a valid git repository (no objects dir)."
    assert os.path.isfile(os.path.join(repo_path, "config")), f"{repo_path} is not a valid git repository (no config file)."

    # Check if it's bare
    result = subprocess.run(["git", "-C", repo_path, "config", "--get", "core.bare"], capture_output=True, text=True)
    assert result.stdout.strip() == "true", f"{repo_path} is not configured as a bare repository."

def test_pre_receive_hook_exists_and_executable():
    """Verify that the pre-receive hook exists and is executable."""
    hook_path = "/home/user/deploy.git/hooks/pre-receive"
    assert os.path.isfile(hook_path), f"Hook {hook_path} does not exist."
    st = os.stat(hook_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Hook {hook_path} is not executable."

def test_sync_script_functionality():
    """Verify the sync.py script exists and correctly backs up the repo."""
    sync_script = "/home/user/sync.py"
    assert os.path.isfile(sync_script), f"Script {sync_script} does not exist."

    backup_path = "/home/user/backup.git"
    # Run the sync script
    result = subprocess.run(["/usr/bin/python3", sync_script], capture_output=True, text=True)
    assert result.returncode == 0, f"sync.py failed to execute: {result.stderr}"

    assert os.path.isdir(backup_path), f"Backup directory {backup_path} was not created by sync.py."
    assert os.path.isdir(os.path.join(backup_path, "objects")), f"{backup_path} does not seem to contain the copied git objects."
    assert os.path.isfile(os.path.join(backup_path, "config")), f"{backup_path} does not seem to contain the copied git config."

def test_crontab_schedule():
    """Verify the cron job is correctly scheduled."""
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab."

    expected_command = "/usr/bin/python3 /home/user/sync.py"
    found = False
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "*/5 * * * *" in line and expected_command in line:
            found = True
            break

    assert found, f"Crontab does not contain the correct schedule for {expected_command}."

def test_git_hook_functionality():
    """Test the pre-receive hook by pushing valid and invalid commits, and verifying SMTP."""

    # Start a mock SMTP server
    smtp_data = []
    smtp_ready = threading.Event()
    smtp_stop = threading.Event()

    def mock_smtp_server():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('127.0.0.1', 2525))
        server.listen(1)
        server.settimeout(1.0)
        smtp_ready.set()

        while not smtp_stop.is_set():
            try:
                conn, addr = server.accept()
                conn.settimeout(1.0)
                conn.sendall(b"220 mock.smtp ESMTP\r\n")

                while not smtp_stop.is_set():
                    try:
                        data = conn.recv(1024)
                        if not data:
                            break
                        smtp_data.append(data)
                        if b"QUIT" in data.upper():
                            conn.sendall(b"221 Bye\r\n")
                            break
                        else:
                            conn.sendall(b"250 OK\r\n")
                    except socket.timeout:
                        continue
                conn.close()
            except socket.timeout:
                continue
        server.close()

    t = threading.Thread(target=mock_smtp_server)
    t.start()
    smtp_ready.wait(timeout=2)

    with tempfile.TemporaryDirectory() as temp_dir:
        clone_dir = os.path.join(temp_dir, "test_clone")

        # Clone the repo
        res = subprocess.run(["git", "clone", "/home/user/deploy.git", clone_dir], capture_output=True)
        assert res.returncode == 0, "Failed to clone deploy.git."

        # Configure git identity for the test clone
        subprocess.run(["git", "-C", clone_dir, "config", "user.email", "test@test.com"])
        subprocess.run(["git", "-C", clone_dir, "config", "user.name", "Test User"])

        # Test valid commit
        mounts_file = os.path.join(clone_dir, "mounts.fstab")
        with open(mounts_file, "w") as f:
            f.write("overlay /var/lib/docker/overlay2 overlay defaults 0 0\n")

        subprocess.run(["git", "-C", clone_dir, "add", "mounts.fstab"])
        subprocess.run(["git", "-C", clone_dir, "commit", "-m", "Valid mount"])

        res = subprocess.run(["git", "-C", clone_dir, "push", "origin", "master"], capture_output=True, text=True)
        assert res.returncode == 0, f"Pushing a valid mount failed: {res.stderr}"

        # Test invalid commit
        with open(mounts_file, "w") as f:
            f.write("none /etc tmpfs defaults 0 0\n")

        subprocess.run(["git", "-C", clone_dir, "add", "mounts.fstab"])
        subprocess.run(["git", "-C", clone_dir, "commit", "-m", "Invalid mount"])

        res = subprocess.run(["git", "-C", clone_dir, "push", "origin", "master"], capture_output=True, text=True)
        assert res.returncode != 0, "Pushing an invalid mount (/etc) succeeded, but it should have failed."

    # Stop SMTP server
    smtp_stop.set()
    t.join(timeout=2)

    full_email_data = b"".join(smtp_data).decode('utf-8', errors='ignore')

    assert "Subject: Violation" in full_email_data, "Email Subject 'Violation' not found in SMTP traffic."
    assert "Invalid mount" in full_email_data, "Email body 'Invalid mount' not found in SMTP traffic."
    assert "admin@local.system" in full_email_data, "Recipient admin@local.system not found in SMTP traffic."
    assert "git@local.system" in full_email_data, "Sender git@local.system not found in SMTP traffic."