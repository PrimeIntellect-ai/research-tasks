# test_final_state.py

import os
import json
import tarfile
import urllib.request
from pathlib import Path

def test_services_json_updated():
    config_path = Path("/home/user/services.json")
    assert config_path.is_file(), "services.json is missing"

    with open(config_path, "r") as f:
        data = json.load(f)

    assert data.get("service_a", {}).get("host") == "127.0.0.1", "service_a host not updated to 127.0.0.1"
    assert data.get("service_a", {}).get("port") == 9001, "service_a port not updated to 9001"

    assert data.get("service_b", {}).get("host") == "127.0.0.1", "service_b host not updated to 127.0.0.1"
    assert data.get("service_b", {}).get("port") == 9002, "service_b port not updated to 9002"

def test_symlinks_updated():
    symlinks = {
        "/home/user/deployments/service_a/current": "/home/user/releases/service_a_v2",
        "/home/user/deployments/service_b/current": "/home/user/releases/service_b_v2",
    }
    for link, expected_target in symlinks.items():
        link_path = Path(link)
        assert link_path.is_symlink(), f"{link} is not a symlink"
        actual_target = os.readlink(link)
        assert actual_target == expected_target, f"Symlink {link} points to {actual_target}, expected {expected_target}"

def test_backups_created_and_contain_v1_data():
    backups = {
        "/home/user/backups/service_a_backup.tar.gz": "v1 a",
        "/home/user/backups/service_b_backup.tar.gz": "v1 b",
    }
    for backup_path, expected_content in backups.items():
        assert Path(backup_path).is_file(), f"Backup file missing: {backup_path}"

        # Verify it's a valid tar.gz and contains the v1 index.html
        with tarfile.open(backup_path, "r:gz") as tar:
            # We don't know the exact path structure inside the tarball the student used, 
            # but we can look for an index.html file containing the expected string.
            found = False
            for member in tar.getmembers():
                if member.isfile() and member.name.endswith("index.html"):
                    f = tar.extractfile(member)
                    if f:
                        content = f.read().decode("utf-8")
                        if expected_content in content:
                            found = True
                            break
            assert found, f"Expected content '{expected_content}' not found in any index.html inside {backup_path}"

def test_http_servers_running_and_serving_v2():
    endpoints = {
        "http://127.0.0.1:9001/index.html": "v2 a",
        "http://127.0.0.1:9002/index.html": "v2 b",
    }
    for url, expected_content in endpoints.items():
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                content = response.read().decode("utf-8")
                assert expected_content in content, f"Expected '{expected_content}' in response from {url}, got '{content}'"
        except Exception as e:
            assert False, f"Failed to fetch {url}: {e}"

def test_pid_files_match_running_processes():
    pid_files = [
        "/home/user/run/service_a.pid",
        "/home/user/run/service_b.pid",
    ]
    for pid_file in pid_files:
        assert Path(pid_file).is_file(), f"PID file missing: {pid_file}"
        with open(pid_file, "r") as f:
            pid_str = f.read().strip()

        assert pid_str.isdigit(), f"PID file {pid_file} does not contain a valid integer PID"
        pid = int(pid_str)

        # Check if process is running
        try:
            os.kill(pid, 0)
        except OSError:
            assert False, f"Process with PID {pid} (from {pid_file}) is not running"