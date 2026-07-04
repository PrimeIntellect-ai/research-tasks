# test_final_state.py
import os
import csv

def test_processed_changes_exists():
    output_file = "/home/user/processed_changes.csv"
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

def test_processed_changes_content():
    input_file = "/home/user/config_changes.csv"
    output_file = "/home/user/processed_changes.csv"

    assert os.path.isfile(input_file), f"Input file {input_file} is missing."
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

    expected_rows = []
    expected_header = ["timestamp", "masked_ip", "server_id", "config_key", "size_delta", "rolling_avg_delta"]

    with open(input_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        deltas = []
        for row in reader:
            if not row or not any(row.values()):
                continue

            timestamp = row["timestamp"]
            ip_parts = row["user_ip"].split(".")
            masked_ip = f"{ip_parts[0]}.{ip_parts[1]}.*.*"
            server_id = row["server_id"]
            config_key = row["config_key"]

            old_size = int(row["old_size_bytes"])
            new_size = int(row["new_size_bytes"])
            size_delta = new_size - old_size
            deltas.append(size_delta)

            window = deltas[-3:]
            rolling_avg = sum(window) / len(window)
            rolling_avg_str = f"{rolling_avg:.2f}"

            expected_rows.append([timestamp, masked_ip, server_id, config_key, str(size_delta), rolling_avg_str])

    with open(output_file, 'r', newline='') as f:
        reader = csv.reader(f)
        actual_data = list(reader)

    assert len(actual_data) > 0, "Output file is empty."
    assert actual_data[0] == expected_header, f"Expected header {expected_header}, but got {actual_data[0]}"

    # Remove empty rows at the end if any
    while actual_data and not any(actual_data[-1]):
        actual_data.pop()

    actual_rows = actual_data[1:]

    assert len(actual_rows) == len(expected_rows), f"Expected {len(expected_rows)} data rows, but got {len(actual_rows)}."

    for i, (actual, expected) in enumerate(zip(actual_rows, expected_rows)):
        assert actual == expected, f"Row {i+1} mismatch. Expected {expected}, but got {actual}."

def test_cpp_source_exists():
    cpp_file = "/home/user/process_configs.cpp"
    assert os.path.isfile(cpp_file), f"C++ source file {cpp_file} is missing."