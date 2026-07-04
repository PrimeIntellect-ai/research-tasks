# test_final_state.py
import os
import math
import itertools

def parse_fasta(path):
    seqs = {}
    current_id = None
    current_seq = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if current_id:
                    seqs[current_id] = ''.join(current_seq)
                current_id = line[1:]
                current_seq = []
            else:
                current_seq.append(line)
        if current_id:
            seqs[current_id] = ''.join(current_seq)
    return seqs

def get_dist(seq):
    counts = { ''.join(a): 0 for a in itertools.product('ACGT', repeat=3) }
    for i in range(len(seq) - 2):
        kmer = seq[i:i+3]
        if kmer in counts:
            counts[kmer] += 1
    N = len(seq) - 2
    return {k: (c + 1) / (N + 64) for k, c in counts.items()}

def kl(p, q):
    return sum(p[k] * math.log2(p[k] / q[k]) for k in p)

def test_divergence_results():
    csv_path = "/home/user/divergence_results.csv"
    assert os.path.exists(csv_path), f"File {csv_path} is missing. The Go program should write its output here."

    fasta_path = "/home/user/sequences.fasta"
    assert os.path.exists(fasta_path), f"File {fasta_path} is missing."

    seqs = parse_fasta(fasta_path)
    assert "Reference" in seqs, "Reference sequence is missing from FASTA."

    ref_seq = seqs.pop("Reference")
    pref = get_dist(ref_seq)

    expected = {}
    for target_id, seq in seqs.items():
        p_target = get_dist(seq)
        expected[target_id] = kl(p_target, pref)

    with open(csv_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) > 0, "CSV file is empty."
    assert lines[0] == "SequenceID,KLDivergence", f"CSV header is incorrect. Expected 'SequenceID,KLDivergence', got '{lines[0]}'"

    parsed_results = {}
    for line in lines[1:]:
        parts = line.split(',')
        assert len(parts) == 2, f"Invalid CSV line: {line}"
        parsed_results[parts[0]] = float(parts[1])

    assert sorted(parsed_results.keys()) == sorted(expected.keys()), "Target IDs in CSV do not match the expected targets from FASTA."

    # Check alphabetical ordering
    keys_in_file = [line.split(',')[0] for line in lines[1:]]
    assert keys_in_file == sorted(keys_in_file), "CSV rows are not sorted alphabetically by SequenceID."

    for target_id in expected:
        expected_val = expected[target_id]
        actual_val = parsed_results[target_id]
        # Check formatting logic implicitly by comparing floats with a tolerance
        # The prompt asks to format to exactly 4 decimal places, which we can check by string inspection
        line_for_target = [line for line in lines[1:] if line.startswith(target_id + ',')][0]
        val_str = line_for_target.split(',')[1]
        assert '.' in val_str and len(val_str.split('.')[1]) == 4, f"Value for {target_id} is not formatted to exactly 4 decimal places: {val_str}"

        assert math.isclose(actual_val, expected_val, abs_tol=1e-4), f"KL divergence for {target_id} is incorrect. Expected ~{expected_val:.4f}, got {actual_val:.4f}"