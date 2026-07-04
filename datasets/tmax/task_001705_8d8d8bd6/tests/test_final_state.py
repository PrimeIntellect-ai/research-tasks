# test_final_state.py

import os
import struct
import re

def parse_logs_bin(filepath):
    records = []
    with open(filepath, 'rb') as f:
        while True:
            header = f.read(11)
            if not header:
                break
            if len(header) < 11:
                break
            ts, enc, msg_len = struct.unpack('<QBH', header)
            msg_bytes = f.read(msg_len)
            if enc == 1:
                # UTF-16LE, ascii range only as per spec
                msg = msg_bytes.decode('utf-16le')
            else:
                msg = msg_bytes.decode('utf-8')
            records.append((ts, msg))
    return records

def compute_expected_csv(records):
    if not records:
        return "Timestamp,Event_Type,Message\n"

    accepted = []
    last_msg = None
    for ts, msg in records:
        if msg != last_msg:
            accepted.append((ts, msg))
            last_msg = msg

    t_start = records[0][0]
    t_end = records[-1][0]
    num_buckets = ((t_end - t_start) // 60) + 1

    buckets = [None] * num_buckets
    for ts, msg in accepted:
        idx = (ts - t_start) // 60
        if 0 <= idx < num_buckets:
            if buckets[idx] is None:
                buckets[idx] = (ts, msg)

    expected_lines = ["Timestamp,Event_Type,Message"]
    for i in range(num_buckets):
        bucket_ts = t_start + i * 60
        if buckets[i] is None:
            expected_lines.append(f"{bucket_ts},GAP,MISSING")
        else:
            msg = buckets[i][1]
            event_type = msg.split(' ')[0] if ' ' in msg else msg
            expected_lines.append(f"{bucket_ts},{event_type},{msg}")

    return "\n".join(expected_lines) + "\n"

def test_c_program_exists():
    assert os.path.exists("/home/user/process_logs.c"), "process_logs.c is missing."

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.exists(script_path), "run_pipeline.sh is missing."
    assert os.access(script_path, os.X_OK), "run_pipeline.sh is not executable."

def test_crontab_content():
    crontab_path = "/home/user/crontab.txt"
    assert os.path.exists(crontab_path), "crontab.txt is missing."

    with open(crontab_path, 'r') as f:
        content = f.read().strip()

    pattern = r'^\*/5\s+\*\s+\*\s+\*\s+\*\s+(?:/bin/(?:bash|sh)\s+)?/home/user/run_pipeline\.sh$'
    assert re.match(pattern, content), f"crontab.txt content '{content}' does not match expected schedule for run_pipeline.sh."

def test_output_csv_correctness():
    bin_path = "/home/user/logs.bin"
    csv_path = "/home/user/output.csv"

    assert os.path.exists(csv_path), "output.csv is missing."

    records = parse_logs_bin(bin_path)
    expected_csv = compute_expected_csv(records)

    with open(csv_path, 'r') as f:
        actual_csv = f.read()

    # Normalize line endings
    actual_csv = actual_csv.replace('\r\n', '\n').strip() + '\n'
    expected_csv = expected_csv.replace('\r\n', '\n').strip() + '\n'

    assert actual_csv == expected_csv, "output.csv does not match the expected processed log data."