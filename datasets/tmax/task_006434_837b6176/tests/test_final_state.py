# test_final_state.py
import os
import subprocess
import tempfile

def test_task1_git_hook():
    repo_path = "/home/user/dashboards.git"
    hook_path = os.path.join(repo_path, "hooks", "pre-receive")

    assert os.path.isfile(hook_path), f"pre-receive hook not found at {hook_path}"
    assert os.access(hook_path, os.X_OK), "pre-receive hook is not executable"

    with tempfile.TemporaryDirectory() as tmpdir:
        # Configure git to avoid warnings
        subprocess.run(["git", "config", "--global", "init.defaultBranch", "master"], check=False)
        subprocess.run(["git", "config", "--global", "user.email", "test@example.com"], check=False)
        subprocess.run(["git", "config", "--global", "user.name", "Test User"], check=False)

        # Clone the bare repository
        subprocess.run(["git", "clone", repo_path, tmpdir], check=True, capture_output=True)

        # Create a bad dashboard
        bad_file = os.path.join(tmpdir, "dashboard.json")
        with open(bad_file, "w") as f:
            f.write('{"uid": null}')

        subprocess.run(["git", "add", "dashboard.json"], cwd=tmpdir, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "bad commit"], cwd=tmpdir, check=True, capture_output=True)

        # Try to push the bad dashboard
        res_bad = subprocess.run(["git", "push", "origin", "master"], cwd=tmpdir, capture_output=True, text=True)
        assert res_bad.returncode != 0, "Pushing a dashboard with null UID should fail, but it succeeded."
        assert "Observability Policy Violation: Null UID found." in res_bad.stderr, "The pre-receive hook did not print the exact required error message."

        # Fix the dashboard
        with open(bad_file, "w") as f:
            f.write('{"uid": "123"}')

        subprocess.run(["git", "add", "dashboard.json"], cwd=tmpdir, check=True, capture_output=True)
        subprocess.run(["git", "commit", "-m", "good commit"], cwd=tmpdir, check=True, capture_output=True)

        # Try to push the good dashboard
        res_good = subprocess.run(["git", "push", "origin", "master"], cwd=tmpdir, capture_output=True, text=True)
        assert res_good.returncode == 0, f"Pushing a valid dashboard should succeed, but failed with: {res_good.stderr}"

def test_task2_fstab_configuration():
    fstab_path = "/home/user/dashboard_fstab"
    assert os.path.isfile(fstab_path), f"File {fstab_path} does not exist."

    with open(fstab_path, "r") as f:
        lines = f.readlines()

    found = False
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) >= 6:
            if (parts[0] == "UUID=9a3b2c1d-8e7f-4a5b-6c7d-8e9f0a1b2c3d" and
                parts[1] == "/home/user/dashboards_backup" and
                parts[2] == "ext4" and
                parts[3] == "rw,nosuid,nodev,noexec" and
                parts[4] == "0" and
                parts[5] == "2"):
                found = True
                break

    assert found, "The required fstab entry was not found or is formatted incorrectly in /home/user/dashboard_fstab."

def test_task3_ssh_configuration():
    ssh_config_path = "/home/user/.ssh/config"
    assert os.path.isfile(ssh_config_path), f"SSH config file {ssh_config_path} does not exist."

    # Use ssh -G to parse the effective configuration for the host
    res = subprocess.run(["ssh", "-F", ssh_config_path, "-G", "obs-jumpbox"], capture_output=True, text=True)
    assert res.returncode == 0, "Failed to parse SSH configuration using 'ssh -G'."

    output = res.stdout.lower().splitlines()

    assert "hostname 192.168.10.100" in output, "SSH Hostname/IP is not configured correctly."
    assert "user o11y" in output, "SSH User is not configured correctly."
    assert "port 2222" in output, "SSH Port is not configured correctly."
    assert "localforward 8080 dashboard-api.internal:80" in output, "SSH LocalForward is not configured correctly."
    assert "pubkeyauthentication no" in output, "SSH PubkeyAuthentication must be explicitly disabled (no)."
    assert "passwordauthentication yes" in output, "SSH PasswordAuthentication must be explicitly enabled (yes)."