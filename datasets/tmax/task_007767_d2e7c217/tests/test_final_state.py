# test_final_state.py

import os
import csv
from datetime import datetime

def test_clean_metrics_exists():
    assert os.path.isfile('/home/user/clean_metrics.csv'), "The output file /home/user/clean_metrics.csv does not exist."

def test_clean_metrics_content():
    raw_file = '/home/user/raw_metrics.csv'
    assert os.path.isfile(raw_file), f"Raw metrics file {raw_file} is missing."

    # Read and parse raw data
    with open(raw_file, 'r', newline='') as f:
        reader = csv.DictReader(f)
        raw_data = list(reader)

    # Process data to derive expected output
    processed = []
    for row in raw_data:
        # Timestamp alignment
        ts = datetime.strptime(row['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
        aligned = ts.strftime('%Y-%m-%d %H:%M:00')

        # CPU parsing
        cpu = float(row['cpu_percent'])

        # Memory normalization
        mem_str = row['memory_usage'].strip().upper()
        if mem_str.endswith('GB'):
            mem = float(mem_str[:-2]) * 1024
        elif mem_str.endswith('MB'):
            mem = float(mem_str[:-2])
        elif mem_str.endswith('KB'):
            mem = float(mem_str[:-2]) / 1024
        else:
            mem = float(mem_str)

        processed.append({
            'aligned_minute': aligned,
            'cpu_percent': cpu,
            'memory_mb': mem
        })

    # Sort chronologically
    processed.sort(key=lambda x: x['aligned_minute'])

    # Calculate rolling 3-row average for CPU
    for i in range(len(processed)):
        start_idx = max(0, i - 2)
        window = [x['cpu_percent'] for x in processed[start_idx:i+1]]
        processed[i]['rolling_cpu_3m'] = sum(window) / len(window)

    # Read actual output data
    out_file = '/home/user/clean_metrics.csv'
    with open(out_file, 'r', newline='') as f:
        reader = csv.reader(f)
        try:
            headers = next(reader)
        except StopIteration:
            assert False, f"{out_file} is empty."
        out_data = list(reader)

    expected_headers = ['aligned_minute', 'cpu_percent', 'memory_mb', 'rolling_cpu_3m']
    assert headers == expected_headers, f"Header row is incorrect. Expected {expected_headers}, got {headers}."

    assert len(out_data) == len(processed), f"Number of rows in output ({len(out_data)}) does not match expected ({len(processed)})."

    for i, (out_row, exp_row) in enumerate(zip(out_data, processed)):
        assert len(out_row) == 4, f"Row {i+1} does not have exactly 4 columns."

        expected_aligned = exp_row['aligned_minute']
        expected_cpu = f"{exp_row['cpu_percent']:.2f}"
        expected_mem = f"{exp_row['memory_mb']:.2f}"
        expected_rolling = f"{exp_row['rolling_cpu_3m']:.2f}"

        assert out_row[0] == expected_aligned, f"Row {i+1}: Aligned minute mismatch. Expected {expected_aligned}, got {out_row[0]}."
        assert out_row[1] == expected_cpu, f"Row {i+1}: CPU percent mismatch or formatting error. Expected {expected_cpu}, got {out_row[1]}."
        assert out_row[2] == expected_mem, f"Row {i+1}: Memory MB mismatch or formatting error. Expected {expected_mem}, got {out_row[2]}."
        assert out_row[3] == expected_rolling, f"Row {i+1}: Rolling CPU mismatch or formatting error. Expected {expected_rolling}, got {out_row[3]}."