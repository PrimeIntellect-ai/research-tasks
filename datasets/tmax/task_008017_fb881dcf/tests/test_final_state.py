# test_final_state.py

import os
import math

def parse_fasta(filepath):
    sequences = []
    current_seq = []
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith(">"):
                if current_seq:
                    sequences.append("".join(current_seq))
                    current_seq = []
            else:
                current_seq.append(line)
        if current_seq:
            sequences.append("".join(current_seq))
    return sequences

def test_smoothed_pwm_format_and_values():
    alignment_path = "/home/user/alignment.fasta"
    pwm_path = "/home/user/smoothed_pwm.txt"

    assert os.path.isfile(alignment_path), f"Missing {alignment_path}"
    assert os.path.isfile(pwm_path), f"Missing {pwm_path}"

    sequences = parse_fasta(alignment_path)
    assert len(sequences) > 0, "No sequences found in alignment.fasta"

    seq_len = len(sequences[0])
    N = len(sequences)

    aa_list = "A C D E F G H I K L M N P Q R S T V W Y".split()

    expected_pwm = []
    for i in range(seq_len):
        counts = {aa: 0 for aa in aa_list}
        for seq in sequences:
            if i < len(seq):
                aa = seq[i]
                if aa in counts:
                    counts[aa] += 1

        row_scores = []
        for aa in aa_list:
            p = (counts[aa] + 1) / (N + 20)
            score = math.log2(p / 0.05)
            row_scores.append(score)
        expected_pwm.append(row_scores)

    with open(pwm_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == seq_len, f"Expected {seq_len} rows in {pwm_path}, got {len(lines)}"

    for i, line in enumerate(lines):
        parts = line.split('\t')
        assert len(parts) == 21, f"Expected 21 columns in row {i+1}, got {len(parts)}"
        assert int(parts[0]) == i + 1, f"Expected row index {i+1}, got {parts[0]}"

        for j, expected_score in enumerate(expected_pwm[i]):
            actual_score = float(parts[j+1])
            assert abs(actual_score - expected_score) < 0.005, \
                f"Row {i+1}, AA {aa_list[j]}: expected {expected_score:.3f}, got {actual_score}"

def test_target_score():
    alignment_path = "/home/user/alignment.fasta"
    target_path = "/home/user/target.fasta"
    score_path = "/home/user/target_score.txt"

    assert os.path.isfile(alignment_path), f"Missing {alignment_path}"
    assert os.path.isfile(target_path), f"Missing {target_path}"
    assert os.path.isfile(score_path), f"Missing {score_path}"

    sequences = parse_fasta(alignment_path)
    target_seqs = parse_fasta(target_path)

    assert len(target_seqs) > 0, "No sequences found in target.fasta"
    target_seq = target_seqs[0]

    N = len(sequences)
    aa_list = "A C D E F G H I K L M N P Q R S T V W Y".split()

    expected_total_score = 0.0
    for i, aa in enumerate(target_seq):
        count = 0
        for seq in sequences:
            if i < len(seq) and seq[i] == aa:
                count += 1
        p = (count + 1) / (N + 20)
        score = math.log2(p / 0.05)
        expected_total_score += score

    with open(score_path, 'r') as f:
        content = f.read().strip()

    try:
        actual_score = float(content)
    except ValueError:
        assert False, f"Could not parse target score as float: {content}"

    assert abs(actual_score - expected_total_score) < 0.005, \
        f"Expected target score {expected_total_score:.3f}, got {actual_score}"