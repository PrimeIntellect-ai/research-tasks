# test_final_state.py

import os
import re

def test_config_env_content():
    config_path = "/home/user/pr_review/config.env"
    assert os.path.isfile(config_path), f"{config_path} does not exist. Did you run build.sh?"

    with open(config_path, "r") as f:
        content = f.read().strip()

    assert "CONFIG_ARCH=arm64" in content, f"Expected 'CONFIG_ARCH=arm64' in {config_path}, but found: {content}"

def test_test_results_log_exists():
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist. Did you save the output of e2e_test.sh?"

def test_test_results_log_content():
    log_path = "/home/user/test_results.log"
    assert os.path.isfile(log_path), f"{log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read()

    success_count = content.count("Success: Solved subset sum for target")
    assert success_count >= 5, f"Expected at least 5 successful executions in the log, found {success_count}. Log content:\n{content}"

    assert "429 Rate Limit Exceeded" not in content, "Found '429 Rate Limit Exceeded' in the test results. Rate limiting was not properly avoided."

def test_e2e_test_sh_has_sleep():
    script_path = "/home/user/pr_review/e2e_test.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    with open(script_path, "r") as f:
        content = f.read()

    # Look for 'sleep' command in the script
    assert re.search(r'\bsleep\s+', content) is not None, "e2e_test.sh does not contain a 'sleep' command to delay executions."