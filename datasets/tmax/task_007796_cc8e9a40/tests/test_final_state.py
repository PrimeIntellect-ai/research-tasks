# test_final_state.py

import os
import pytest

def get_expected_output(fasta_path):
    with open(fasta_path, 'r') as f:
        lines = f.readlines()

    seqs = []
    current_seq = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('>'):
            if current_seq:
                seqs.append("".join(current_seq))
                current_seq = []
        else:
            current_seq.append(line)
    if current_seq:
        seqs.append("".join(current_seq))

    gc_contents = []
    for seq in seqs:
        gc = sum(1 for c in seq if c in 'GCgc')
        gc_contents.append(gc / len(seq) if len(seq) > 0 else 0)

    n = len(gc_contents)
    if n == 0:
        return ""

    sample_mean = sum(gc_contents) / n

    r = 42
    means = []
    for _ in range(1000):
        s = 0
        for _ in range(n):
            r = (r * 1103515245 + 12345) & 0x7FFFFFFF
            idx = r % n
            s += gc_contents[idx]
        means.append(s / n)
    means.sort()

    return f"Sample Mean: {sample_mean:.4f}\n95% CI: {means[25]:.4f} to {means[975]:.4f}"

def test_cpp_source_exists():
    assert os.path.isfile("/home/user/process_fasta.cpp"), "/home/user/process_fasta.cpp does not exist."

def test_cpp_executable_exists():
    assert os.path.isfile("/home/user/process_fasta"), "/home/user/process_fasta executable does not exist."
    assert os.access("/home/user/process_fasta", os.X_OK), "/home/user/process_fasta is not executable."

def test_gc_summary_output():
    fasta_path = "/home/user/data/input.fasta"
    summary_path = "/home/user/gc_summary.txt"

    assert os.path.isfile(summary_path), f"{summary_path} does not exist."

    expected_text = get_expected_output(fasta_path)

    with open(summary_path, 'r') as f:
        actual_text = f.read().strip()

    assert actual_text == expected_text, f"The contents of {summary_path} do not match the expected output.\nExpected:\n{expected_text}\nActual:\n{actual_text}"