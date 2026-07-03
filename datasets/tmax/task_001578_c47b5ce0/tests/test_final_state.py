# test_final_state.py
import os
import json
import re

def test_monitor_log():
    log_path = '/home/user/app_logs/monitor.log'
    assert os.path.exists(log_path), "monitor.log does not exist"

    with open(log_path, 'r') as f:
        lines = f.readlines()
        assert len(lines) >= 1, "Log file is empty"
        last_line = lines[-1].strip()
        try:
            data = json.loads(last_line)
        except json.JSONDecodeError:
            assert False, "Last line of monitor.log is not valid JSON"

        assert data.get("event") == "service_check", "event key missing or incorrect in monitor.log"
        assert data.get("status") == "FAILURE_DETECTED", "status key missing or incorrect in monitor.log"

def test_logrotate_config():
    config_path = '/home/user/monitor_logrotate.conf'
    assert os.path.exists(config_path), "monitor_logrotate.conf does not exist"

    with open(config_path, 'r') as f:
        content = f.read()

    assert re.search(r'\bsize\s+10k\b', content), "Missing or incorrect 'size 10k' directive in logrotate config"
    assert re.search(r'\brotate\s+4\b', content), "Missing or incorrect 'rotate 4' directive in logrotate config"
    assert re.search(r'\bcompress\b', content), "Missing 'compress' directive in logrotate config"
    assert re.search(r'\bcreate\s+0644\b', content), "Missing or incorrect 'create 0644' directive in logrotate config"
    assert re.search(r'\bmissingok\b', content), "Missing 'missingok' directive in logrotate config"
    assert re.search(r'\bnotifempty\b', content), "Missing 'notifempty' directive in logrotate config"

def test_backup_fstab():
    fstab_path = '/home/user/backup.fstab'
    assert os.path.exists(fstab_path), "backup.fstab does not exist"

    with open(fstab_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip() and not line.strip().startswith('#')]

    assert len(lines) == 1, "backup.fstab must contain exactly ONE active line"

    parts = re.split(r'\s+', lines[0])
    assert len(parts) >= 6, "fstab line does not have enough fields"

    assert parts[0] == "10.50.0.5:/export/backups", f"Incorrect remote source: {parts[0]}"
    assert parts[1] == "/home/user/remote_backups", f"Incorrect mount point: {parts[1]}"
    assert parts[2] == "nfs", f"Incorrect filesystem type: {parts[2]}"
    assert parts[3] == "ro,user,noauto,hard", f"Incorrect options: {parts[3]}"
    assert parts[4] == "0", f"Incorrect dump value: {parts[4]}"
    assert parts[5] == "0", f"Incorrect pass value: {parts[5]}"

def test_port_forward_sh():
    fw_path = '/home/user/port_forward.sh'
    assert os.path.exists(fw_path), "port_forward.sh does not exist"

    with open(fw_path, 'r') as f:
        content = f.read()

    # Check for required parts of the iptables command
    assert re.search(r'iptables\s+-t\s+nat\s+-[AI]\s+PREROUTING\s+-i\s+eth1\s+-p\s+tcp\s+--dport\s+80\s+-j\s+DNAT\s+--to-destination\s+192\.168\.1\.100:8080', content), "port_forward.sh does not contain the exact required iptables command"