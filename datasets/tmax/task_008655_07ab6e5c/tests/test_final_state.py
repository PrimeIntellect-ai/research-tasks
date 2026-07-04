# test_final_state.py

import os

def test_check_deploy_script_exists():
    script_path = "/home/user/check_deploy.py"
    assert os.path.exists(script_path), f"The script {script_path} does not exist. Did you create it?"
    assert os.path.isfile(script_path), f"{script_path} is not a file."

def test_deploy_monitor_log_contents():
    log_path = "/home/user/deploy_monitor.log"
    assert os.path.exists(log_path), f"The log file {log_path} does not exist."
    assert os.path.isfile(log_path), f"{log_path} is not a file."

    expected_lines = [
        "ENV: staging",
        "ROLLOUT: confirmed",
        "HTTP_CODE: 200",
        "UPTIME_STATUS: healthy"
    ]

    with open(log_path, "r") as f:
        content = f.read().strip()

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {log_path}, found {len(actual_lines)}."

    for i, (expected, actual) in enumerate(zip(expected_lines, actual_lines)):
        assert actual == expected, f"Line {i+1} in {log_path} is incorrect. Expected '{expected}', got '{actual}'."

def test_notify_eml_contents():
    eml_path = "/home/user/notify.eml"
    assert os.path.exists(eml_path), f"The email file {eml_path} does not exist."
    assert os.path.isfile(eml_path), f"{eml_path} is not a file."

    expected_content = (
        "From: sre@company.local\n"
        "To: admin@company.local\n"
        "Subject: Staging Rollout Status\n"
        "\n"
        "Deployment successful. Service is healthy."
    )

    with open(eml_path, "r") as f:
        content = f.read().strip()

    # Normalize line endings and spacing for robust comparison
    actual_lines = [line.strip() for line in content.splitlines()]
    expected_lines = [line.strip() for line in expected_content.splitlines()]

    assert actual_lines == expected_lines, f"The contents of {eml_path} do not match the expected email format."