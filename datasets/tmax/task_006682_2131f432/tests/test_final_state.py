# test_final_state.py
import os
import re

def test_env_script():
    env_path = "/home/user/monitor_env.sh"
    assert os.path.isfile(env_path), f"Environment script is missing at {env_path}"

    with open(env_path, 'r') as f:
        content = f.read()

    assert re.search(r'export\s+MONITOR_PORT=9090', content), "MONITOR_PORT=9090 is not exported correctly"
    assert re.search(r'export\s+SMTP_PORT=2525', content), "SMTP_PORT=2525 is not exported correctly"
    assert re.search(r'export\s+ALERT_EMAIL=oncall@staged-deploy\.local', content), "ALERT_EMAIL is not exported correctly"

def test_cpp_source():
    cpp_path = "/home/user/monitor.cpp"
    assert os.path.isfile(cpp_path), f"C++ source file is missing at {cpp_path}"

def test_executable():
    exe_path = "/home/user/monitor"
    assert os.path.isfile(exe_path), f"Executable is missing at {exe_path}"
    assert os.access(exe_path, os.X_OK), f"File at {exe_path} is not executable"

def test_email_log():
    log_path = "/home/user/email_alerts.log"
    assert os.path.isfile(log_path), f"Email alerts log is missing at {log_path}. Did the monitor run successfully?"

    with open(log_path, 'r') as f:
        content = f.read()

    assert "Subject: Alert: Port Down" in content, "The email subject is missing or incorrect in the log"
    assert "Port 9090 is unresponsive." in content, "The email body is missing or incorrect in the log"