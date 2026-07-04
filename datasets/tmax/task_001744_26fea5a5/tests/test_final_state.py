# test_final_state.py

import os
import sqlite3
import pytest

def test_result_file_exists():
    result_file = "/home/user/ticket_4092/result.txt"
    assert os.path.isfile(result_file), f"Expected output file {result_file} is missing. Did you run the script?"

def test_result_file_content():
    # Recompute the expected result logically based on the setup
    db_path = "/home/user/ticket_4092/records.db"
    input_list = "/home/user/ticket_4092/input_files.txt"
    result_file = "/home/user/ticket_4092/result.txt"

    assert os.path.isfile(db_path), f"Database {db_path} is missing."
    assert os.path.isfile(input_list), f"Input list {input_list} is missing."

    # Read input files
    with open(input_list, 'r') as f:
        filenames = [line.strip() for line in f if line.strip()]

    # Query database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    values = []
    for filename in filenames:
        cursor.execute("SELECT value FROM measurements WHERE filename = ?", (filename,))
        row = cursor.fetchone()
        if row:
            values.append(row[0])

    conn.close()

    # Calculate expected moving average (window size = 3)
    window_size = 3
    expected_m_avg = []
    if len(values) >= window_size:
        for i in range(len(values) - window_size + 1):
            window = values[i:i+window_size]
            expected_m_avg.append(sum(window) / window_size)

    expected_output = ",".join(f"{x:.2f}" for x in expected_m_avg) + "\n"

    # Read actual result
    with open(result_file, 'r') as f:
        actual_output = f.read()

    assert actual_output == expected_output, (
        f"The content of {result_file} is incorrect.\n"
        f"Expected: {repr(expected_output)}\n"
        f"Actual:   {repr(actual_output)}\n"
        "Ensure the environment variable, the file parsing logic, and the moving average logic are all fixed."
    )