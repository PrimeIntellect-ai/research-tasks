# test_final_state.py

import os
import re

def test_raw_logs_downloaded():
    """Test that raw_logs.csv was downloaded to /home/user/raw_logs.csv"""
    assert os.path.isfile('/home/user/raw_logs.csv'), "raw_logs.csv was not downloaded to /home/user/"

def test_clean_logs_exists_and_utf8():
    """Test that clean_logs.csv exists and contains valid UTF-8"""
    clean_path = '/home/user/clean_logs.csv'
    assert os.path.isfile(clean_path), "clean_logs.csv is missing"

    try:
        with open(clean_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        assert False, "clean_logs.csv contains invalid UTF-8 characters"

def test_clean_logs_content():
    """Test the formatting and filtering in clean_logs.csv"""
    clean_path = '/home/user/clean_logs.csv'
    assert os.path.isfile(clean_path), "clean_logs.csv is missing"

    with open(clean_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 6, f"Expected exactly 6 lines (1 header + 5 rows), found {len(lines)}"

    header = lines[0]
    assert header == 'id,timestamp,status,message', "Header row is missing or incorrect"

    data_lines = lines[1:]

    # Check for embedded newlines (if there are 6 lines total, embedded newlines were likely removed)
    # Check date format and valid statuses
    valid_statuses = {'200', '301', '404', '500'}

    for line in data_lines:
        parts = line.split(',', 3)
        assert len(parts) == 4, f"Line does not have 4 columns: {line}"

        timestamp = parts[1]
        assert re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$', timestamp), f"Timestamp {timestamp} is not in YYYY-MM-DD HH:MM:SS format"

        status = parts[2]
        assert status in valid_statuses, f"Found invalid status {status} in clean_logs.csv"

        message = parts[3]
        assert message.startswith('"') and message.endswith('"'), f"Message field not properly quoted: {message}"
        assert '\n' not in message, "Embedded newline was not removed"

def test_status_counts():
    """Test the summary statistics file"""
    counts_path = '/home/user/status_counts.txt'
    assert os.path.isfile(counts_path), "status_counts.txt is missing"

    with open(counts_path, 'r', encoding='utf-8') as f:
        content = f.read().strip()

    expected = (
        "200: 2\n"
        "301: 1\n"
        "404: 1\n"
        "500: 1"
    )

    assert content == expected, f"status_counts.txt content is incorrect.\nExpected:\n{expected}\nGot:\n{content}"