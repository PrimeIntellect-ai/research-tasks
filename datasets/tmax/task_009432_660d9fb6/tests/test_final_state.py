# test_final_state.py
import os
import csv

def test_c_source_file_exists():
    assert os.path.exists('/home/user/detect_spam.c'), "The C source file /home/user/detect_spam.c does not exist."

def test_executable_exists():
    assert os.path.exists('/home/user/detect_spam'), "The compiled executable /home/user/detect_spam does not exist."
    assert os.access('/home/user/detect_spam', os.X_OK), "The file /home/user/detect_spam is not executable."

def test_output_file_exists():
    assert os.path.exists('/home/user/suspicious_patterns.csv'), "The output file /home/user/suspicious_patterns.csv does not exist."

def test_output_file_content():
    expected_records = [
        ["2023-10-01T12:00:30Z", "U01", "U03", "1", "3"],
        ["2023-10-01T12:01:10Z", "U03", "U04", "1", "3"],
        ["2023-10-01T12:05:10Z", "U05", "U06", "2", "2"],
        ["2023-10-01T12:05:30Z", "U05", "U08", "1", "4"],
        ["2023-10-01T12:05:30Z", "U08", "U05", "0", "5"]
    ]

    actual_records = []
    with open('/home/user/suspicious_patterns.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # skip empty lines if any
                actual_records.append([col.strip() for col in row])

    assert len(actual_records) == len(expected_records), f"Expected {len(expected_records)} records in suspicious_patterns.csv, but found {len(actual_records)}."

    for i, (actual, expected) in enumerate(zip(actual_records, expected_records)):
        assert actual == expected, f"Record {i+1} mismatch. Expected: {','.join(expected)}, Actual: {','.join(actual)}"