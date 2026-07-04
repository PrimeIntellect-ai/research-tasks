# test_final_state.py
import os
import subprocess

def test_mailer_config_exists_and_correct():
    config_path = "/home/user/mailer_config.txt"
    assert os.path.isfile(config_path), f"Configuration file {config_path} is missing."
    with open(config_path, "r") as f:
        content = f.read()
    assert "ADMIN=admin@backup.local" in content, "Admin email in config is incorrect or missing."
    assert "PORT=2525" in content, "SMTP port in config is incorrect or missing."
    assert "STAGE=staging" in content, "Stage in config is incorrect or missing."

def test_expect_script_exists():
    script_path = "/home/user/setup_mailer.exp"
    assert os.path.isfile(script_path), f"Expect script {script_path} is missing."

def test_deploy_script_idempotent():
    script_path = "/home/user/deploy.sh"
    assert os.path.isfile(script_path), f"Deploy script {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"Deploy script {script_path} is not executable."

    # Run deploy.sh, it should output "Configuration already applied." and exit 0
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"deploy.sh failed with return code {result.returncode}"
    assert "Configuration already applied." in result.stdout, "deploy.sh did not output the expected idempotency message."

def test_c_program_and_binary_exist():
    c_source = "/home/user/check_spool.c"
    c_binary = "/home/user/check_spool"
    assert os.path.isfile(c_source), f"C source file {c_source} is missing."
    assert os.path.isfile(c_binary), f"Compiled binary {c_binary} is missing."
    assert os.access(c_binary, os.X_OK), f"Compiled binary {c_binary} is not executable."

def test_final_report_contents():
    report_path = "/home/user/final_report.txt"
    assert os.path.isfile(report_path), f"Final report {report_path} is missing."

    with open(report_path, "r") as f:
        content = f.read().strip()

    expected_lines = [
        "Admin: admin@backup.local",
        "Port: 2525",
        "Stage: staging",
        "Valid Emails: 2"
    ]

    actual_lines = [line.strip() for line in content.splitlines() if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Final report has {len(actual_lines)} lines, expected {len(expected_lines)}."

    for i, expected in enumerate(expected_lines):
        assert actual_lines[i] == expected, f"Line {i+1} of final report mismatch. Expected '{expected}', got '{actual_lines[i]}'."