# test_final_state.py

import os
import re

def test_capacity_setup_script():
    """Verify that the setup script exists and is executable."""
    script_path = "/home/user/capacity_setup.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_logrotate_conf():
    """Verify the logrotate configuration file contents."""
    conf_path = "/home/user/logrotate.conf"
    assert os.path.isfile(conf_path), f"{conf_path} does not exist."

    with open(conf_path, "r") as f:
        content = f.read()

    assert "/home/user/capacity_logs/usage.log" in content, "Logrotate conf missing target log file."
    assert "weekly" in content, "Logrotate conf missing 'weekly' directive."
    assert "rotate 4" in content, "Logrotate conf missing 'rotate 4' directive."
    assert "compress" in content, "Logrotate conf missing 'compress' directive."
    assert "missingok" in content, "Logrotate conf missing 'missingok' directive."

def test_fstab_entry():
    """Verify the fstab entry file contents."""
    fstab_path = "/home/user/fstab_entry.txt"
    assert os.path.isfile(fstab_path), f"{fstab_path} does not exist."

    with open(fstab_path, "r") as f:
        content = f.read().strip()

    lines = [line for line in content.splitlines() if line.strip() and not line.strip().startswith("#")]
    assert len(lines) >= 1, f"{fstab_path} is empty or contains no valid fstab entries."

    found = False
    for line in lines:
        parts = line.split()
        if len(parts) >= 6:
            if (parts[0] == "metrics-server:/var/log/metrics" and
                parts[1] == "/home/user/capacity_logs" and
                parts[2] == "nfs" and
                parts[3] == "ro,nosuid,nodev" and
                parts[4] == "0" and
                parts[5] == "0"):
                found = True
                break

    assert found, "Fstab entry does not match the required specification."

def test_tunnel_cmd():
    """Verify the SSH tunneling command file contents."""
    cmd_path = "/home/user/tunnel_cmd.txt"
    assert os.path.isfile(cmd_path), f"{cmd_path} does not exist."

    with open(cmd_path, "r") as f:
        content = f.read().strip()

    assert "ssh" in content, "Command does not contain 'ssh'."

    # Check for flags using regex to ensure they are distinct words
    assert re.search(r'\b-f\b', content), "Command missing '-f' flag."
    assert re.search(r'\b-N\b', content), "Command missing '-N' flag."

    assert "9090:internal-api.local:80" in content, "Command missing the correct port forwarding string."
    assert "jump@gateway.corp.com" in content, "Command missing the correct bastion host."