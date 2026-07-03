# test_final_state.py

import os
import math
import pytest

def test_bottleneck_txt():
    bottleneck_path = "/home/user/bottleneck.txt"
    assert os.path.isfile(bottleneck_path), f"Missing file: {bottleneck_path}"

    with open(bottleneck_path, "r") as f:
        content = f.read().strip()

    assert content == "compute_distances", f"Expected bottleneck function to be 'compute_distances', but got '{content}'"

def test_posterior_mean_txt():
    fasta_path = "/home/user/data.fasta"
    assert os.path.isfile(fasta_path), f"Missing file: {fasta_path}"

    # Read sequences
    sequences = []
    with open(fasta_path, 'r') as f:
        seq = ""
        for line in f:
            if line.startswith(">"):
                if seq: sequences.append(seq)
                seq = ""
            else:
                seq += line.strip()
        if seq: sequences.append(seq)

    n = len(sequences)
    L = len(sequences[0])

    # Compute distances
    distances = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1, n):
            d = sum(1 for a, b in zip(sequences[i], sequences[j]) if a != b)
            distances[i][j] = d
            distances[j][i] = d

    # MCMC with log-likelihood
    import random

    def log_likelihood(mu):
        ll = 0.0
        for i in range(n):
            for j in range(i+1, n):
                d = distances[i][j]
                ll += d * math.log(mu) + (L - d) * math.log(1 - mu)
        return ll

    # We need to use a deterministic random sequence identical to numpy's if possible.
    # Actually, the truth script uses numpy.random.
    # Since we can't use third-party libs like numpy in the test file per instructions,
    # wait, the instructions say "Use only the Python standard library and pytest (no third-party libs)."
    # But numpy is used in the truth and the task. If I can't use numpy, I can't exactly replicate numpy.random.normal.
    # So I will just check if the output matches the expected float 0.0768.

    posterior_path = "/home/user/posterior_mean.txt"
    assert os.path.isfile(posterior_path), f"Missing file: {posterior_path}"

    with open(posterior_path, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse float from {posterior_path}, content: '{content}'")

    # The expected value is 0.0768 based on the fixed numpy random seed
    assert math.isclose(val, 0.0768, abs_tol=1e-4), f"Expected posterior mean around 0.0768, got {val}"

def test_mcmc_mutations_modifications():
    script_path = "/home/user/mcmc_mutations.py"
    assert os.path.isfile(script_path), f"Missing file: {script_path}"

    with open(script_path, "r") as f:
        content = f.read()

    # Check that raw likelihood multiplication is gone
    assert "prob *= (mu**d) * ((1-mu)**(L-d))" not in content, "The script still contains the raw likelihood multiplication which causes underflow."

    # Check that log likelihood is used
    assert "np.log(" in content or "math.log(" in content, "The script does not seem to use log-likelihood."