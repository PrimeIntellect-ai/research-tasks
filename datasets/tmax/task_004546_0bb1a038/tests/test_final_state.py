# test_final_state.py

import os
import stat
import re

def test_backup_file():
    backup_path = "/home/user/backup/check_network.py.bak"
    assert os.path.isfile(backup_path), f"Backup file {backup_path} does not exist."

    st = os.stat(backup_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o400, f"Backup file permissions should be 0400, but got {oct(perms)}."

def test_alert_log():
    log_path = "/home/user/monitor/logs/alert.log"
    assert os.path.isfile(log_path), f"Alert log {log_path} does not exist. Did you run the script?"

    st = os.stat(log_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o444, f"Alert log permissions should be 0444, but got {oct(perms)}."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    pattern = r"^\[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] ALERT: Port 8080 is bound by process \"?nginx\"?$"
    assert re.match(pattern, content), (
        f"Alert log content does not match the expected format.\n"
        f"Expected pattern: {pattern}\n"
        f"Actual content: {content}"
    )

def test_script_content():
    script_path = "/home/user/monitor/check_network.py"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, 'r') as f:
        content = f.read()

    assert "subprocess" in content, "The script must use 'subprocess' to execute grep/awk."
    assert "grep" in content, "The script must use 'grep' in the subprocess call."
    assert "awk" in content, "The script must use 'awk' in the subprocess call."
    assert "/home/user/monitor/logs/alert.log" in content, "The script must use the absolute path for the alert log."