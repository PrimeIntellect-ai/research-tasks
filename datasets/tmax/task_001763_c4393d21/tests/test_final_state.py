# test_final_state.py

import os
import csv
import re
import pytest

def get_expected_data():
    csv_path = "/home/user/new_hires.csv"
    log_path = "/home/user/access.log"

    users = []
    usernames = []

    with open(csv_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            first = row['FirstName']
            last = row['LastName']
            base_user = (first[0] + last).lower()[:8]

            uname = base_user
            counter = 1
            while uname in usernames:
                # Need to truncate to append? The prompt says "append the digit 1 to the end of the truncated base string".
                # "truncate it to a maximum of 8 characters. If the resulting username already exists... append the digit 1 to the end of the truncated base string."
                uname = base_user + str(counter)
                counter += 1

            usernames.append(uname)
            row['Username'] = uname
            users.append(row)

    locked_users = set()
    with open(log_path, 'r') as f:
        for line in f:
            if "STATUS=LOCKED" in line:
                m = re.search(r'\[([^\]]+)\]', line)
                if m:
                    locked_users.add(m.group(1))

    return users, locked_users

def test_passwd_file():
    users, _ = get_expected_data()
    passwd_path = "/home/user/site_data/passwd"
    assert os.path.isfile(passwd_path), f"File {passwd_path} does not exist."

    with open(passwd_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == len(users), f"Expected {len(users)} entries in passwd, found {len(lines)}."

    dept_to_gid = {"Engineering": "2000", "Sales": "2001", "HR": "2002"}
    uid = 1000

    for i, user in enumerate(users):
        expected_line = f"{user['Username']}:x:{uid + i}:{dept_to_gid[user['Department']]}:{user['FirstName']} {user['LastName']}:/home/user/site_data/home/{user['Username']}:/bin/bash"
        assert lines[i] == expected_line, f"Passwd entry mismatch at line {i+1}. Expected '{expected_line}', got '{lines[i]}'."

def test_home_directories():
    users, _ = get_expected_data()
    for user in users:
        home_dir = f"/home/user/site_data/home/{user['Username']}"
        assert os.path.isdir(home_dir), f"Home directory {home_dir} does not exist."

def test_mail_spool():
    users, _ = get_expected_data()
    for user in users:
        spool_file = f"/home/user/site_data/mail_spool/{user['Username']}.txt"
        assert os.path.isfile(spool_file), f"Mail spool file {spool_file} does not exist."

        with open(spool_file, 'r') as f:
            content = f.read().strip().split('\n')

        assert len(content) == 2, f"Expected 2 lines in {spool_file}, got {len(content)}."
        assert content[0] == f"To: {user['Email']}", f"Incorrect To line in {spool_file}."
        assert content[1] == f"Subject: Welcome to {user['Department']}, {user['FirstName']}!", f"Incorrect Subject line in {spool_file}."

def test_locked_emails():
    users, locked_users = get_expected_data()
    locked_emails_path = "/home/user/site_data/locked_emails.txt"
    assert os.path.isfile(locked_emails_path), f"File {locked_emails_path} does not exist."

    expected_locked_emails = set()
    for user in users:
        if user['Username'] in locked_users:
            expected_locked_emails.add(user['Email'])

    with open(locked_emails_path, 'r') as f:
        actual_locked_emails = set(line.strip() for line in f if line.strip())

    assert actual_locked_emails == expected_locked_emails, f"Locked emails mismatch. Expected {expected_locked_emails}, got {actual_locked_emails}."

def test_mailing_lists():
    users, locked_users = get_expected_data()

    expected_lists = {}
    for user in users:
        if user['Username'] not in locked_users:
            dept = user['Department']
            expected_lists.setdefault(dept, set()).add(user['Email'])

    # Check all departments
    all_depts = set(u['Department'] for u in users)
    for dept in all_depts:
        list_file = f"/home/user/site_data/lists/{dept}.list"
        expected_emails = expected_lists.get(dept, set())

        if not expected_emails:
            # File should be empty or missing
            if os.path.exists(list_file):
                with open(list_file, 'r') as f:
                    content = f.read().strip()
                assert not content, f"List file {list_file} should be empty, but contains data."
        else:
            assert os.path.isfile(list_file), f"List file {list_file} does not exist."
            with open(list_file, 'r') as f:
                actual_emails = set(line.strip() for line in f if line.strip())
            assert actual_emails == expected_emails, f"Mailing list {dept} mismatch. Expected {expected_emails}, got {actual_emails}."