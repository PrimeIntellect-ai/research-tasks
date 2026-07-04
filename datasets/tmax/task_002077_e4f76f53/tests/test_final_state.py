# test_final_state.py

import os
import subprocess
import pytest

def test_api_key_file():
    api_key_path = "/home/user/api_key.txt"
    assert os.path.isfile(api_key_path), f"The file {api_key_path} does not exist."

    with open(api_key_path, "r") as f:
        content = f.read().strip()

    # The API key found in the git history
    expected_key = "SRE_PROD_99382A"
    assert expected_key in content, f"The file {api_key_path} does not contain the correct API key."

def test_final_score_file():
    final_score_path = "/home/user/final_score.txt"
    assert os.path.isfile(final_score_path), f"The file {final_score_path} does not exist."

    with open(final_score_path, "r") as f:
        content = f.read().strip()

    expected_score = "12750"
    assert content == expected_score, f"The file {final_score_path} contains '{content}', but expected '{expected_score}'."

def test_monitor_script_fixed():
    script_path = "/home/user/uptime-monitor/monitor.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

    # Run the script with the logs to ensure it doesn't crash on '08' or '09'
    env = os.environ.copy()
    env["API_KEY"] = "SRE_PROD_99382A"

    log_files = [
        "/home/user/logs/server1.log",
        "/home/user/logs/server2.log"
    ]

    try:
        result = subprocess.run(
            [script_path] + log_files,
            env=env,
            capture_output=True,
            text=True,
            check=True
        )
        output = result.stdout.strip()
        assert output == "12750", f"The script output was '{output}', expected '12750'. The mathematical bug might not be fully fixed."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"The script crashed or returned a non-zero exit code. Error output: {e.stderr.strip()}")