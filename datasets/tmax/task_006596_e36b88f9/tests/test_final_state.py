# test_final_state.py

import os
import re
import pytest

def test_processed_logs_csv_correctness():
    config_log_path = "/home/user/config_log.txt"
    metadata_path = "/home/user/metadata.txt"
    output_csv_path = "/home/user/processed_logs.csv"

    assert os.path.exists(config_log_path), f"Missing {config_log_path}"
    assert os.path.exists(metadata_path), f"Missing {metadata_path}"
    assert os.path.exists(output_csv_path), f"Missing output file {output_csv_path}"

    # Read metadata
    metadata = {}
    with open(metadata_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) >= 2:
                metadata[parts[0]] = parts[1]

    expected_lines = []
    server_counts = {}

    # Process config log
    with open(config_log_path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) < 3:
                continue

            timestamp = parts[0]
            server_id = parts[1]
            raw_config = parts[2]

            # 1. Join
            email = metadata.get(server_id, "unknown@unknown.com")

            # 2. Masking
            if "@" in email:
                local_part, domain = email.split("@", 1)
                if len(local_part) > 0:
                    masked_email = f"{local_part[0]}*@{domain}"
                else:
                    masked_email = f"*@{domain}"
            else:
                masked_email = email

            # 3. Cleaning
            cleaned_config = re.sub(r'[^a-zA-Z0-9]', '', raw_config).lower()

            # 4. Rolling Statistic
            server_counts[server_id] = server_counts.get(server_id, 0) + 1
            cumulative_changes = server_counts[server_id]

            expected_lines.append(f"{timestamp},{server_id},{masked_email},{cleaned_config},{cumulative_changes}")

    # Read actual output
    with open(output_csv_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} rows in CSV, but got {len(actual_lines)}"

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, f"Row {i+1} mismatch.\nExpected: {expected}\nActual:   {actual}"

def test_c_program_exists():
    c_source_path = "/home/user/process_configs.c"
    c_exec_path = "/home/user/process_configs"

    assert os.path.exists(c_source_path), f"C source file missing at {c_source_path}"
    assert os.path.exists(c_exec_path), f"Compiled executable missing at {c_exec_path}"
    assert os.access(c_exec_path, os.X_OK), f"File {c_exec_path} is not executable"