# test_final_state.py
import os
import json
import math
import pytest

def get_nucleotide_value(c):
    if c == 'A': return 10.0
    if c == 'C': return 20.0
    if c == 'G': return 30.0
    if c == 'T': return 40.0
    return 0.0

def calculate_population_variance(seq):
    vals = [get_nucleotide_value(c) for c in seq if c in 'ACGT']
    if not vals:
        return 0.0
    mean = sum(vals) / len(vals)
    var = sum((x - mean) ** 2 for x in vals) / len(vals)
    return var

def parse_fasta(filepath):
    seqs = {}
    with open(filepath, 'r') as f:
        seq_id = None
        seq_data = []
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith('>'):
                if seq_id is not None:
                    seqs[seq_id] = ''.join(seq_data)
                seq_id = line[1:]
                seq_data = []
            else:
                seq_data.append(line)
        if seq_id is not None:
            seqs[seq_id] = ''.join(seq_data)
    return seqs

def welch_t_test(var_a, var_b):
    n1 = len(var_a)
    n2 = len(var_b)
    m1 = sum(var_a) / n1
    m2 = sum(var_b) / n2

    # Sample variances (ddof=1)
    v1 = sum((x - m1)**2 for x in var_a) / (n1 - 1)
    v2 = sum((x - m2)**2 for x in var_b) / (n2 - 1)

    t_stat = (m1 - m2) / math.sqrt(v1/n1 + v2/n2)
    return t_stat

def test_executable_exists():
    """Test that the compiled executable exists."""
    exe_path = "/home/user/sequence_project/bin/analyze_seqs"
    assert os.path.isfile(exe_path), f"Compiled executable missing at {exe_path}"
    assert os.access(exe_path, os.X_OK), f"File at {exe_path} is not executable"

def test_csv_outputs_exist_and_correct():
    """Test that CSV outputs are generated and contain correct variances."""
    csv_a = "/home/user/sequence_project/data/cohort_A_results.csv"
    csv_b = "/home/user/sequence_project/data/cohort_B_results.csv"

    assert os.path.isfile(csv_a), f"Missing CSV output: {csv_a}"
    assert os.path.isfile(csv_b), f"Missing CSV output: {csv_b}"

    fasta_a = "/home/user/sequence_project/data/cohort_A.fasta"
    fasta_b = "/home/user/sequence_project/data/cohort_B.fasta"

    seqs_a = parse_fasta(fasta_a)
    seqs_b = parse_fasta(fasta_b)

    def check_csv(csv_path, seqs):
        with open(csv_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]

        assert len(lines) == len(seqs), f"Expected {len(seqs)} lines in {csv_path}, found {len(lines)}"

        for line in lines:
            parts = line.split(',')
            assert len(parts) == 2, f"Invalid CSV format in {csv_path}: {line}"
            seq_id, var_str = parts
            assert seq_id in seqs, f"Unknown sequence ID in CSV: {seq_id}"

            expected_var = calculate_population_variance(seqs[seq_id])
            actual_var = float(var_str)

            assert math.isclose(actual_var, expected_var, rel_tol=1e-4, abs_tol=1e-4), \
                f"Variance mismatch for {seq_id}: expected {expected_var}, got {actual_var}. Numerical instability might not be fixed."

    check_csv(csv_a, seqs_a)
    check_csv(csv_b, seqs_b)

def test_json_output_exists_and_correct():
    """Test that the final JSON results file is correct."""
    json_path = "/home/user/sequence_project/results.json"
    assert os.path.isfile(json_path), f"Missing JSON output: {json_path}"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Invalid JSON format in {json_path}")

    assert "t_statistic" in data, "Missing 't_statistic' in JSON"
    assert "p_value" in data, "Missing 'p_value' in JSON"

    fasta_a = "/home/user/sequence_project/data/cohort_A.fasta"
    fasta_b = "/home/user/sequence_project/data/cohort_B.fasta"

    seqs_a = parse_fasta(fasta_a)
    seqs_b = parse_fasta(fasta_b)

    var_a = [calculate_population_variance(seq) for seq in seqs_a.values()]
    var_b = [calculate_population_variance(seq) for seq in seqs_b.values()]

    expected_t_stat = welch_t_test(var_a, var_b)

    actual_t_stat = float(data["t_statistic"])
    actual_p_value = float(data["p_value"])

    assert math.isclose(actual_t_stat, expected_t_stat, rel_tol=1e-3, abs_tol=1e-3) or \
           math.isclose(actual_t_stat, -expected_t_stat, rel_tol=1e-3, abs_tol=1e-3), \
        f"t_statistic mismatch: expected {expected_t_stat}, got {actual_t_stat}"

    assert 0.0 <= actual_p_value <= 1.0, f"p_value out of valid range: {actual_p_value}"