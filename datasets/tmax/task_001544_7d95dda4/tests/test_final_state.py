# test_final_state.py
import os
import csv
import pytest

def parse_fasta(path):
    seqs = {}
    with open(path) as f:
        curr_id = None
        curr_seq = []
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if curr_id:
                    seqs[curr_id] = "".join(curr_seq)
                curr_id = line[1:]
                curr_seq = []
            else:
                curr_seq.append(line)
        if curr_id:
            seqs[curr_id] = "".join(curr_seq)
    return seqs

def get_bg(path):
    with open(path) as f:
        return "".join(l.strip() for l in f if not l.startswith(">"))

def revcomp(seq):
    comp = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}
    return "".join(comp.get(c, c) for c in reversed(seq))

def get_score(seq, bg):
    max_score = 0
    for i in range(len(bg) - len(seq)):
        score = sum(2 if seq[j] == bg[i+j] else -1 for j in range(len(seq)))
        if score > max_score: 
            max_score = score
    return max_score

def test_optimized_primers():
    csv_path = "/home/user/optimized_primers.csv"
    targets_path = "/home/user/targets.fasta"
    bg_path = "/home/user/background.fasta"

    assert os.path.isfile(csv_path), f"Output file missing: {csv_path}"
    assert os.path.isfile(targets_path), f"Targets file missing: {targets_path}"
    assert os.path.isfile(bg_path), f"Background file missing: {bg_path}"

    targets = parse_fasta(targets_path)
    bg = get_bg(bg_path)

    total_score = 0
    count = 0

    with open(csv_path) as f:
        reader = csv.DictReader(f)
        assert "Target_ID" in reader.fieldnames, "Missing Target_ID column"
        assert "Forward_Primer" in reader.fieldnames, "Missing Forward_Primer column"
        assert "Reverse_Primer" in reader.fieldnames, "Missing Reverse_Primer column"

        for row in reader:
            tid = row['Target_ID']
            fwd = row['Forward_Primer']
            rev = row['Reverse_Primer']

            assert tid in targets, f"Unknown Target_ID in CSV: {tid}"
            target = targets[tid]

            assert len(fwd) == 20, f"Forward primer for {tid} is not 20bp"
            assert len(rev) == 20, f"Reverse primer for {tid} is not 20bp"

            assert fwd in target[:40], f"Forward primer for {tid} is not a valid substring of the first 40bp"
            assert revcomp(rev) in target[60:], f"Reverse primer for {tid} is not a valid reverse complement of the last 40bp"

            total_score += get_score(fwd, bg)
            total_score += get_score(rev, bg)
            count += 2

    assert count == 10, f"Expected 10 primers (5 targets * 2), found {count}"
    assert total_score <= 180, f"Total off-target score {total_score} exceeds threshold of 180"