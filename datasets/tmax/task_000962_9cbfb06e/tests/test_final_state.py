# test_final_state.py

import os

def test_v2_data_correctness():
    v2_data_path = "/home/user/v2_data.txt"
    assert os.path.exists(v2_data_path), f"File missing: {v2_data_path}"

    expected_content = """id|name|calculated_value
1|Alice|7.00
2|Bob|3.33
3|Charlie|10.70
4|David|84.25
"""
    with open(v2_data_path, "r") as f:
        content = f.read()

    assert content.strip() == expected_content.strip(), f"Content of {v2_data_path} does not match the expected V2 output."

def test_memory_profile_exists_and_valid():
    profile_path = "/home/user/memory_profile.txt"
    assert os.path.exists(profile_path), f"File missing: {profile_path}"

    with open(profile_path, "r") as f:
        content = f.read()

    assert "Maximum resident set size" in content, f"'{profile_path}' is missing 'Maximum resident set size' output from /usr/bin/time -v"
    assert "User time" in content, f"'{profile_path}' is missing 'User time' output from /usr/bin/time -v"
    assert "System time" in content, f"'{profile_path}' is missing 'System time' output from /usr/bin/time -v"