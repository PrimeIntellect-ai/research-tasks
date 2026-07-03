# test_final_state.py
import os
import re

def test_vnc_logs_directory():
    """Verify that the /home/user/vnc_logs directory exists."""
    assert os.path.isdir('/home/user/vnc_logs'), "Directory /home/user/vnc_logs does not exist."

def test_vnc_monitor_script():
    """Verify that the /home/user/vnc_monitor.py script exists and has correct configuration."""
    script_path = '/home/user/vnc_monitor.py'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    with open(script_path, 'r') as f:
        content = f.read()

    assert 'RotatingFileHandler' in content, "RotatingFileHandler not found in the script."
    assert 'maxBytes=60' in content.replace(' ', ''), "maxBytes=60 not found in the script."
    assert 'backupCount=3' in content.replace(' ', ''), "backupCount=3 not found in the script."
    assert '%(asctime)s - VNC_STATUS - %(message)s' in content, "Required log format not found in the script."

def test_log_files_and_rotation():
    """Verify that the log files exist and rotation occurred as expected."""
    base_log = '/home/user/vnc_logs/monitor.log'
    backups = [f"{base_log}.{i}" for i in range(1, 4)]

    assert os.path.isfile(base_log), f"Base log file {base_log} does not exist."
    for backup in backups:
        assert os.path.isfile(backup), f"Backup log file {backup} does not exist. Did you run the script 5 times?"

def test_log_contents():
    """Verify that the log contents match the required format."""
    log_files = ['/home/user/vnc_logs/monitor.log'] + [f"/home/user/vnc_logs/monitor.log.{i}" for i in range(1, 4)]

    pattern = re.compile(r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} - VNC_STATUS - (SUCCESS|FAILED)$")

    for log_file in log_files:
        if os.path.isfile(log_file):
            with open(log_file, 'r') as f:
                lines = f.read().strip().split('\n')
                for line in lines:
                    if line:  # ignore empty lines
                        assert pattern.match(line), f"Log line '{line}' in {log_file} does not match the required format."