# test_final_state.py

import os
import pytest

def test_mail_env_sh():
    """Verify /home/user/mail_env.sh exists and exports the correct variables."""
    path = "/home/user/mail_env.sh"
    assert os.path.isfile(path), f"{path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    assert "MAILING_DOMAIN=system-deploy.local" in content, "MAILING_DOMAIN not exported correctly."
    assert "DEPLOY_WORKERS=3" in content, "DEPLOY_WORKERS not exported correctly."
    assert "ROLLOUT_DELAY_MS=100" in content, "ROLLOUT_DELAY_MS not exported correctly."

def test_mail_worker_sh():
    """Verify /home/user/mail_worker.sh exists and is executable."""
    path = "/home/user/mail_worker.sh"
    assert os.path.isfile(path), f"{path} does not exist."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_postfix_mock_cf():
    """Verify /home/user/postfix_mock.cf exists and has exact content."""
    path = "/home/user/postfix_mock.cf"
    assert os.path.isfile(path), f"{path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = [
        "primary_domain = system-deploy.local",
        "active_daemons = 3"
    ]
    assert lines == expected, f"Content of {path} does not match expected."

def test_worker_events_log():
    """Verify /home/user/worker_events.log exists and has exact content."""
    path = "/home/user/worker_events.log"
    assert os.path.isfile(path), f"{path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = [
        "[INIT] Worker 1 listening for system-deploy.local",
        "[INIT] Worker 2 listening for system-deploy.local",
        "[INIT] Worker 3 listening for system-deploy.local"
    ]
    assert lines == expected, f"Content of {path} does not match expected."

def test_deployd_log():
    """Verify /home/user/deployd.log exists and has exact content."""
    path = "/home/user/deployd.log"
    assert os.path.isfile(path), f"{path} does not exist."

    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = [
        "Staged rollout complete for worker 1",
        "Staged rollout complete for worker 2",
        "Staged rollout complete for worker 3"
    ]
    assert lines == expected, f"Content of {path} does not match expected."

def test_deployd_binary():
    """Verify the Rust binary was compiled and exists at the correct path."""
    path = "/home/user/deployd/target/release/deployd"
    assert os.path.isfile(path), f"Rust binary {path} does not exist. Did you compile with --release?"
    assert os.access(path, os.X_OK), f"Rust binary {path} is not executable."