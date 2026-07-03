# test_final_state.py

import os
import csv
import pytest

def get_expected_total():
    csv_path = "/home/user/cloud_costs.csv"
    if not os.path.exists(csv_path):
        pytest.fail(f"Required file {csv_path} is missing.")

    total = 0.0
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cost = float(row['Cost'])
            if cost > 500.00:
                total += cost
    return f"{total:.2f}"

def get_expected_email_content():
    total = get_expected_total()
    return (
        "To: finops-list@local.domain\n"
        "From: billing-bot@local.domain\n"
        "Subject: Daily High Cost Alert\n"
        "\n"
        f"Total high cost: ${total}\n"
    )

def test_directories_exist():
    archive_dir = "/home/user/reports/archive/"
    outbox_dir = "/home/user/mail_spool/outbox/"

    assert os.path.isdir(archive_dir), f"Directory {archive_dir} does not exist."
    assert os.path.isdir(outbox_dir), f"Directory {outbox_dir} does not exist."

def test_symlink_exists_and_correct():
    symlink_path = "/home/user/reports/latest_alert.eml"
    target_path = "/home/user/reports/archive/cost_alert.eml"

    assert os.path.islink(symlink_path), f"{symlink_path} is not a symbolic link."

    actual_target = os.readlink(symlink_path)
    assert actual_target == target_path, f"Symlink points to {actual_target} instead of {target_path}."

def test_archive_email_content():
    email_path = "/home/user/reports/archive/cost_alert.eml"
    assert os.path.isfile(email_path), f"File {email_path} does not exist."

    with open(email_path, 'r', encoding='utf-8') as f:
        content = f.read()

    expected_content = get_expected_email_content()
    assert content.strip() == expected_content.strip(), f"Content of {email_path} does not match expected format and calculation."

def test_outbox_email_content():
    email_path = "/home/user/mail_spool/outbox/cost_alert.eml"
    assert os.path.isfile(email_path), f"File {email_path} does not exist."

    with open(email_path, 'r', encoding='utf-8') as f:
        content = f.read()

    expected_content = get_expected_email_content()
    assert content.strip() == expected_content.strip(), f"Content of {email_path} does not match expected format and calculation."