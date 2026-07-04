# test_final_state.py
import os
import re

def test_bashrc_contains_env_var():
    """Verify that EDGE_NODE_ID=IOT-992 is in /home/user/.bashrc."""
    bashrc_path = "/home/user/.bashrc"
    assert os.path.isfile(bashrc_path), f"{bashrc_path} does not exist or is not a file."

    with open(bashrc_path, "r") as f:
        content = f.read()

    assert "EDGE_NODE_ID=IOT-992" in content, "EDGE_NODE_ID=IOT-992 not found in /home/user/.bashrc."

def test_iot_config_ini():
    """Verify /home/user/iot_config.ini exists and has correct values."""
    config_path = "/home/user/iot_config.ini"
    assert os.path.isfile(config_path), f"{config_path} does not exist or is not a file."

    with open(config_path, "r") as f:
        content = f.read()

    assert re.search(r"AdminEmail\s*=\s*ops@edge\.local", content), "AdminEmail=ops@edge.local not found in iot_config.ini."
    assert re.search(r"SpoolDir\s*=\s*/home/user/mail_spool/outbox", content), "SpoolDir=/home/user/mail_spool/outbox not found in iot_config.ini."

def test_monitor_cpp_and_executable_exist():
    """Verify the monitor.cpp and compiled monitor executable exist."""
    cpp_path = "/home/user/monitor.cpp"
    exe_path = "/home/user/monitor"

    assert os.path.isfile(cpp_path), f"{cpp_path} does not exist."
    assert os.path.isfile(exe_path), f"{exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"{exe_path} is not executable."

def test_alert_eml_content():
    """Verify the contents of the generated alert.eml."""
    alert_path = "/home/user/mail_spool/outbox/alert.eml"
    assert os.path.isfile(alert_path), f"{alert_path} does not exist. Did the monitor program run and generate it?"

    expected_content = (
        "To: ops@edge.local\n"
        "Subject: ALERT: Node IOT-992 offline\n\n"
        "The sensor process is down.\n"
    )

    with open(alert_path, "r") as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_content.strip(), (
        f"Content of {alert_path} does not match expected.\n"
        f"Expected:\n{expected_content}\n"
        f"Actual:\n{actual_content}"
    )