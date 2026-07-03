# test_final_state.py

import os
import re
import pytest

def compute_expected_distance():
    alpha_log_path = "/home/user/server_alpha.log"
    beta_log_path = "/home/user/server_beta.log"

    alpha_data = {}
    beta_data = {}

    pattern = re.compile(r"\[(\d+)\]\s+host=\w+\s+reqs=(\d+)")

    if os.path.exists(alpha_log_path):
        with open(alpha_log_path, 'r') as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    alpha_data[int(match.group(1))] = int(match.group(2))

    if os.path.exists(beta_log_path):
        with open(beta_log_path, 'r') as f:
            for line in f:
                match = pattern.search(line)
                if match:
                    beta_data[int(match.group(1))] = int(match.group(2))

    if not alpha_data and not beta_data:
        return 0

    min_ts = min(list(alpha_data.keys()) + list(beta_data.keys()))
    max_ts = max(list(alpha_data.keys()) + list(beta_data.keys()))

    total_distance = 0
    for ts in range(min_ts, max_ts + 1):
        a_reqs = alpha_data.get(ts, 0)
        b_reqs = beta_data.get(ts, 0)
        total_distance += abs(a_reqs - b_reqs)

    return total_distance

def test_distance_result():
    result_file = "/home/user/distance_result.txt"
    assert os.path.isfile(result_file), f"Expected result file {result_file} does not exist."

    with open(result_file, 'r') as f:
        content = f.read().strip()

    expected_distance = compute_expected_distance()
    expected_content = f"Total Distance: {expected_distance}"

    assert content == expected_content, f"Result file content '{content}' does not match expected '{expected_content}'."