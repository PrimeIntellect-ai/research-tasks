# test_final_state.py

import os
import json
from collections import defaultdict

def test_blocked_users_file():
    log_path = "/home/user/access_log.json"
    output_path = "/home/user/blocked_users.txt"
    script_path = "/home/user/check_rate.py"

    assert os.path.exists(script_path), f"Script {script_path} is missing."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    assert os.path.exists(output_path), f"Output file {output_path} is missing."
    assert os.path.isfile(output_path), f"{output_path} is not a file."

    # Recompute the expected blocked users
    assert os.path.exists(log_path), f"Input file {log_path} is missing."
    with open(log_path, 'r') as f:
        try:
            logs = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {log_path} is not valid JSON."

    user_times = defaultdict(list)
    for entry in logs:
        user_times[entry["user"]].append(entry["time"])

    expected_blocked = set()
    for user, times in user_times.items():
        times.sort()
        for i in range(len(times) - 4):
            if times[i + 4] - times[i] <= 10:
                expected_blocked.add(user)
                break

    expected_output = sorted(list(expected_blocked))

    # Read the actual output
    with open(output_path, 'r') as f:
        actual_lines = f.read().splitlines()

    # Strip whitespace and remove empty lines for robustness
    actual_output = [line.strip() for line in actual_lines if line.strip()]

    assert actual_output == expected_output, (
        f"The contents of {output_path} are incorrect.\n"
        f"Expected: {expected_output}\n"
        f"Got: {actual_output}"
    )