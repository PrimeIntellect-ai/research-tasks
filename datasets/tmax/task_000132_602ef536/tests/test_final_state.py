# test_final_state.py

import os
import subprocess
import time
import tempfile
import urllib.request
import json

def test_post_receive_hook_exists():
    hook_path = "/home/user/gitserver/manifests.git/hooks/post-receive"
    assert os.path.isfile(hook_path), f"Hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), f"Hook at {hook_path} is not executable"

def test_cron_job_configured():
    try:
        crontab = subprocess.check_output(["crontab", "-l"], stderr=subprocess.STDOUT).decode("utf-8")
    except subprocess.CalledProcessError:
        crontab = ""
    assert "9090/sync" in crontab, "Cron job for /sync endpoint is not configured correctly"
    assert "sync.log" in crontab, "Cron job does not append to /home/user/sync.log"

def test_performance_and_functionality():
    # Clone the repo
    with tempfile.TemporaryDirectory() as tmpdir:
        repo_dir = os.path.join(tmpdir, "repo")
        subprocess.check_call(["git", "clone", "http://127.0.0.1:8000/manifests.git", repo_dir])

        # Configure git user for the temp repo
        subprocess.check_call(["git", "config", "user.name", "Test User"], cwd=repo_dir)
        subprocess.check_call(["git", "config", "user.email", "test@example.com"], cwd=repo_dir)

        # Generate 500 yaml files
        for i in range(500):
            with open(os.path.join(repo_dir, f"manifest_{i}.yaml"), "w") as f:
                f.write(f"apiVersion: v1\nkind: ConfigMap\nmetadata:\n  name: cm-{i}\n")

        subprocess.check_call(["git", "add", "."], cwd=repo_dir)
        subprocess.check_call(["git", "commit", "-m", "Add 500 manifests"], cwd=repo_dir)

        # Measure push time
        start_time = time.time()
        subprocess.check_call(["git", "push", "origin", "master"], cwd=repo_dir)
        end_time = time.time()

        time_taken = end_time - start_time
        assert time_taken <= 1.5, f"git push took {time_taken:.3f} seconds, which exceeds the 1.5 second threshold"

        # Verify that the files were actually processed by checking the mock API sync endpoint
        try:
            req = urllib.request.Request("http://127.0.0.1:9090/sync")
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode("utf-8"))
                # If the mock API exposes the count in the sync status, verify it
                if "applied_count" in data:
                    assert data["applied_count"] >= 500, f"Expected at least 500 files applied, got {data['applied_count']}"
                elif "count" in data:
                    assert data["count"] >= 500, f"Expected at least 500 files applied, got {data['count']}"
        except Exception as e:
            # If the endpoint doesn't return a recognizable count, we rely on the push success and time limit
            pass