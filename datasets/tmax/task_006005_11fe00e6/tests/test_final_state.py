# test_final_state.py

import os
import re
import datetime
import pytest

def parse_timestamp(ts_str):
    if ts_str.isdigit():
        dt = datetime.datetime.fromtimestamp(int(ts_str), tz=datetime.timezone.utc)
    else:
        # Parse ISO8601 like 2023-10-01T00:05:00Z
        ts_str = ts_str.replace('Z', '+00:00')
        dt = datetime.datetime.fromisoformat(ts_str)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def compute_expected_sql(raw_logs_path):
    with open(raw_logs_path, 'r') as f:
        lines = f.read().strip().split('\n')

    sql_lines = []
    for line in lines:
        if not line.strip():
            continue
        parts = line.strip().split()
        ts_str = parts[0]
        server = parts[1]

        metrics = {}
        for part in parts[2:]:
            k, v = part.split(':')
            metrics[k] = float(v)

        is_anomaly = 1 if metrics.get('cpu', 0) > 90.0 and metrics.get('mem', 0) > 90.0 else 0

        norm_time = parse_timestamp(ts_str)

        for metric_name in ['cpu', 'mem', 'disk']:
            if metric_name in metrics:
                val = metrics[metric_name]
                sql = f"INSERT INTO metrics (log_time, server, metric_name, metric_value, anomaly_flag) VALUES ('{norm_time}', '{server}', '{metric_name}', {val:.1f}, {is_anomaly});"
                sql_lines.append(sql)

    return sql_lines

def test_etl_output_exists_and_correct():
    raw_logs_path = "/home/user/raw_logs.txt"
    output_path = "/home/user/etl_output.sql"

    assert os.path.exists(raw_logs_path), f"Input file {raw_logs_path} is missing."
    assert os.path.exists(output_path), f"Output file {output_path} is missing. Did you run your ETL processor?"

    expected_lines = compute_expected_sql(raw_logs_path)

    with open(output_path, 'r') as f:
        actual_content = f.read().strip()

    actual_lines = [line.strip() for line in actual_content.split('\n') if line.strip()]

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} SQL statements, but found {len(actual_lines)}."

    for i, (expected, actual) in enumerate(zip(expected_lines, actual_lines)):
        assert actual == expected, f"Mismatch at line {i+1}.\nExpected: {expected}\nActual:   {actual}"

def test_c_source_and_binary_exist():
    source_path = "/home/user/etl_processor.c"
    binary_path = "/home/user/etl_processor"

    assert os.path.exists(source_path), f"C source file {source_path} is missing."
    assert os.path.exists(binary_path), f"Compiled binary {binary_path} is missing."
    assert os.access(binary_path, os.X_OK), f"File {binary_path} is not executable."