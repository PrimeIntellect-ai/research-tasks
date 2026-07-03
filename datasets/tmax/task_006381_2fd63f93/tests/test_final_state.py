# test_final_state.py
import os
import re
import pytest

def test_nginx_config():
    conf_path = "/home/user/nginx/nginx.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} is missing."
    with open(conf_path, "r") as f:
        content = f.read()

    expected_directive = "proxy_pass http://unix:/home/user/app/run/gunicorn.sock;"
    assert expected_directive in content, "Nginx proxy_pass directive not updated to the correct socket path."

def test_logrotate_config():
    conf_path = "/home/user/metrics_logrotate.conf"
    assert os.path.isfile(conf_path), f"File {conf_path} is missing."
    with open(conf_path, "r") as f:
        content = f.read()

    assert "/home/user/nginx/logs/access.log" in content, "Logrotate config does not target the correct log file."
    assert "daily" in content, "Logrotate config missing 'daily' directive."
    assert re.search(r"rotate\s+7", content), "Logrotate config missing 'rotate 7' directive."
    assert "compress" in content, "Logrotate config missing 'compress' directive."

def test_fstab_entry():
    fstab_path = "/home/user/capacity_fstab"
    assert os.path.isfile(fstab_path), f"File {fstab_path} is missing."
    with open(fstab_path, "r") as f:
        content = f.read().strip()

    lines = [line for line in content.splitlines() if line.strip() and not line.strip().startswith("#")]
    assert len(lines) == 1, "fstab file should contain exactly one uncommented line."

    parts = lines[0].split()
    assert len(parts) == 6, "fstab entry does not have exactly 6 fields."
    assert parts[0] == "/dev/nvme1n1", "fstab entry device is incorrect."
    assert parts[1] == "/home/user/capacity_metrics", "fstab entry mount point is incorrect."
    assert parts[2] == "xfs", "fstab entry filesystem type is incorrect."
    assert parts[3] == "defaults", "fstab entry options are incorrect."
    assert parts[4] == "0", "fstab entry dump value is incorrect."
    assert parts[5] == "2", "fstab entry pass value is incorrect."

def test_firewall_rule():
    script_path = "/home/user/firewall_rule.sh"
    assert os.path.isfile(script_path), f"File {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    with open(script_path, "r") as f:
        content = f.read()

    # Check for the required iptables components
    assert "iptables" in content, "iptables command not found."
    assert "-A INPUT" in content, "Missing append to INPUT chain."
    assert "-j DROP" in content, "Missing DROP target."
    assert "8080" in content, "Missing port 8080."
    assert "192.168.1.100" in content, "Missing source IP 192.168.1.100."
    assert "-p tcp" in content, "Missing TCP protocol specification."

    # Check for common valid orderings
    valid_patterns = [
        r"iptables\s+-A\s+INPUT\s+-s\s+192\.168\.1\.100\s+-p\s+tcp\s+--dport\s+8080\s+-j\s+DROP",
        r"iptables\s+-A\s+INPUT\s+-p\s+tcp\s+-s\s+192\.168\.1\.100\s+--dport\s+8080\s+-j\s+DROP",
        r"iptables\s+-A\s+INPUT\s+-p\s+tcp\s+--dport\s+8080\s+-s\s+192\.168\.1\.100\s+-j\s+DROP"
    ]

    match = any(re.search(pattern, content) for pattern in valid_patterns)
    assert match, "The iptables command does not match the required arguments and structure."