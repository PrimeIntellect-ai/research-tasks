# test_final_state.py

import os
import json
import csv
import re
import pytest

def test_department_stats_json():
    json_path = "/home/user/department_stats.json"
    assert os.path.isfile(json_path), f"File {json_path} does not exist. The Go program must generate this file."

    # Parse the generated JSON
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            actual_stats = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {json_path} is not a valid JSON file.")

    assert isinstance(actual_stats, dict), f"The root of {json_path} must be a JSON object (dictionary)."

    # Recompute the expected stats from the source files
    users_csv_path = "/home/user/data/users.csv"
    activity_log_path = "/home/user/data/activity.log"

    assert os.path.isfile(users_csv_path), f"Missing source file {users_csv_path}"
    assert os.path.isfile(activity_log_path), f"Missing source file {activity_log_path}"

    # Load user mappings
    uuid_to_dept = {}
    with open(users_csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            uuid_to_dept[row['uuid']] = row['department']

    # Parse activity log
    expected_stats = {}
    uuid_pattern = re.compile(r"User<([^>]+)>")
    with open(activity_log_path, 'r', encoding='utf-16le') as f:
        for line in f:
            match = uuid_pattern.search(line)
            if match:
                uuid = match.group(1)
                if uuid in uuid_to_dept:
                    dept = uuid_to_dept[uuid]
                    expected_stats[dept] = expected_stats.get(dept, 0) + 1

    # Compare actual with expected
    assert actual_stats == expected_stats, (
        f"The aggregated statistics in {json_path} do not match the expected values.\n"
        f"Expected: {expected_stats}\n"
        f"Actual: {actual_stats}"
    )