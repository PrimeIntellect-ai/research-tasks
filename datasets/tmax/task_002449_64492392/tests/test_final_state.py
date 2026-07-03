# test_final_state.py
import os
import csv
import re
import pytest

def test_process_script_exists_and_executable():
    """Verify that the process.py script exists and is executable."""
    script_path = '/home/user/process.py'
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"The script {script_path} is not executable."

def test_clean_users_csv_exists_and_correct():
    """Verify the output CSV is correctly processed, sorted, deduplicated, and masked."""
    csv_path = '/home/user/clean_users.csv'
    assert os.path.isfile(csv_path), f"The output file {csv_path} does not exist."

    with open(csv_path, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            pytest.fail(f"The file {csv_path} is empty.")

        expected_headers = ['user_id', 'name', 'email', 'signup_date']
        assert headers == expected_headers, f"Headers are incorrect. Expected {expected_headers}, got {headers}."

        rows = list(reader)

    assert len(rows) == 5, f"Expected 5 rows in {csv_path}, but got {len(rows)}."

    # Check sorting and deduplication
    user_ids = [int(row[0]) for row in rows]
    assert user_ids == [1, 2, 3, 4, 5], f"Rows are not deduplicated or not sorted by user_id correctly. Got user_ids: {user_ids}."

    # Validate specific rows for masking and date normalization
    expected_data = {
        1: {'email': '*********th@example.com', 'date': '2023-01-15'},
        2: {'email': '****es@test.org', 'date': '2023-02-20'},
        3: {'email': '****wn@peanuts.com', 'date': '2023-03-10'},
        4: {'email': '***na@themyscira.gov', 'date': '2022-12-05'},
        5: {'email': 'ed@short.com', 'date': '2023-05-12'},
    }

    for row in rows:
        uid = int(row[0])
        email = row[2]
        date = row[3]

        expected = expected_data[uid]
        assert email == expected['email'], f"Email masking failed for user_id {uid}. Expected {expected['email']}, got {email}."
        assert date == expected['date'], f"Date normalization failed for user_id {uid}. Expected {expected['date']}, got {date}."

def test_cron_backup_correct():
    """Verify that the cron job was scheduled correctly and backed up."""
    backup_path = '/home/user/cron_backup.txt'
    assert os.path.isfile(backup_path), f"The cron backup file {backup_path} does not exist."

    with open(backup_path, 'r') as f:
        content = f.read()

    # Regex to match: 0 2 * * * /home/user/process.py
    # Allows for varying whitespace between cron fields
    pattern = r'^0\s+2\s+\*\s+\*\s+\*\s+/home/user/process\.py\s*$'

    match = False
    for line in content.splitlines():
        if re.match(pattern, line.strip()):
            match = True
            break

    assert match, f"Could not find the correct cron schedule in {backup_path}. Expected a line matching '0 2 * * * /home/user/process.py'."