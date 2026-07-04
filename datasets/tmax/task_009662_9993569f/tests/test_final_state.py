# test_final_state.py

import os
import math
import pytest

def test_features_csv_exists():
    assert os.path.isfile("/home/user/features.csv"), "/home/user/features.csv does not exist."

def test_features_csv_content():
    data_file = "/home/user/data.txt"
    assert os.path.isfile(data_file), "Original data file /home/user/data.txt is missing."

    with open(data_file, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 2, "data.txt must have exactly 2 lines."

    sequence = lines[0]
    signals = [float(x) for x in lines[1].split(',')]

    primer = "ATGCGAT"
    idx = sequence.find(primer)
    assert idx != -1, f"Primer {primer} not found in sequence."

    payload_start = idx + len(primer)
    signal_start = payload_start * 10

    assert len(signals) >= signal_start + 50, "Not enough signal samples for the payload."
    extracted_signal = signals[signal_start:signal_start + 50]

    N = 50
    expected_rows = ["Bin,Magnitude"]
    for k in range(N):
        re = 0.0
        im = 0.0
        for n in range(N):
            angle = 2.0 * math.pi * k * n / N
            re += extracted_signal[n] * math.cos(angle)
            im -= extracted_signal[n] * math.sin(angle)
        mag = math.sqrt(re*re + im*im)
        expected_rows.append(f"{k},{mag:.4f}")

    expected_csv = "\n".join(expected_rows) + "\n"

    with open("/home/user/features.csv", 'r') as f:
        actual_csv = f.read()

    # Standardize line endings
    actual_csv_lines = [line.strip() for line in actual_csv.strip().split('\n')]
    expected_csv_lines = [line.strip() for line in expected_csv.strip().split('\n')]

    assert actual_csv_lines == expected_csv_lines, "The contents of features.csv do not match the expected DFT magnitudes."