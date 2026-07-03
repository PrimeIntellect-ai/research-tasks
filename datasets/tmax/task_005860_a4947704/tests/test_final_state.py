# test_final_state.py
import os
import re
import csv
from collections import defaultdict

def test_user_features_csv_correctness():
    log_file_path = "/home/user/etl_dump.log"
    output_file_path = "/home/user/user_features.csv"

    assert os.path.exists(output_file_path), f"Output file {output_file_path} is missing."
    assert os.path.isfile(output_file_path), f"{output_file_path} is not a file."

    seen = set()
    user_data = defaultdict(lambda: {"total_purchase_amount": 0, "ips": set()})

    data_pattern = re.compile(r'DATA=\{action:\s*"([^"]*)",\s*amount:\s*"([^"]*)",\s*ip:\s*"([^"]*)"\}')

    with open(log_file_path, "r", encoding="utf-8") as f:
        for line in f:
            parts = [p.strip() for p in line.split("|", 3)]
            if len(parts) < 4:
                continue

            user_id = parts[2]
            raw_payload = parts[3]

            dup_key = (user_id, raw_payload)
            if dup_key in seen:
                continue
            seen.add(dup_key)

            match = data_pattern.search(raw_payload)
            if match:
                action = match.group(1).lower()
                amount = int(match.group(2))
                ip = match.group(3)

                if action == "purchase":
                    user_data[user_id]["total_purchase_amount"] += amount
                user_data[user_id]["ips"].add(ip)

    expected_rows = []
    for user_id in sorted(user_data.keys()):
        amount = user_data[user_id]["total_purchase_amount"]
        ips = ";".join(sorted(list(user_data[user_id]["ips"])))
        expected_rows.append([user_id, str(amount), ips])

    actual_rows = []
    with open(output_file_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ["user_id", "total_purchase_amount", "unique_ips"], f"Invalid header in {output_file_path}"
        for row in reader:
            if row:
                actual_rows.append(row)

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} rows, but got {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, got {actual}."

def test_cpp_file_exists():
    cpp_file = "/home/user/process_logs.cpp"
    assert os.path.exists(cpp_file), f"Source file {cpp_file} is missing."