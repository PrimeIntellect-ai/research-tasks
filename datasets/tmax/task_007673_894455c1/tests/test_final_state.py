# test_final_state.py

import os
import stat
import pytest

def test_sensor_conf():
    conf_path = "/home/user/edge_config/sensor.conf"
    assert os.path.isfile(conf_path), f"{conf_path} does not exist."

    with open(conf_path, "r") as f:
        content = f.read()

    assert "THRESHOLD=85.5" in content, "THRESHOLD=85.5 missing in sensor.conf"
    assert "SENSOR_ID=NODE_42" in content, "SENSOR_ID=NODE_42 missing in sensor.conf"
    assert "ALERT_EMAIL=admin@edge.local" in content, "ALERT_EMAIL=admin@edge.local missing in sensor.conf"

def test_msmtprc():
    msmtprc_path = "/home/user/.msmtprc"
    assert os.path.isfile(msmtprc_path), f"{msmtprc_path} does not exist."

    # Check permissions
    st = os.stat(msmtprc_path)
    perms = stat.S_IMODE(st.st_mode)
    assert perms == 0o600, f"{msmtprc_path} permissions are {oct(perms)}, expected 0o600."

    with open(msmtprc_path, "r") as f:
        content = f.read().lower()

    assert "account default" in content or "account\tdefault" in content, "Account name 'default' missing in .msmtprc"
    assert "host localhost" in content or "host\tlocalhost" in content, "Host 'localhost' missing in .msmtprc"
    assert "port 2525" in content or "port\t2525" in content, "Port '2525' missing in .msmtprc"
    assert "from edge_node@local" in content or "from\tedge_node@local" in content, "From 'edge_node@local' missing in .msmtprc"
    assert "auth off" in content or "auth\toff" in content, "Auth 'off' missing in .msmtprc"

def test_analyzer_executable():
    cpp_path = "/home/user/src/analyzer.cpp"
    bin_path = "/home/user/bin/analyzer"

    assert os.path.isfile(cpp_path), f"{cpp_path} does not exist."
    assert os.path.isfile(bin_path), f"{bin_path} does not exist."
    assert os.access(bin_path, os.X_OK), f"{bin_path} is not executable."

def test_process_telemetry_script():
    script_path = "/home/user/bin/process_telemetry.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_alerts_generated():
    alerts_path = "/home/user/data/alerts_generated.txt"
    assert os.path.isfile(alerts_path), f"{alerts_path} does not exist. Did you run the script?"

    with open(alerts_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "ALERT: SENSOR_ID=NODE_42 VALUE=88.70",
        "ALERT: SENSOR_ID=NODE_42 VALUE=90.00",
        "ALERT: SENSOR_ID=NODE_42 VALUE=102.34"
    ]

    assert lines == expected_lines, f"Contents of {alerts_path} do not match the expected alerts."