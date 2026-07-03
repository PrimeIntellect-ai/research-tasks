# test_final_state.py

import os
import csv
import pytest

def get_expected_costs(base_dir):
    expected_data = {}
    if not os.path.isdir(base_dir):
        return expected_data

    for user in os.listdir(base_dir):
        user_dir = os.path.join(base_dir, user)
        if not os.path.isdir(user_dir):
            continue

        total_bytes = 0
        total_cost = 0

        for root, _, files in os.walk(user_dir):
            for file in files:
                filepath = os.path.join(root, file)
                size = os.path.getsize(filepath)
                total_bytes += size

                ext = os.path.splitext(file)[1].lower()
                if ext == '.log':
                    total_cost += size * 1
                elif ext == '.db':
                    total_cost += size * 5
                elif ext == '.tmp':
                    total_cost += size * 0
                else:
                    total_cost += size * 2

        expected_data[user] = {"TotalBytes": total_bytes, "TotalCost": total_cost}

    return expected_data

def test_cpp_file_exists():
    cpp_file = "/home/user/cost_analyzer.cpp"
    assert os.path.isfile(cpp_file), f"C++ source file {cpp_file} is missing."

def test_bash_script_exists_and_executable():
    bash_script = "/home/user/run_analysis.sh"
    assert os.path.isfile(bash_script), f"Bash script {bash_script} is missing."
    assert os.access(bash_script, os.X_OK), f"Bash script {bash_script} is not executable."

def test_cost_report_csv():
    csv_file = "/home/user/cost_report.csv"
    assert os.path.isfile(csv_file), f"Output file {csv_file} is missing."

    expected_data = get_expected_costs("/home/user/cloud_storage")
    assert expected_data, "Could not compute expected data; /home/user/cloud_storage might be missing."

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 0, f"{csv_file} is empty."

    header = rows[0]
    expected_header = ["Username", "TotalBytes", "TotalCost"]
    assert header == expected_header, f"Header in {csv_file} is {header}, expected {expected_header}."

    parsed_data = {}
    for row in rows[1:]:
        assert len(row) == 3, f"Row {row} does not have exactly 3 columns."
        username, total_bytes, total_cost = row
        parsed_data[username] = {
            "TotalBytes": int(total_bytes),
            "TotalCost": int(total_cost)
        }

    expected_users = sorted(expected_data.keys())
    actual_users = list(parsed_data.keys())

    assert actual_users == expected_users, f"Users in CSV are not sorted alphabetically or do not match expected. Actual: {actual_users}, Expected: {expected_users}"

    for user in expected_users:
        expected_bytes = expected_data[user]["TotalBytes"]
        expected_cost = expected_data[user]["TotalCost"]
        actual_bytes = parsed_data[user]["TotalBytes"]
        actual_cost = parsed_data[user]["TotalCost"]

        assert actual_bytes == expected_bytes, f"User {user} has TotalBytes {actual_bytes}, expected {expected_bytes}."
        assert actual_cost == expected_cost, f"User {user} has TotalCost {actual_cost}, expected {expected_cost}."