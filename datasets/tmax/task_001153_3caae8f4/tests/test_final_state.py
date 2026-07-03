# test_final_state.py
import os
import math

def test_source_code_exists():
    assert os.path.exists('/home/user/analyze_dist.cpp'), "Source code /home/user/analyze_dist.cpp is missing"

def test_executable_exists():
    assert os.path.exists('/home/user/analyze_dist'), "Executable /home/user/analyze_dist is missing"
    assert os.access('/home/user/analyze_dist', os.X_OK), "Executable /home/user/analyze_dist is not executable"

def test_convergence_results():
    fasta_path = '/home/user/sequences.fasta'
    assert os.path.exists(fasta_path), f"{fasta_path} is missing"

    with open(fasta_path, 'r') as f:
        lines = f.readlines()

    seqs = []
    for line in lines:
        line = line.strip()
        if not line.startswith('>') and line:
            seqs.append(line)

    aas = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    valid_aas = set(aas)

    def calc_kl(n):
        counts = {aa: 0 for aa in aas}
        total = 0
        for s in seqs[:n]:
            for char in s:
                if char in valid_aas:
                    counts[char] += 1
                    total += 1

        kl = 0.0
        for aa in aas:
            if total > 0:
                p = counts[aa] / total
                q = 1.0 / 20.0
                if p > 0:
                    kl += p * math.log(p / q)
        return kl

    n_values = [100, 500, 1000, 2000]
    expected_kls = {n: calc_kl(n) for n in n_values}

    csv_path = '/home/user/convergence_results.csv'
    assert os.path.exists(csv_path), f"{csv_path} is missing"

    with open(csv_path, 'r') as f:
        csv_lines = [l.strip() for l in f.readlines() if l.strip()]

    assert len(csv_lines) == 5, f"Expected 5 lines in CSV (header + 4 rows), got {len(csv_lines)}"
    assert csv_lines[0] == "N,KL_Divergence", f"Expected header 'N,KL_Divergence', got '{csv_lines[0]}'"

    for i, n in enumerate(n_values):
        parts = csv_lines[i+1].split(',')
        assert len(parts) == 2, f"Expected 2 columns in row {i+1}, got {len(parts)}"
        assert parts[0] == str(n), f"Expected N={n} in row {i+1}, got {parts[0]}"

        try:
            actual_kl = float(parts[1])
        except ValueError:
            assert False, f"Could not parse KL_Divergence value '{parts[1]}' as float"

        expected_kl = expected_kls[n]
        assert abs(actual_kl - expected_kl) < 1e-5, f"Expected KL divergence for N={n} to be ~{expected_kl:.6f}, got {actual_kl}"

def test_hypothesis_file():
    hyp_path = '/home/user/hypothesis.txt'
    assert os.path.exists(hyp_path), f"{hyp_path} is missing"

    with open(hyp_path, 'r') as f:
        content = f.read().strip()

    assert content == "H1", f"Expected hypothesis.txt to contain 'H1', got '{content}'"