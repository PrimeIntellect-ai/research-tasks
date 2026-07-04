# test_final_state.py

import os
import subprocess
import pytest

def test_release_binary_exists():
    binary_path = "/home/user/csv_processor/target/release/csv_processor"
    assert os.path.isfile(binary_path), f"Release binary not found at {binary_path}. Did you run 'cargo build --release'?"
    assert os.access(binary_path, os.X_OK), f"File at {binary_path} is not executable."

def test_cleaned_users_csv_content():
    csv_path = "/home/user/data/cleaned_users.csv"
    assert os.path.isfile(csv_path), f"Cleaned CSV file not found at {csv_path}. Did you run the compiled binary?"

    with open(csv_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = [
        "extracted_id,name,email",
        "100001,Alice Smith,alice@example.com",
        "100002,Bob Jones,bob.jones@test.org",
        "100003,Dave Miller,dave@miller.net"
    ]

    assert len(lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in cleaned CSV, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} in cleaned CSV does not match expected.\nExpected: {expected}\nActual: {actual}"

def test_crontab_entry_exists():
    try:
        result = subprocess.run(["crontab", "-l"], capture_output=True, text=True, check=True)
        crontab_content = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab. Ensure crontab is installed for the user.")

    found = False
    for line in crontab_content.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Check if the line matches the schedule and binary path
        parts = line.split()
        if len(parts) >= 6:
            schedule = " ".join(parts[:5])
            command = " ".join(parts[5:])
            if schedule == "30 2 * * *" and "/home/user/csv_processor/target/release/csv_processor" in command:
                found = True
                break

    assert found, "Crontab entry for the CSV processor not found or incorrect. Expected schedule '30 2 * * *' and command pointing to the release binary."