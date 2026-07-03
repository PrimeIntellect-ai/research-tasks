# test_final_state.py

import os
import csv
import math

def calculate_expected_data():
    primer = 'GATCGATCG'
    seqs = [
        "GATCGATCGAAT",
        "ATATATATATAT",
        "GCGCGCGCGCGC",
        "GATCGATCGGGC",
        "TTTTTTTTTTTT",
        "GATCGATC",
        "GATCGATCG",
        "CCCGGGCCCGGG"
    ]

    expected_csv = [["sequence", "gc_percentage", "group", "binding_score"]]
    group_a_scores = []
    group_b_scores = []

    for seq in seqs:
        # GC content
        gc_count = sum(1 for c in seq if c in 'GC')
        gc_percentage = (gc_count / len(seq)) * 100.0

        # Group
        group = 'A' if gc_percentage >= 50.0 else 'B'

        # Binding score
        if len(seq) < len(primer):
            max_m = 0
        else:
            max_m = 0
            for i in range(len(seq) - len(primer) + 1):
                window = seq[i:i+len(primer)]
                m = sum(1 for a, b in zip(window, primer) if a == b)
                if m > max_m:
                    max_m = m

        expected_csv.append([seq, f"{gc_percentage:.2f}", group, str(max_m)])

        if group == 'A':
            group_a_scores.append(max_m)
        else:
            group_b_scores.append(max_m)

    mean_a = sum(group_a_scores) / len(group_a_scores) if group_a_scores else 0.0
    mean_b = sum(group_b_scores) / len(group_b_scores) if group_b_scores else 0.0
    diff = abs(mean_a - mean_b) > 1.0

    expected_stats = [
        f"Mean Score A: {mean_a:.2f}",
        f"Mean Score B: {mean_b:.2f}",
        f"Significant Difference: {str(diff).lower()}"
    ]

    return expected_csv, expected_stats

def test_cpp_file_exists():
    assert os.path.isfile("/home/user/prepare_data.cpp"), "Source code file /home/user/prepare_data.cpp is missing."

def test_training_data_csv():
    csv_path = "/home/user/training_data.csv"
    assert os.path.isfile(csv_path), f"Output file {csv_path} is missing."

    expected_csv, _ = calculate_expected_data()

    with open(csv_path, 'r') as f:
        reader = csv.reader(f)
        actual_csv = list(reader)

    assert len(actual_csv) == len(expected_csv), f"Expected {len(expected_csv)} lines in CSV, got {len(actual_csv)}."

    for i, (actual_row, expected_row) in enumerate(zip(actual_csv, expected_csv)):
        assert actual_row == expected_row, f"Mismatch at CSV row {i+1}. Expected {expected_row}, got {actual_row}."

def test_stats_txt():
    stats_path = "/home/user/stats.txt"
    assert os.path.isfile(stats_path), f"Output file {stats_path} is missing."

    _, expected_stats = calculate_expected_data()

    with open(stats_path, 'r') as f:
        actual_stats = [line.strip() for line in f.readlines() if line.strip()]

    assert len(actual_stats) == len(expected_stats), f"Expected {len(expected_stats)} lines in stats.txt, got {len(actual_stats)}."

    for i, (actual_line, expected_line) in enumerate(zip(actual_stats, expected_stats)):
        assert actual_line.lower() == expected_line.lower(), f"Mismatch at stats.txt line {i+1}. Expected '{expected_line}', got '{actual_line}'."