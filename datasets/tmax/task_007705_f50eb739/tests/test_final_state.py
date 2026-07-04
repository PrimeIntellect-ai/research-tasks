# test_final_state.py

import os
import subprocess
import time
import tempfile
import shutil

def run_cmd(cmd, cwd=None):
    return subprocess.run(cmd, shell=True, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

def test_authorized_deployers_file():
    filepath = "/home/user/authorized_deployers.txt"
    assert os.path.isfile(filepath), f"{filepath} does not exist."
    with open(filepath, "r") as f:
        content = f.read()
    assert "alice@example.com" in content, "alice@example.com not in authorized_deployers.txt"
    assert "bob@example.com" in content, "bob@example.com not in authorized_deployers.txt"

def test_systemd_service_active():
    res = run_cmd("systemctl --user is-active deploy-daemon.service")
    assert res.stdout.strip() == "active", "deploy-daemon.service is not active."

def test_socket_exists():
    socket_path = "/home/user/deploy.sock"
    # The socket might be created by the daemon
    assert os.path.exists(socket_path), f"Unix socket {socket_path} does not exist."
    # Check if it is a socket
    import stat
    mode = os.stat(socket_path).st_mode
    assert stat.S_ISSOCK(mode), f"{socket_path} is not a socket."

def test_deployment_workflow():
    repo_path = "/home/user/deploy_repo.git"
    assert os.path.isdir(repo_path), f"Bare repo {repo_path} does not exist."

    live_site = "/home/user/live_site"
    os.makedirs(live_site, exist_ok=True)

    with tempfile.TemporaryDirectory() as tmpdir:
        # Clone the repo
        clone_res = run_cmd(f"git clone {repo_path} {tmpdir}")
        assert clone_res.returncode == 0, f"Failed to clone repo: {clone_res.stderr}"

        # 1. Authorized push
        run_cmd('git config user.email "alice@example.com"', cwd=tmpdir)
        run_cmd('git config user.name "Alice"', cwd=tmpdir)

        with open(os.path.join(tmpdir, "index.html"), "w") as f:
            f.write("<html>Deploy1</html>")

        run_cmd("git add index.html", cwd=tmpdir)
        run_cmd('git commit -m "Authorized deploy"', cwd=tmpdir)

        hash1 = run_cmd("git rev-parse HEAD", cwd=tmpdir).stdout.strip()

        push_res = run_cmd("git push origin master", cwd=tmpdir)
        assert push_res.returncode == 0, f"Failed to push authorized commit: {push_res.stderr}"

        time.sleep(2)  # Wait for daemon to process

        log_path = "/home/user/deploy.log"
        assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

        with open(log_path, "r") as f:
            log_content = f.read()

        assert f"SUCCESS: {hash1} by alice@example.com" in log_content, "Authorized deploy not logged as SUCCESS."

        deployed_file = os.path.join(live_site, "index.html")
        assert os.path.isfile(deployed_file), "Deployed file not found in live_site."
        with open(deployed_file, "r") as f:
            assert f.read().strip() == "<html>Deploy1</html>", "Deployed file content mismatch."

        # 2. Unauthorized push
        run_cmd('git config user.email "mallory@evil.com"', cwd=tmpdir)
        run_cmd('git config user.name "Mallory"', cwd=tmpdir)

        with open(os.path.join(tmpdir, "index.html"), "w") as f:
            f.write("<html>Hacked</html>")

        run_cmd("git add index.html", cwd=tmpdir)
        run_cmd('git commit -m "Unauthorized deploy"', cwd=tmpdir)

        hash2 = run_cmd("git rev-parse HEAD", cwd=tmpdir).stdout.strip()

        push_res = run_cmd("git push origin master", cwd=tmpdir)
        assert push_res.returncode == 0, f"Failed to push unauthorized commit: {push_res.stderr}"

        time.sleep(2)  # Wait for daemon to process

        with open(log_path, "r") as f:
            log_content = f.read()

        assert f"DENIED: {hash2} by mallory@evil.com" in log_content, "Unauthorized deploy not logged as DENIED."

        with open(deployed_file, "r") as f:
            assert f.read().strip() == "<html>Deploy1</html>", "Unauthorized deploy overwrote the live site."