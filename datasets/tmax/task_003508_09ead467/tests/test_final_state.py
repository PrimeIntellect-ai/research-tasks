# test_final_state.py

import os
import pytest

def expected_signature(line):
    s = sum(ord(c) for c in line)
    return f"{(s ^ 0x5A):04X}"

def test_final_trace_accuracy():
    final_log_path = '/home/user/final_trace.log'
    gold_lines_path = '/tmp/gold_lines.txt'

    assert os.path.exists(final_log_path), f"Output file missing: {final_log_path}"
    assert os.path.exists(gold_lines_path), f"Gold lines file missing: {gold_lines_path}"

    with open(final_log_path, 'r') as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    with open(gold_lines_path, 'r') as f:
        gold_lines = set(l.strip() for l in f.readlines())

    total_gold = len(gold_lines)
    assert total_gold > 0, "Gold lines file is empty."

    correct = 0

    for line in lines:
        if '|' not in line:
            continue
        content, sig = line.rsplit('|', 1)
        if content in gold_lines and sig == expected_signature(content):
            correct += 1
            gold_lines.remove(content) # Count each only once

    accuracy = correct / total_gold

    assert accuracy >= 0.90, f"Accuracy {accuracy:.2f} is below the threshold of 0.90. Correctly recovered and signed lines: {correct}/{total_gold}"