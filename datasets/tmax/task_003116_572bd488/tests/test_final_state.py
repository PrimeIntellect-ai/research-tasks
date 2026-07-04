# test_final_state.py
import os
import subprocess
import re

def test_operator_binary():
    bin_path = "/home/user/bin/operator"
    log_path = "/home/user/logs/operator.log"
    manifests_dir = "/home/user/manifests"

    assert os.path.exists(bin_path), f"Binary {bin_path} does not exist."
    assert os.access(bin_path, os.X_OK), f"Binary {bin_path} is not executable."

    # Clear log
    if os.path.exists(log_path):
        os.remove(log_path)

    # Run binary
    result = subprocess.run([bin_path], capture_output=True)
    assert result.returncode == 0, f"Operator binary exited with non-zero status: {result.returncode}"

    assert os.path.exists(log_path), f"Log file {log_path} was not created."

    with open(log_path, 'r') as f:
        log_content = f.read()

    # Check for expected manifests
    expected_files = ["deployment.yaml", "service.yaml", "ingress.yaml"]
    for expected_file in expected_files:
        if os.path.exists(os.path.join(manifests_dir, expected_file)):
            expected_log = f"[SUCCESS] Deployed {expected_file}"
            assert expected_log in log_content, f"Expected log entry '{expected_log}' not found in {log_path}."

def test_logrotate_conf():
    conf_path = "/home/user/logrotate.conf"
    assert os.path.exists(conf_path), f"Logrotate config {conf_path} does not exist."

    with open(conf_path, 'r') as f:
        content = f.read().lower()

    assert "/home/user/logs/operator.log" in content, f"Logrotate config missing target log file."
    assert "daily" in content, "Logrotate config missing 'daily' directive."
    assert re.search(r"rotate\s+3", content), "Logrotate config missing 'rotate 3' directive."
    assert "compress" in content, "Logrotate config missing 'compress' directive."
    assert "create" in content, "Logrotate config missing 'create' directive."

def test_cron_configuration():
    cron_file = "/home/user/operator.cron"
    assert os.path.exists(cron_file), f"Cron file {cron_file} does not exist."

    with open(cron_file, 'r') as f:
        content = f.read()

    cron_pattern = r"\*/5\s+\*\s+\*\s+\*\s+\*\s+/home/user/bin/operator"
    assert re.search(cron_pattern, content), f"Cron file {cron_file} does not contain the correct schedule."

    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab."
    assert re.search(cron_pattern, result.stdout), "Crontab does not contain the correct schedule."

def test_ci_cd_pipeline():
    script_path = "/home/user/build_and_test.sh"
    log_path = "/home/user/logs/operator.log"

    assert os.path.exists(script_path), f"CI script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"CI script {script_path} is not executable."

    if os.path.exists(log_path):
        os.remove(log_path)

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"CI script exited with non-zero status: {result.returncode}. Output: {result.stdout}"

    assert "CI PASSED" in result.stdout, "CI script did not print 'CI PASSED'."

    assert os.path.exists(log_path), f"Log file {log_path} was not created by CI script."
    with open(log_path, 'r') as f:
        log_content = f.read()

    assert "[SUCCESS] Deployed ci-test.yaml" in log_content, "Log file does not contain expected output from CI test."