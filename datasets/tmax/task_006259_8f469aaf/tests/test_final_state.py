# test_final_state.py
import os
import csv
from collections import defaultdict

def test_output_directory_exists():
    assert os.path.isdir("/home/user/output"), "Directory /home/user/output/ does not exist. The script should create it."

def test_normalized_joined_csv():
    filepath = "/home/user/output/normalized_joined.csv"
    assert os.path.isfile(filepath), f"File {filepath} does not exist."

    with open(filepath, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 1, f"{filepath} is empty or missing data rows."

    header = rows[0]
    expected_header = ["timestamp", "ip", "user_id", "role", "region", "endpoint", "status"]
    assert header == expected_header, f"{filepath} header is incorrect. Expected {expected_header}, got {header}."

    data_rows = rows[1:]

    # Check sorting by timestamp
    timestamps = [row[0] for row in data_rows]
    assert timestamps == sorted(timestamps), f"{filepath} is not sorted chronologically by timestamp."

    # Check endpoint normalization
    for i, row in enumerate(data_rows):
        endpoint = row[5]
        assert "?" not in endpoint, f"Row {i+1} in {filepath} contains a query parameter in the endpoint: {endpoint}"
        assert endpoint == endpoint.lower(), f"Row {i+1} in {filepath} contains uppercase characters in the endpoint: {endpoint}"

        # Check join correctness (simple check for a known user)
        user_id = row[2]
        role = row[3]
        if user_id == "101":
            assert role == "admin", f"Join failed for user 101: expected role 'admin', got '{role}'."

def test_stratified_sample_csv():
    filepath = "/home/user/output/stratified_sample.csv"
    assert os.path.isfile(filepath), f"File {filepath} does not exist."

    with open(filepath, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 1, f"{filepath} is empty or missing data rows."

    header = rows[0]
    expected_header = ["timestamp", "ip", "user_id", "role", "region", "endpoint", "status"]
    assert header == expected_header, f"{filepath} header is incorrect. Expected {expected_header}, got {header}."

    data_rows = rows[1:]

    # Verify sorting: alphabetically by role, then chronologically by timestamp
    roles_timestamps = [(row[3], row[0]) for row in data_rows]
    assert roles_timestamps == sorted(roles_timestamps), f"{filepath} is not sorted by role and then by timestamp."

    # Verify max 2 per role
    role_counts = defaultdict(int)
    for row in data_rows:
        role_counts[row[3]] += 1

    for role, count in role_counts.items():
        assert count <= 2, f"Role '{role}' has more than 2 entries ({count}) in {filepath}."

    # Verify they are the *first* chronological logs (we check against known data)
    # The expected roles present should be admin, bot, guest, user
    expected_roles = {"admin", "bot", "guest", "user"}
    found_roles = set(role_counts.keys())
    assert found_roles == expected_roles, f"Expected roles {expected_roles} in sample, but found {found_roles}."

def test_anomaly_user_txt():
    filepath = "/home/user/output/anomaly_user.txt"
    assert os.path.isfile(filepath), f"File {filepath} does not exist."

    with open(filepath, "r") as f:
        content = f.read().strip()

    assert content == "105", f"Incorrect anomaly user identified. Expected '105', got '{content}'."