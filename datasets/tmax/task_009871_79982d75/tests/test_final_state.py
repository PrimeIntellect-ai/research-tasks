# test_final_state.py
import os
import subprocess
import time
import re

def test_crontab_configured():
    """Verify that the watchdog is scheduled in the user's crontab to run every minute."""
    result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab. Is it configured?"
    cron_jobs = result.stdout.strip().split('\n')

    found = False
    for job in cron_jobs:
        if job.startswith('#'):
            continue
        if '/usr/bin/python3 /home/user/watchdog.py' in job:
            parts = job.split()
            # Check if it runs every minute: * * * * *
            if parts[:5] == ['*', '*', '*', '*', '*']:
                found = True
                break

    assert found, "Crontab does not contain the correct entry to run the watchdog every minute."

def test_logrotate_configured():
    """Verify the logrotate configuration file contains the required directives."""
    conf_path = '/home/user/watchrotate.conf'
    assert os.path.isfile(conf_path), f"Logrotate config {conf_path} is missing."

    with open(conf_path, 'r') as f:
        content = f.read()

    assert '/home/user/watchdog.log' in content, "Logrotate config missing the target log file."
    assert re.search(r'\bdaily\b', content), "Logrotate config missing 'daily' directive."
    assert re.search(r'\brotate\s+5\b', content), "Logrotate config missing 'rotate 5' directive."
    assert re.search(r'\bcompress\b', content), "Logrotate config missing 'compress' directive."
    assert re.search(r'\bmissingok\b', content), "Logrotate config missing 'missingok' directive."
    assert re.search(r'\bcreate\s+(0?644)\b', content), "Logrotate config missing 'create 0644' directive."

def get_flaky_api_pid():
    result = subprocess.run(['pgrep', '-f', 'flaky_api.py'], capture_output=True, text=True)
    pids = result.stdout.strip().split('\n')
    pids = [pid for pid in pids if pid]
    if pids:
        return pids[0]
    return None

def kill_flaky_api():
    subprocess.run(['pkill', '-f', 'flaky_api.py'])
    time.sleep(0.5)

def run_watchdog():
    result = subprocess.run(['/usr/bin/python3', '/home/user/watchdog.py'], capture_output=True, text=True)
    return result

def check_log_for_reason(reason):
    log_path = '/home/user/watchdog.log'
    assert os.path.isfile(log_path), f"Log file {log_path} not found."
    with open(log_path, 'r') as f:
        lines = f.readlines()

    if not lines:
        return False

    last_line = lines[-1].strip()
    pattern = rf"^\[\d{{4}}-\d{{2}}-\d{{2}} \d{{2}}:\d{{2}}:\d{{2}}\] RESTART triggered\. Reason: {reason}$"
    return bool(re.match(pattern, last_line))

def test_watchdog_down_behavior():
    """Verify watchdog restarts the service when it is DOWN."""
    kill_flaky_api()
    assert get_flaky_api_pid() is None, "Failed to kill flaky_api.py for testing."

    run_watchdog()
    time.sleep(1)

    assert get_flaky_api_pid() is not None, "Watchdog failed to restart the service when DOWN."
    assert check_log_for_reason("DOWN"), "Watchdog log does not contain the correct DOWN reason format."

def test_watchdog_timeout_behavior():
    """Verify watchdog restarts the service when it TIMEOUTs."""
    kill_flaky_api()
    subprocess.Popen(['/usr/bin/python3', '/home/user/flaky_api.py'])
    time.sleep(1)

    old_pid = get_flaky_api_pid()
    assert old_pid is not None, "Service is not running."

    # Simulate timeout
    with open('/home/user/hang.flag', 'w') as f:
        f.write("1")

    run_watchdog()
    time.sleep(1)

    os.remove('/home/user/hang.flag')

    new_pid = get_flaky_api_pid()
    assert new_pid is not None, "Service is not running after timeout restart."
    assert new_pid != old_pid, "Watchdog failed to restart the service (PID unchanged) when TIMEOUT."
    assert check_log_for_reason("TIMEOUT"), "Watchdog log does not contain the correct TIMEOUT reason format."

def test_watchdog_error_behavior():
    """Verify watchdog restarts the service when it returns ERROR."""
    kill_flaky_api()
    subprocess.Popen(['/usr/bin/python3', '/home/user/flaky_api.py'])
    time.sleep(1)

    old_pid = get_flaky_api_pid()
    assert old_pid is not None, "Service is not running."

    # Simulate error
    with open('/home/user/error.flag', 'w') as f:
        f.write("1")

    run_watchdog()
    time.sleep(1)

    if os.path.exists('/home/user/error.flag'):
        os.remove('/home/user/error.flag')

    new_pid = get_flaky_api_pid()
    assert new_pid is not None, "Service is not running after error restart."
    assert new_pid != old_pid, "Watchdog failed to restart the service (PID unchanged) when ERROR."
    assert check_log_for_reason("ERROR"), "Watchdog log does not contain the correct ERROR reason format."