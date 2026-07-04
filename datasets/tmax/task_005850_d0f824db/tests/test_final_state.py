# test_final_state.py

import os
import csv
import pytest

def test_c_program_exists():
    path = "/home/user/process_configs.c"
    assert os.path.exists(path), f"C program file {path} does not exist."
    assert os.path.isfile(path), f"Path {path} is not a file."

def test_report_files_generated_and_moved():
    csv_path = "/home/user/config_history.csv"
    assert os.path.exists(csv_path), f"Input file {csv_path} is missing."

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            pytest.fail("CSV file is empty.")

        dates = []
        data = {h: [] for h in headers[1:]}
        for row in reader:
            if not row:
                continue
            dates.append(row[0])
            for i, h in enumerate(headers[1:]):
                data[h].append(row[i+1])

    archive_dir = "/home/user/remote_archive"
    assert os.path.exists(archive_dir), f"Directory {archive_dir} does not exist."

    for server in headers[1:]:
        report_path = os.path.join(archive_dir, f"{server}.report")
        assert os.path.exists(report_path), f"Report file for {server} was not found at {report_path}."

        expected_lines = [
            f"REPORT FOR: {server}",
            "========================",
            "Update History:"
        ]
        for d, v in zip(dates, data[server]):
            expected_lines.append(f"- {d}: {v}")

        expected_content = "\n".join(expected_lines).strip()

        with open(report_path, 'r') as f:
            actual_content = f.read().strip()

        assert actual_content == expected_content, f"Content of {report_path} does not match the expected format or data."

def test_no_report_files_in_home():
    # Check that the report files were moved, not just copied
    csv_path = "/home/user/config_history.csv"
    if not os.path.exists(csv_path):
        return

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            return

    for server in headers[1:]:
        local_report_path = f"/home/user/{server}.report"
        # The prompt says "Transfer (copy or move)", so either is technically acceptable,
        # but usually transfer implies moving or it's fine if they are left. 
        # The prompt says "Transfer (copy or move)", so we shouldn't strictly fail if they are still there.
        pass