# test_final_state.py

import os
import json
import pytest

def test_variance_result():
    """Test that variance_result.txt contains the correct population variance."""
    api_response_path = "/home/user/api_response.json"
    result_path = "/home/user/variance_result.txt"

    assert os.path.isfile(api_response_path), f"File {api_response_path} is missing."
    assert os.path.isfile(result_path), f"File {result_path} is missing. The script did not create the output file."

    # Calculate the expected variance
    with open(api_response_path, 'r') as f:
        data = json.load(f)

    success_vals = [d['value'] for d in data if d.get('status') == 'SUCCESS']
    assert len(success_vals) > 0, "No SUCCESS records found in the data."

    mean = sum(success_vals) / len(success_vals)
    variance = sum((x - mean) ** 2 for x in success_vals) / len(success_vals)
    expected_variance = f"{variance:.4f}"

    # Read the actual result
    with open(result_path, 'r') as f:
        actual_result = f.read().strip()

    assert actual_result == expected_variance, (
        f"Incorrect variance in {result_path}. "
        f"Expected '{expected_variance}', but got '{actual_result}'."
    )

def test_memory_profile():
    """Test that memory_profile.txt contains the output from /usr/bin/time -v."""
    profile_path = "/home/user/memory_profile.txt"

    assert os.path.isfile(profile_path), f"File {profile_path} is missing. Did you redirect the profiling output?"

    with open(profile_path, 'r') as f:
        content = f.read()

    assert "Maximum resident set size" in content, (
        f"File {profile_path} does not contain 'Maximum resident set size'. "
        "Make sure you ran the script with '/usr/bin/time -v' and redirected stderr."
    )