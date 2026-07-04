# test_final_state.py

import os
import re
import subprocess
import pytest

SCRIPT_PATH = "/home/user/scale_down.sh"
INSTANCES_PATH = "/home/user/instances.txt"
LOG_PATH = "/home/user/scale_log.txt"
CRON_PATH = "/home/user/finops.cron"

def test_script_exists_and_executable():
    assert os.path.isfile(SCRIPT_PATH), f"Script {SCRIPT_PATH} does not exist."
    assert os.access(SCRIPT_PATH, os.X_OK), f"Script {SCRIPT_PATH} is not executable."

def test_script_execution_and_output():
    # To ensure the script works correctly, we will remove the log file, run the script, and check the output.
    if os.path.exists(LOG_PATH):
        os.remove(LOG_PATH)

    try:
        subprocess.run([SCRIPT_PATH], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {SCRIPT_PATH} failed with error: {e.stderr}")

    assert os.path.isfile(LOG_PATH), f"Log file {LOG_PATH} was not created by the script."

    with open(LOG_PATH, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Parse the expected instances from instances.txt
    with open(INSTANCES_PATH, "r") as f:
        instances = []
        for line in f:
            parts = line.strip().split()
            if len(parts) == 2:
                instances.append((parts[0], float(parts[1]), parts[1]))

    # Sort instances by cost descending
    instances.sort(key=lambda x: x[1], reverse=True)

    assert len(lines) == len(instances), f"Expected {len(instances)} log entries, found {len(lines)}."

    # Since there could be ties in cost (e.g., 3.50), we group by cost and check sets of instance names
    expected_groups = {}
    for name, cost_val, cost_str in instances:
        expected_groups.setdefault(cost_val, []).append((name, cost_str))

    current_idx = 0
    # We iterate through the unique costs in descending order
    sorted_costs = sorted(expected_groups.keys(), reverse=True)

    for cost_val in sorted_costs:
        group = expected_groups[cost_val]
        group_size = len(group)

        actual_lines_for_group = lines[current_idx:current_idx + group_size]

        expected_lines_set = set(
            f"SHUTTING DOWN: {name} (Cost: {cost_str})" for name, cost_str in group
        )
        actual_lines_set = set(actual_lines_for_group)

        assert actual_lines_set == expected_lines_set, (
            f"Mismatch in log entries for cost {cost_val}. "
            f"Expected one of {expected_lines_set}, but got {actual_lines_set}."
        )

        current_idx += group_size

def test_cron_file():
    assert os.path.isfile(CRON_PATH), f"Cron file {CRON_PATH} does not exist."

    with open(CRON_PATH, "r") as f:
        content = f.read().strip()

    # Valid cron expression for 09:00 AM on weekdays
    cron_pattern = re.compile(r"^0\s+9\s+\*\s+\*\s+(1-5|MON-FRI|mon-fri)\s+/home/user/scale_down\.sh$")
    assert cron_pattern.match(content), (
        f"Cron file content '{content}' does not match the expected pattern for 09:00 AM on weekdays."
    )