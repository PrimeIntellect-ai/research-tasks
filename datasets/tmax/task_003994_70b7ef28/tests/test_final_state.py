# test_final_state.py

import os

def parse_fasta(filepath):
    lengths = []
    gcs = []
    with open(filepath, 'r') as f:
        current_seq = []
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if current_seq:
                    seq = "".join(current_seq)
                    lengths.append(len(seq))
                    gc = sum(1 for c in seq if c in 'GCgc') / len(seq)
                    gcs.append(gc)
                current_seq = []
            else:
                current_seq.append(line)
        if current_seq:
            seq = "".join(current_seq)
            lengths.append(len(seq))
            gc = sum(1 for c in seq if c in 'GCgc') / len(seq)
            gcs.append(gc)
    return lengths, gcs

def test_variance_results():
    """Verify that the variance results are computed correctly and written to the exact format."""
    results_path = "/home/user/variance_results.txt"
    assert os.path.exists(results_path), f"{results_path} is missing."

    lengths, gcs = parse_fasta("/home/user/data.fasta")
    N = len(gcs)
    assert N > 1, "Need at least two sequences to compute sample variance."

    # Compute Naive variance
    sum_x = sum(gcs)
    sum_x2 = sum(x*x for x in gcs)
    naive_var = (sum_x2 - (sum_x*sum_x)/N) / (N - 1)

    # Compute Welford variance
    mean = 0.0
    M2 = 0.0
    for i, x in enumerate(gcs, 1):
        delta = x - mean
        mean += delta / i
        delta2 = x - mean
        M2 += delta * delta2
    welford_var = M2 / (N - 1)

    with open(results_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {results_path}, got {len(lines)}."

    expected_line1 = f"Total sequences: {N}"
    assert lines[0] == expected_line1, f"Line 1 incorrect. Expected '{expected_line1}', got '{lines[0]}'."

    expected_naive = f"Naive variance: {naive_var:.8f}"
    assert lines[1] == expected_naive, f"Line 2 incorrect. Expected '{expected_naive}', got '{lines[1]}'."

    expected_welford = f"Welford variance: {welford_var:.8f}"
    assert lines[2] == expected_welford, f"Line 3 incorrect. Expected '{expected_welford}', got '{lines[2]}'."

def test_histogram_results():
    """Verify that the histogram matches the actual sequence lengths."""
    histogram_path = "/home/user/histogram.txt"
    assert os.path.exists(histogram_path), f"{histogram_path} is missing."

    lengths, _ = parse_fasta("/home/user/data.fasta")
    bin1 = sum(1 for l in lengths if l <= 15)
    bin2 = sum(1 for l in lengths if 15 < l <= 25)
    bin3 = sum(1 for l in lengths if l > 25)

    expected_lines = [
        f"Bin 1: {'*' * bin1}",
        f"Bin 2: {'*' * bin2}",
        f"Bin 3: {'*' * bin3}"
    ]

    with open(histogram_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {histogram_path}, got {len(lines)}."

    for i in range(3):
        assert lines[i] == expected_lines[i], (
            f"Histogram line {i+1} incorrect.\n"
            f"Expected: '{expected_lines[i]}'\n"
            f"Got: '{lines[i]}'"
        )