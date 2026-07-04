# test_final_state.py

import os
import pytest

def test_destination_directory_created():
    dest_dir = "/home/user/secure_vault/archive_2024"
    assert os.path.isdir(dest_dir), f"Destination directory {dest_dir} was not created."

def test_c_program_exists_and_uses_mmap():
    c_file = "/home/user/archiver.c"
    assert os.path.isfile(c_file), f"C source file {c_file} is missing."
    with open(c_file, 'r') as f:
        content = f.read()
    assert "mmap" in content, f"C program does not appear to use mmap as required."

def test_executable_exists():
    exe_file = "/home/user/archiver"
    assert os.path.isfile(exe_file), f"Executable {exe_file} is missing."
    assert os.access(exe_file, os.X_OK), f"{exe_file} is not executable."

def test_processed_data_content():
    processed_file = "/home/user/secure_vault/archive_2024/processed_data.txt"
    assert os.path.isfile(processed_file), f"Processed data file {processed_file} is missing."

    expected_lines = [
        "[KEEP] SYSTEM BOOT INITIATED AT 04:00.\n",
        "[KEEP] USER ADMIN LOGGED IN FROM 192.168.1.50.\n",
        "[KEEP] DATABASE BACKUP COMPLETED SUCCESSFULLY.\n",
        "[KEEP] WARNING: DISK SPACE ON /DEV/SDA1 IS AT 85.\n" if "85%" not in "[KEEP] WARNING: DISK SPACE ON /DEV/SDA1 IS AT 85%.\n" else "[KEEP] WARNING: DISK SPACE ON /DEV/SDA1 IS AT 85%.\n",
        "[KEEP] ERROR: FAILED TO WRITE TO SECTOR 7A.\n"
    ]

    with open(processed_file, 'r') as f:
        actual_lines = f.readlines()

    # Standardize line endings for comparison
    actual_lines = [line.strip() for line in actual_lines if line.strip()]
    expected_lines = [line.strip() for line in expected_lines if line.strip()]

    assert actual_lines == expected_lines, "The processed data does not match the expected uppercase [KEEP] lines."

def test_summary_log_content():
    summary_file = "/home/user/summary.log"
    assert os.path.isfile(summary_file), f"Summary log {summary_file} is missing."

    with open(summary_file, 'r') as f:
        content = f.read().strip()

    assert content == "Total archived: 5", f"Summary log content is incorrect. Expected 'Total archived: 5', got '{content}'."