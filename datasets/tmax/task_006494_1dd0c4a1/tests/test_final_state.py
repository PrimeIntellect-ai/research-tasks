# test_final_state.py
import os
import subprocess
import pytest

def test_alert_env_exists():
    """Check that .alert_env exists and exports ALERT_CODE correctly."""
    env_file = '/home/user/.alert_env'
    assert os.path.isfile(env_file), f"Environment file {env_file} is missing."

    # Test sourcing the file and echoing the variable
    result = subprocess.run(
        f"source {env_file} && echo $ALERT_CODE",
        shell=True,
        executable="/bin/bash",
        capture_output=True,
        text=True
    )
    assert result.stdout.strip() == "DEP_FAIL_01", f"ALERT_CODE is not correctly exported in {env_file}."

def test_scripts_executable():
    """Check that the scripts exist and are executable."""
    py_script = '/home/user/check_deploy.py'
    sh_script = '/home/user/rotate_alerts.sh'

    assert os.path.isfile(py_script), f"Python script {py_script} is missing."
    assert os.access(py_script, os.X_OK), f"Python script {py_script} is not executable."

    assert os.path.isfile(sh_script), f"Bash script {sh_script} is missing."
    assert os.access(sh_script, os.X_OK), f"Bash script {sh_script} is not executable."

def test_check_deploy_behavior():
    """Test the behavior of the check_deploy.py script."""
    env_file = '/home/user/.alert_env'
    py_script = '/home/user/check_deploy.py'
    alerts_log = '/home/user/alerts.log'

    # Ensure alerts.log does not exist or is empty before test
    if os.path.exists(alerts_log):
        os.remove(alerts_log)

    # Run the script with the environment sourced
    subprocess.run(
        f"source {env_file} && python3 {py_script}",
        shell=True,
        executable="/bin/bash",
        check=True
    )

    assert os.path.isfile(alerts_log), f"{alerts_log} was not created by the script."

    with open(alerts_log, 'r') as f:
        lines = f.read().splitlines()

    expected_line = "[DEP_FAIL_01] Alert triggered: Dependency not ready"
    assert len(lines) == 2, f"Expected 2 lines in {alerts_log}, but found {len(lines)}."
    assert lines[0] == expected_line, f"First line in {alerts_log} is incorrect."
    assert lines[1] == expected_line, f"Second line in {alerts_log} is incorrect."

def test_rotate_alerts_under_limit():
    """Test that rotate_alerts.sh does nothing when lines <= 5."""
    sh_script = '/home/user/rotate_alerts.sh'
    alerts_log = '/home/user/alerts.log'
    bak_log = '/home/user/alerts.log.bak'

    if os.path.exists(bak_log):
        os.remove(bak_log)

    # The alerts.log currently has 2 lines from the previous test
    subprocess.run(
        f"bash {sh_script}",
        shell=True,
        executable="/bin/bash",
        check=True
    )

    assert not os.path.exists(bak_log), f"{bak_log} should not be created when lines <= 5."

    with open(alerts_log, 'r') as f:
        lines = f.read().splitlines()
    assert len(lines) == 2, "alerts.log was improperly modified when lines <= 5."

def test_rotate_alerts_over_limit():
    """Test that rotate_alerts.sh rotates the log when lines > 5."""
    sh_script = '/home/user/rotate_alerts.sh'
    alerts_log = '/home/user/alerts.log'
    bak_log = '/home/user/alerts.log.bak'

    # Append 4 lines to make it 6 lines total
    with open(alerts_log, 'a') as f:
        for _ in range(4):
            f.write("dummy log\n")

    subprocess.run(
        f"bash {sh_script}",
        shell=True,
        executable="/bin/bash",
        check=True
    )

    assert os.path.isfile(bak_log), f"{bak_log} was not created when lines > 5."

    with open(bak_log, 'r') as f:
        bak_lines = f.read().splitlines()
    assert len(bak_lines) == 6, f"Expected 6 lines in {bak_log}, found {len(bak_lines)}."

    assert os.path.isfile(alerts_log), f"{alerts_log} was deleted instead of truncated/recreated."
    with open(alerts_log, 'r') as f:
        new_lines = f.read().splitlines()
    assert len(new_lines) == 0, f"{alerts_log} should be empty after rotation."