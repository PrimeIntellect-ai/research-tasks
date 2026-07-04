# test_final_state.py

import os
import subprocess
import time
import socket
import glob
import pytest

def test_services_listening():
    """Test that both the SMTP sink and Webhook Notifier are listening on their respective ports."""
    ports = {
        8025: "SMTP Sink",
        8080: "Webhook Notifier"
    }
    for port, name in ports.items():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2)
            result = s.connect_ex(('127.0.0.1', port))
            assert result == 0, f"{name} is not listening on 127.0.0.1:{port}"

def test_systemd_service_dependencies():
    """Test that the webhook-notifier.service has the correct systemd dependencies."""
    # The user might have copied or symlinked the service file.
    # Check standard user systemd paths first, fallback to the vendored path.
    possible_paths = [
        os.path.expanduser("~/.config/systemd/user/webhook-notifier.service"),
        "/app/webhook-notifier-1.0.0/webhook-notifier.service"
    ]

    content = ""
    for path in possible_paths:
        if os.path.isfile(path):
            with open(path, "r") as f:
                content = f.read()
            break

    assert content, "Could not find webhook-notifier.service in expected locations"
    assert "After=smtp-sink.service" in content, "webhook-notifier.service is missing After=smtp-sink.service"
    assert "Requires=smtp-sink.service" in content or "Wants=smtp-sink.service" in content, \
        "webhook-notifier.service is missing Requires=smtp-sink.service (or Wants=)"

def test_git_push_triggers_pipeline(tmp_path):
    """Simulate a git push and verify the end-to-end pipeline."""
    project_repo = "/home/user/project.git"
    assert os.path.isdir(project_repo), f"Bare repository {project_repo} does not exist"

    clone_dir = tmp_path / "test-clone"

    # Clone the bare repo
    clone_proc = subprocess.run(["git", "clone", project_repo, str(clone_dir)], capture_output=True, text=True)
    assert clone_proc.returncode == 0, f"Failed to clone repository: {clone_proc.stderr}"

    # Configure git
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=str(clone_dir), check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=str(clone_dir), check=True)

    # Create a commit
    test_file = clone_dir / "test.txt"
    test_file.write_text("Automated test push")

    subprocess.run(["git", "add", "test.txt"], cwd=str(clone_dir), check=True)
    subprocess.run(["git", "commit", "-m", "Test push"], cwd=str(clone_dir), check=True)

    # Push to trigger the hook
    push_proc = subprocess.run(["git", "push", "origin", "master"], cwd=str(clone_dir), capture_output=True, text=True)
    assert push_proc.returncode == 0, f"Git push failed: {push_proc.stderr}"

    # Give the services a moment to process the webhook and write files
    time.sleep(2)

    # Verify backup creation
    backup_dir = "/home/user/backups/"
    assert os.path.isdir(backup_dir), f"Backup directory {backup_dir} does not exist"
    backups = glob.glob(os.path.join(backup_dir, "*.tar.gz"))
    assert len(backups) > 0, f"No backup tarball found in {backup_dir} after push"

    # Verify email creation
    emails_dir = "/home/user/emails/"
    assert os.path.isdir(emails_dir), f"Emails directory {emails_dir} does not exist"
    emails = glob.glob(os.path.join(emails_dir, "*.eml"))
    assert len(emails) > 0, f"No .eml file found in {emails_dir} after push"

    # Verify email content
    found_subject = False
    for email_file in emails:
        with open(email_file, "r") as f:
            content = f.read()
            if "Subject: Deploy triggered" in content:
                found_subject = True
                break

    assert found_subject, "None of the saved .eml files contained the expected 'Subject: Deploy triggered'"