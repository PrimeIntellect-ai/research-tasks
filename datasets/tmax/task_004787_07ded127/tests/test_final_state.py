# test_final_state.py

import os
import pytest

def read_fasta(path):
    seqs = {}
    with open(path, "r") as f:
        curr_id = None
        curr_seq = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if curr_id:
                    seqs[curr_id] = "".join(curr_seq)
                curr_id = line[1:]
                curr_seq = []
            else:
                curr_seq.append(line)
        if curr_id:
            seqs[curr_id] = "".join(curr_seq)
    return seqs

def calc_sum(seq):
    return sum(abs(ord(a) - ord(b)) for a in seq for b in seq)

def test_analyze_go_exists_and_concurrent():
    go_file = "/home/user/analyze.go"
    assert os.path.isfile(go_file), f"Go source file {go_file} is missing."

    with open(go_file, "r") as f:
        content = f.read()

    assert "go " in content, "The Go program does not appear to use the 'go' keyword for goroutines."
    has_waitgroup = "sync.WaitGroup" in content
    has_chan = "chan " in content or "make(chan" in content
    assert has_waitgroup or has_chan, "The Go program does not appear to use sync.WaitGroup or channels for synchronization."

def test_summary_csv_correct():
    fasta_path = "/home/user/data/proteins.fasta"
    summary_path = "/home/user/summary.csv"

    assert os.path.isfile(fasta_path), f"FASTA file {fasta_path} is missing."
    assert os.path.isfile(summary_path), f"Output file {summary_path} is missing."

    seqs = read_fasta(fasta_path)
    expected_lines = []
    for seq_id in sorted(seqs.keys()):
        total_sum = calc_sum(seqs[seq_id])
        expected_lines.append(f"{seq_id},{total_sum}")

    with open(summary_path, "r") as f:
        actual_lines = [line.strip() for line in f if line.strip()]

    assert actual_lines == expected_lines, (
        f"The contents of {summary_path} do not match the expected output. "
        f"Expected:\n{chr(10).join(expected_lines)}\nActual:\n{chr(10).join(actual_lines)}"
    )