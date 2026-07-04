# test_final_state.py
import os
import json
import pytest

def test_directories_exist():
    dirs = [
        "/home/user/capacity_planner/configs",
        "/home/user/capacity_planner/logs",
        "/home/user/capacity_planner/bin"
    ]
    for d in dirs:
        assert os.path.isdir(d), f"Directory {d} is missing or not a directory."

def test_config_and_symlink():
    config_path = "/home/user/capacity_planner/configs/prod.json"
    assert os.path.isfile(config_path), f"Config file {config_path} is missing."

    with open(config_path, 'r') as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Config file {config_path} is not valid JSON.")

    assert config.get("cpu_max") == 90, "cpu_max in config is not 90."
    assert config.get("mem_max") == 80, "mem_max in config is not 80."
    assert config.get("alert_email") == "alerts@capacity.local", "alert_email in config is incorrect."

    symlink_path = "/home/user/capacity_planner/active_config"
    assert os.path.islink(symlink_path), f"{symlink_path} is not a symlink."

    target = os.readlink(symlink_path)
    # Target could be relative or absolute, let's resolve it
    abs_target = os.path.abspath(os.path.join(os.path.dirname(symlink_path), target))
    assert abs_target == config_path, f"Symlink points to {abs_target} instead of {config_path}."

def test_simulated_metrics_csv():
    csv_path = "/home/user/capacity_planner/simulated_metrics.csv"
    assert os.path.isfile(csv_path), f"CSV file {csv_path} is missing."
    with open(csv_path, 'r') as f:
        content = f.read().strip()
    assert "timestamp,cpu_usage,mem_usage" in content, "CSV header is missing or incorrect."
    assert "1600000004,99,99" in content, "CSV data is missing or incorrect."

def test_scripts_exist():
    smtp_script = "/home/user/capacity_planner/bin/mock_smtp.py"
    monitor_script = "/home/user/capacity_planner/bin/monitor.py"

    assert os.path.isfile(smtp_script), f"Script {smtp_script} is missing."
    assert os.path.isfile(monitor_script), f"Script {monitor_script} is missing."

def test_supervisord_conf():
    conf_path = "/home/user/capacity_planner/supervisord.conf"
    assert os.path.isfile(conf_path), f"Supervisord config {conf_path} is missing."
    with open(conf_path, 'r') as f:
        content = f.read()
    assert "mock_smtp.py" in content, "mock_smtp.py not referenced in supervisord.conf."
    assert "monitor.py" in content, "monitor.py not referenced in supervisord.conf."

def test_emails_log():
    log_path = "/home/user/capacity_planner/logs/emails.log"
    assert os.path.isfile(log_path), f"Log file {log_path} is missing. Did the monitor and smtp server run?"

    with open(log_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_alerts = [
        "ALERT: timestamp=1600000002, cpu=95, mem=70",
        "ALERT: timestamp=1600000003, cpu=50, mem=85",
        "ALERT: timestamp=1600000004, cpu=99, mem=99"
    ]

    assert len(lines) == len(expected_alerts), f"Expected {len(expected_alerts)} alerts in log, found {len(lines)}."

    for i, expected in enumerate(expected_alerts):
        assert expected in lines[i], f"Log line {i+1} does not contain expected alert. Expected: '{expected}', Found: '{lines[i]}'"