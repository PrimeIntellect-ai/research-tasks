# test_final_state.py
import os
import pytest

def test_files_exist():
    """Verify that all required output files exist."""
    assert os.path.isfile('/home/user/gc_bootstrap.tsv'), "Output file /home/user/gc_bootstrap.tsv is missing."
    assert os.path.isfile('/home/user/plot.gp'), "Gnuplot script /home/user/plot.gp is missing."
    assert os.path.isfile('/home/user/gc_plot.png'), "Plot image /home/user/gc_plot.png is missing."

def test_gc_bootstrap_values():
    """Verify the mathematical correctness of gc_bootstrap.tsv using the exact LCG logic."""
    fasta_path = '/home/user/sequences.fasta'
    assert os.path.isfile(fasta_path), f"File {fasta_path} does not exist."

    seqs = []
    with open(fasta_path, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('>'):
                seqs.append(line)

    assert len(seqs) == 50, f"Expected 50 sequences, found {len(seqs)}."

    # LCG setup
    seed = 42
    def get_rand_idx():
        nonlocal seed
        seed = (seed * 1103515245 + 12345) % 2147483648
        return int((seed / 2147483648) * 50) + 1

    expected_results = []
    for pos in range(91):
        gc_fracs = []
        for seq in seqs:
            window = seq[pos:pos+10]
            gc_count = window.count('G') + window.count('C')
            gc_fracs.append(gc_count / 10.0)

        true_mean = sum(gc_fracs) / len(gc_fracs)

        boot_means = []
        for _ in range(100):
            sample_sum = 0.0
            for _ in range(50):
                idx = get_rand_idx() - 1  # 1-based to 0-based
                sample_sum += gc_fracs[idx]
            boot_means.append(sample_sum / 50.0)

        boot_means.sort()
        lower_ci = boot_means[2]   # 3rd value (1-based) -> index 2
        upper_ci = boot_means[97]  # 98th value (1-based) -> index 97

        expected_results.append((pos + 1, true_mean, lower_ci, upper_ci))

    tsv_path = '/home/user/gc_bootstrap.tsv'
    with open(tsv_path, 'r') as f:
        lines = [line.strip().split('\t') for line in f if line.strip()]

    assert len(lines) == 91, f"Expected 91 lines in {tsv_path}, but found {len(lines)}."

    for i, (line, exp) in enumerate(zip(lines, expected_results)):
        assert len(line) == 4, f"Line {i+1} in {tsv_path} does not have exactly 4 columns."
        pos, mean, lower, upper = map(float, line)

        exp_pos, exp_mean, exp_lower, exp_upper = exp

        assert int(pos) == exp_pos, f"Line {i+1}: Expected Position {exp_pos}, got {pos}."
        assert abs(mean - exp_mean) <= 0.0002, f"Line {i+1}: Expected Mean {exp_mean:.4f}, got {mean:.4f}."
        assert abs(lower - exp_lower) <= 0.0002, f"Line {i+1}: Expected LowerCI {exp_lower:.4f}, got {lower:.4f}."
        assert abs(upper - exp_upper) <= 0.0002, f"Line {i+1}: Expected UpperCI {exp_upper:.4f}, got {upper:.4f}."