# test_final_state.py
import os
import json
import pytest

def read_fasta(path):
    seqs = []
    with open(path, 'r') as f:
        seq = ""
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if seq:
                    seqs.append(seq)
                    seq = ""
            else:
                seq += line
        if seq:
            seqs.append(seq)
    return seqs

def compute_mismatches(ref, samples):
    counts = []
    for s in samples:
        counts.append(sum(1 for a, b in zip(ref, s) if a != b))
    return counts

def compute_posterior_mean(counts):
    alpha_prior = 2
    beta_prior = 1
    alpha_post = alpha_prior + sum(counts)
    beta_post = beta_prior + len(counts)
    return round(alpha_post / beta_post, 1)

def compute_longest_primer(ref, samples):
    max_len = 0
    best_primer = ""
    for i in range(len(ref)):
        for j in range(i + 1, len(ref) + 1):
            sub = ref[i:j]
            valid = True
            for s in samples:
                if s[i:j] != sub:
                    valid = False
                    break
            if valid:
                if (j - i) > max_len:
                    max_len = j - i
                    best_primer = sub
    return best_primer

def test_virtual_environment_exists():
    venv_python = "/home/user/bio_env/bin/python"
    assert os.path.isfile(venv_python) or os.path.isfile("/home/user/bio_env/bin/python3"), \
        "Python virtual environment was not found at /home/user/bio_env"

def test_analysis_result_json():
    json_path = "/home/user/analysis_result.json"
    assert os.path.isfile(json_path), f"{json_path} does not exist."

    with open(json_path, 'r') as f:
        try:
            result = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_path} is not a valid JSON file.")

    assert "mismatch_counts" in result, "Key 'mismatch_counts' missing from JSON."
    assert "mcmc_posterior_mean" in result, "Key 'mcmc_posterior_mean' missing from JSON."
    assert "conserved_primer" in result, "Key 'conserved_primer' missing from JSON."

    ref_seqs = read_fasta("/home/user/reference.fasta")
    assert len(ref_seqs) == 1, "Reference FASTA should contain exactly one sequence."
    ref = ref_seqs[0]

    samples = read_fasta("/home/user/samples.fasta")
    assert len(samples) > 0, "Samples FASTA must contain at least one sequence."

    expected_counts = compute_mismatches(ref, samples)
    expected_mean = compute_posterior_mean(expected_counts)
    expected_primer = compute_longest_primer(ref, samples)

    assert result["mismatch_counts"] == expected_counts, \
        f"Mismatch counts are incorrect. Expected {expected_counts}, got {result['mismatch_counts']}"

    assert result["mcmc_posterior_mean"] == expected_mean, \
        f"MCMC posterior mean is incorrect. Expected {expected_mean}, got {result['mcmc_posterior_mean']}"

    assert result["conserved_primer"] == expected_primer, \
        f"Conserved primer is incorrect. Expected '{expected_primer}', got '{result['conserved_primer']}'"