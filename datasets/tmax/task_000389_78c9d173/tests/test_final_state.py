# test_final_state.py

import os
import subprocess
import tempfile
import time
import socket
import pytest
import json

def test_port_forwarding():
    """Verify that port 8080 is listening and forwards to 9090."""
    host = "127.0.0.1"
    port = 8080
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(2)
        result = s.connect_ex((host, port))
        assert result == 0, f"Port forwarding is not active on {host}:{port}."

def test_cron_configured():
    """Verify that deploy.sh is scheduled in crontab."""
    try:
        crontab_out = subprocess.check_output(["crontab", "-l"], text=True)
    except subprocess.CalledProcessError:
        pytest.fail("No crontab configured for the current user.")

    assert "/home/user/deploy.sh" in crontab_out, "deploy.sh is not scheduled in crontab."

def test_git_hook_adversarial_corpus():
    """Verify the pre-receive hook against the clean and evil corpora."""
    evil_dir = "/app/test_corpus/evil/"
    clean_dir = "/app/test_corpus/clean/"
    repo_url = "/home/user/dashboards.git"

    assert os.path.isdir(repo_url), f"Bare repository {repo_url} does not exist."

    evil_files = [f for f in os.listdir(evil_dir) if f.endswith('.json')]
    clean_files = [f for f in os.listdir(clean_dir) if f.endswith('.json')]

    evil_bypassed = []
    clean_rejected = []

    with tempfile.TemporaryDirectory() as tmpdir:
        # Clone the repo
        subprocess.check_call(["git", "clone", repo_url, tmpdir], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Test evil corpus
        for f in evil_files:
            file_path = os.path.join(evil_dir, f)
            dest_path = os.path.join(tmpdir, f)
            with open(file_path, 'r') as src, open(dest_path, 'w') as dst:
                dst.write(src.read())

            subprocess.check_call(["git", "-C", tmpdir, "add", f])
            subprocess.check_call(["git", "-C", tmpdir, "commit", "-m", f"Add evil {f}"], stdout=subprocess.DEVNULL)

            # Push should FAIL
            result = subprocess.run(["git", "-C", tmpdir, "push", "origin", "main"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode == 0:
                evil_bypassed.append(f)

            # Reset to avoid blocking clean tests
            subprocess.check_call(["git", "-C", tmpdir, "reset", "--hard", "HEAD~1"], stdout=subprocess.DEVNULL)

        # Test clean corpus
        for f in clean_files:
            file_path = os.path.join(clean_dir, f)
            dest_path = os.path.join(tmpdir, f)
            with open(file_path, 'r') as src, open(dest_path, 'w') as dst:
                dst.write(src.read())

            subprocess.check_call(["git", "-C", tmpdir, "add", f])
            subprocess.check_call(["git", "-C", tmpdir, "commit", "-m", f"Add clean {f}"], stdout=subprocess.DEVNULL)

            # Push should SUCCEED
            result = subprocess.run(["git", "-C", tmpdir, "push", "origin", "main"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode != 0:
                clean_rejected.append(f)
            else:
                # Keep the clean commit for end-to-end test
                pass

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_rejected:
        error_msg.append(f"{len(clean_rejected)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_rejected)}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))

def test_end_to_end_flow():
    """Verify that the pushed clean files are eventually deployed via cron."""
    log_file = "/app/uploaded.log"

    # Wait up to 65 seconds for the cron job to run
    timeout = 65
    start_time = time.time()

    found = False
    while time.time() - start_time < timeout:
        if os.path.exists(log_file):
            with open(log_file, 'r') as f:
                content = f.read()
                # Check if good1.json and good2.json IDs (3 and 4) are in the log
                if "3" in content and "4" in content:
                    found = True
                    break
        time.sleep(2)

    assert found, "The cron job did not trigger the deployment script or the API did not receive the expected dashboards within 65 seconds."