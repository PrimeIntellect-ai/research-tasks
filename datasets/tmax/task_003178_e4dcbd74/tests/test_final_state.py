# test_final_state.py

import os
import re
import pytest

def compute_gc_content(fasta_path):
    sequences = []
    current_seq = []
    with open(fasta_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if current_seq:
                    sequences.append("".join(current_seq))
                    current_seq = []
            else:
                current_seq.append(line)
        if current_seq:
            sequences.append("".join(current_seq))

    gc_percentages = []
    for seq in sequences:
        total = sum(1 for c in seq if c.isalpha())
        gc = sum(1 for c in seq if c in 'GCgc')
        if total > 0:
            gc_percentages.append(100.0 * gc / total)

    if not gc_percentages:
        return 0.0
    return sum(gc_percentages) / len(gc_percentages)

def test_executable_exists_and_compiled():
    executable_path = "/home/user/fasta_stats"
    assert os.path.isfile(executable_path), f"Executable {executable_path} is missing."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_analysis_report_content():
    report_path = "/home/user/analysis_report.txt"
    assert os.path.isfile(report_path), f"File {report_path} is missing."

    group_a_path = "/home/user/groupA.fasta"
    group_b_path = "/home/user/groupB.fasta"

    mean_a = compute_gc_content(group_a_path)
    mean_b = compute_gc_content(group_b_path)

    abs_diff = abs(mean_a - mean_b)
    higher_group = "GroupA" if mean_a > mean_b else "GroupB"

    expected_content = (
        f"Mean_GroupA: {mean_a:.2f}\n"
        f"Mean_GroupB: {mean_b:.2f}\n"
        f"Absolute_Difference: {abs_diff:.2f}\n"
        f"Higher_Group: {higher_group}\n"
    )

    with open(report_path, "r") as f:
        actual_content = f.read().strip()

    expected_lines = expected_content.strip().split('\n')
    actual_lines = actual_content.split('\n')

    assert len(actual_lines) == len(expected_lines), f"Expected {len(expected_lines)} lines in {report_path}, but found {len(actual_lines)}."

    for i, (expected, actual) in enumerate(zip(expected_lines, actual_lines)):
        assert actual.strip() == expected.strip(), f"Line {i+1} mismatch in {report_path}.\nExpected: {expected}\nGot: {actual}"