# test_final_state.py

import os
import json
import subprocess
import pytest

def get_expected_values():
    """
    Attempt to derive the expected values from the Git repository forensics,
    falling back to the known truth if the repository state was altered.
    """
    repo_dir = "/home/user/legacy_repo"
    try:
        # Find the commit that added config.json and extract its content
        log_proc = subprocess.run(
            ["git", "log", "--all", "--format=%H", "--", "config.json"],
            cwd=repo_dir,
            capture_output=True,
            text=True,
            check=True
        )
        commits = log_proc.stdout.strip().split('\n')
        # The oldest commit touching config.json should be the one that added it
        if commits and commits[-1]:
            show_proc = subprocess.run(
                ["git", "show", f"{commits[-1]}:config.json"],
                cwd=repo_dir,
                capture_output=True,
                text=True,
                check=True
            )
            config_data = json.loads(show_proc.stdout)
            return config_data.get("api_key"), config_data.get("endpoint")
    except Exception:
        pass

    # Fallback to known truth if git forensics fail
    return "SECRET-99xJ2-44mAq-11bZw", "/v3/telemetry/ingest"

def test_fix_info_json_exists_and_valid():
    target_file = "/home/user/fix_info.json"
    assert os.path.isfile(target_file), f"Expected output file not found at {target_file}. Did you create it?"

    with open(target_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {target_file} does not contain valid JSON.")

    assert isinstance(data, dict), f"The JSON in {target_file} must be an object/dictionary."
    assert "api_key" in data, f"The JSON file {target_file} is missing the 'api_key' key."
    assert "endpoint" in data, f"The JSON file {target_file} is missing the 'endpoint' key."

def test_fix_info_json_contents():
    target_file = "/home/user/fix_info.json"
    if not os.path.isfile(target_file):
        pytest.skip("Output file missing, skipping content validation.")

    with open(target_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.skip("Output file is not valid JSON, skipping content validation.")

    expected_api_key, expected_endpoint = get_expected_values()

    actual_api_key = data.get("api_key")
    actual_endpoint = data.get("endpoint")

    assert actual_api_key == expected_api_key, (
        f"Incorrect api_key recovered. Expected '{expected_api_key}', but got '{actual_api_key}'."
    )

    assert actual_endpoint == expected_endpoint, (
        f"Incorrect endpoint recovered. Expected '{expected_endpoint}', but got '{actual_endpoint}'."
    )