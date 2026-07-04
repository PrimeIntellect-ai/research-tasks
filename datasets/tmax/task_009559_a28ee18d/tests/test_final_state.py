# test_final_state.py

import os
import subprocess
import pytest

def test_redact_script_exists_and_executable():
    script_path = "/home/user/redact.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_traffic_redacted_log_content():
    log_path = "/home/user/logs/traffic_redacted.log"
    assert os.path.isfile(log_path), f"The output log file {log_path} does not exist."

    expected_content = """[2023-10-27 10:00:01] Connection received from [IP_REDACTED]
[2023-10-27 10:00:02] Auth attempt with token [REDACTED] - SUCCESS
[2023-10-27 10:00:05] Data packet sent to [IP_REDACTED], payload size 1024
[2023-10-27 10:01:00] Admin login from [IP_REDACTED] using [REDACTED]
[2023-10-27 10:01:15] Ping from [IP_REDACTED]
[2023-10-27 10:02:00] Invalid token attempt: TKN_WRONG123 from [IP_REDACTED]
"""

    with open(log_path, "r") as f:
        actual_content = f.read()

    assert actual_content.strip() == expected_content.strip(), (
        "The content of traffic_redacted.log does not match the expected redacted output. "
        "Ensure both the token and all IPv4 addresses are properly redacted."
    )

def test_redact_script_functionality(tmp_path):
    script_path = "/home/user/redact.sh"
    if not os.path.isfile(script_path) or not os.access(script_path, os.X_OK):
        pytest.skip("Script missing or not executable")

    test_file = tmp_path / "test.log"
    test_file.write_text("IP: 10.0.0.1, Token: TKN_7x9qL2vP, Other IP: 192.168.100.200\n")

    try:
        result = subprocess.run([script_path, str(test_file)], capture_output=True, text=True, check=True)
        output = result.stdout.strip()
        assert output == "IP: [IP_REDACTED], Token: [REDACTED], Other IP: [IP_REDACTED]", (
            "The redact.sh script did not produce the correct output when tested with a sample file. "
            "Ensure it replaces the exact token with [REDACTED] and IPv4 addresses with [IP_REDACTED]."
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of redact.sh failed: {e.stderr}")