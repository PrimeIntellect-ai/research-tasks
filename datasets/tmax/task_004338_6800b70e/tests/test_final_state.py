# test_final_state.py

import os
import json
import pytest

def get_reverse_complement(seq):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    return "".join(complement.get(base, base) for base in reversed(seq))

def compute_truth():
    fasta_path = "/home/user/aligned_sequences.fasta"
    if not os.path.exists(fasta_path):
        return None

    with open(fasta_path, "r") as f:
        lines = f.readlines()

    seqs = []
    current_seq = []
    for line in lines:
        line = line.strip()
        if line.startswith(">"):
            if current_seq:
                seqs.append("".join(current_seq).upper())
                current_seq = []
        else:
            current_seq.append(line)
    if current_seq:
        seqs.append("".join(current_seq).upper())

    if not seqs:
        return None

    seq_len = len(seqs[0])
    num_seqs = len(seqs)

    conserved = [False] * seq_len
    for i in range(seq_len):
        first_char = seqs[0][i]
        is_conserved = True
        for j in range(1, num_seqs):
            if seqs[j][i] != first_char:
                is_conserved = False
                break
        conserved[i] = is_conserved

    domains = []

    def refine(start, end):
        length = end - start
        cons_count = sum(conserved[start:end])
        ratio = cons_count / length

        if length <= 25 or ratio < 0.70:
            domains.append((start, end, ratio))
        else:
            mid = start + length // 2
            refine(start, mid)
            refine(mid, end)

    # Initial domains
    for start in range(0, seq_len, 200):
        refine(start, start + 200)

    num_final_domains = len(domains)

    candidates = [d for d in domains if (d[1] - d[0] == 25) and d[2] >= 0.90]

    if not candidates:
        return None

    forward_domain = min(candidates, key=lambda x: x[0])
    reverse_domain = max(candidates, key=lambda x: x[0])

    forward_primer = seqs[0][forward_domain[0]:forward_domain[1]]
    reverse_primer_fwd = seqs[0][reverse_domain[0]:reverse_domain[1]]
    reverse_primer = get_reverse_complement(reverse_primer_fwd)

    return {
        "num_final_domains": num_final_domains,
        "forward_primer": forward_primer,
        "reverse_primer": reverse_primer
    }

def test_json_results():
    """Test that analysis_results.json exists and contains the correct results."""
    json_path = "/home/user/analysis_results.json"
    assert os.path.exists(json_path), f"File {json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON.")

    truth = compute_truth()
    assert truth is not None, "Could not compute truth from FASTA."

    assert "num_final_domains" in results, "Missing 'num_final_domains' in JSON."
    assert "forward_primer" in results, "Missing 'forward_primer' in JSON."
    assert "reverse_primer" in results, "Missing 'reverse_primer' in JSON."

    assert results["num_final_domains"] == truth["num_final_domains"], \
        f"Expected num_final_domains={truth['num_final_domains']}, got {results['num_final_domains']}."

    assert results["forward_primer"] == truth["forward_primer"], \
        f"Expected forward_primer={truth['forward_primer']}, got {results['forward_primer']}."

    assert results["reverse_primer"] == truth["reverse_primer"], \
        f"Expected reverse_primer={truth['reverse_primer']}, got {results['reverse_primer']}."

def test_plot_exists():
    """Test that the conservation_mesh.png plot exists."""
    plot_path = "/home/user/conservation_mesh.png"
    assert os.path.exists(plot_path), f"Plot file {plot_path} does not exist."
    assert os.path.isfile(plot_path), f"Path {plot_path} is not a file."
    assert os.path.getsize(plot_path) > 0, f"Plot file {plot_path} is empty."