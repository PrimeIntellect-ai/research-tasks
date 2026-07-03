# test_final_state.py

import os
import hashlib
import pytest

def test_script_exists():
    script_path = "/home/user/clean_data.sh"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."

def test_cleaned_feedback_content():
    raw_path = "/home/user/raw_feedback.txt"
    cleaned_path = "/home/user/cleaned_feedback.txt"

    assert os.path.exists(cleaned_path), f"The output file {cleaned_path} does not exist."

    # Compute expected output
    expected_lines = []
    seen_feedback = set()

    with open(raw_path, "r") as f:
        for line in f:
            line = line.rstrip('\n')
            if not line:
                continue
            parts = line.split('|')
            if len(parts) != 4:
                continue
            row_id, email, timestamp, feedback = parts

            if feedback in seen_feedback:
                continue
            seen_feedback.add(feedback)

            # Anonymize email
            email_hash = hashlib.md5(email.encode('utf-8')).hexdigest()[:8]
            domain = email.split('@')[1] if '@' in email else ""
            anon_email = f"{email_hash}@{domain}"

            # Word count
            word_count = len(feedback.split())

            expected_lines.append(f"{row_id}|{anon_email}|{timestamp}|{feedback}|{word_count}\n")

    expected_content = "".join(expected_lines)

    with open(cleaned_path, "r") as f:
        actual_content = f.read()

    assert actual_content == expected_content, f"The content of {cleaned_path} is incorrect."

def test_report_content():
    raw_path = "/home/user/raw_feedback.txt"
    cleaned_path = "/home/user/cleaned_feedback.txt"
    report_path = "/home/user/report.md"

    assert os.path.exists(report_path), f"The report file {report_path} does not exist."

    with open(raw_path, "r") as f:
        raw_rows = sum(1 for line in f if line.rstrip('\n'))

    with open(cleaned_path, "r") as f:
        cleaned_rows = sum(1 for line in f if line.rstrip('\n'))

    expected_report = f"# Data Cleaning Report\nOriginal rows: {raw_rows}\nCleaned rows: {cleaned_rows}\n"

    with open(report_path, "r") as f:
        actual_report = f.read()

    assert actual_report.strip() == expected_report.strip(), f"The content of {report_path} is incorrect."