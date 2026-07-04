# test_final_state.py

import os
import pytest

def test_etl_output_correctness():
    raw_file = "/home/user/raw_telemetry.txt"
    out_file = "/home/user/etl_output.csv"

    assert os.path.exists(out_file), f"Output file {out_file} is missing. Did you run the pipeline?"
    assert os.path.exists(raw_file), f"Raw file {raw_file} is missing. It should not have been deleted."

    # Read the raw file to compute the expected truth
    with open(raw_file, 'r', encoding='utf-8') as f:
        lines = f.read().strip().split('\n')

    records = []
    for line in lines:
        if not line.strip():
            continue
        parts = line.split(';')
        if len(parts) >= 4 and parts[1] == 'SENS_88':
            records.append({
                'ts': int(parts[0]),
                'temp': float(parts[2]),
                'notes': parts[3]
            })

    # Sort chronologically
    records.sort(key=lambda x: x['ts'])

    expected_lines = []
    temps = []
    for r in records:
        temps.append(r['temp'])
        if len(temps) > 3:
            temps.pop(0)
        avg = sum(temps) / len(temps)

        # Keep only printable ASCII characters (32 to 126 inclusive)
        cleaned_notes = ''.join(c for c in r['notes'] if 32 <= ord(c) <= 126)

        expected_lines.append(f"{r['ts']},{avg:.2f},{cleaned_notes}")

    # Read actual output
    with open(out_file, 'r', encoding='utf-8') as f:
        actual_content = f.read().strip()

    actual_lines = actual_content.split('\n') if actual_content else []

    assert len(actual_lines) == len(expected_lines), (
        f"Expected {len(expected_lines)} lines in {out_file}, but got {len(actual_lines)}."
    )

    for i, (actual, expected) in enumerate(zip(actual_lines, expected_lines)):
        assert actual == expected, (
            f"Mismatch at line {i+1} of {out_file}.\n"
            f"Expected: {expected}\n"
            f"Actual:   {actual}"
        )

def test_c_program_exists():
    c_source = "/home/user/processor.c"
    c_binary = "/home/user/processor"

    assert os.path.exists(c_source), f"C source file {c_source} is missing."
    assert os.path.exists(c_binary), f"Compiled C binary {c_binary} is missing."
    assert os.access(c_binary, os.X_OK), f"File {c_binary} is not executable."