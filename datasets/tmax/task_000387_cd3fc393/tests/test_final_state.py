# test_final_state.py

import os
import csv
import random
import subprocess
import pytest

def oracle_score_func(seq1, seq2):
    total = 0
    for i in range(len(seq1) - 2):
        kmer = seq1[i:i+3]
        if kmer in seq2:
            total += 3
    total -= abs(len(seq1) - len(seq2))
    return total

def test_fuzz_equivalence_score_py():
    agent_script = "/home/user/score.py"
    oracle_bin = "/app/bin/oracle_score"

    assert os.path.exists(agent_script), f"Agent script missing at {agent_script}"

    random.seed(42)
    chars = ['A', 'T', 'G', 'C']

    for _ in range(100):
        len1 = random.randint(10, 50)
        len2 = random.randint(10, 50)
        seq1 = "".join(random.choices(chars, k=len1))
        seq2 = "".join(random.choices(chars, k=len2))

        # Run oracle
        oracle_proc = subprocess.run(
            [oracle_bin, seq1, seq2],
            capture_output=True, text=True
        )
        assert oracle_proc.returncode == 0, "Oracle failed to execute"
        oracle_out = oracle_proc.stdout.strip()

        # Run agent
        agent_proc = subprocess.run(
            ["python3", agent_script, seq1, seq2],
            capture_output=True, text=True
        )
        assert agent_proc.returncode == 0, f"Agent script failed on inputs {seq1}, {seq2}. Stderr: {agent_proc.stderr}"
        agent_out = agent_proc.stdout.strip()

        assert oracle_out == agent_out, f"Mismatch on inputs:\nSeq1: {seq1}\nSeq2: {seq2}\nOracle: {oracle_out}\nAgent: {agent_out}"

def test_features_csv_correctness():
    features_csv = "/home/user/features.csv"
    assert os.path.exists(features_csv), f"Output file missing at {features_csv}"

    patient_reads_csv = "/app/patient_reads.csv"
    assert os.path.exists(patient_reads_csv), f"Input file missing at {patient_reads_csv}"

    ref_seq = "ATGCCGTAACTGG"

    # Compute expected
    data = {}
    read_ids = set()
    with open(patient_reads_csv, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            sid = row['sample_id']
            rid = row['read_id']
            seq = row['sequence']
            score = oracle_score_func(ref_seq, seq)

            if sid not in data:
                data[sid] = {}
            data[sid][rid] = score
            read_ids.add(rid)

    sorted_sids = sorted(data.keys())
    sorted_rids = sorted(list(read_ids))

    expected_rows = []
    header = ['sample_id'] + sorted_rids
    expected_rows.append(header)

    for sid in sorted_sids:
        row = [sid]
        for rid in sorted_rids:
            row.append(str(data[sid].get(rid, 0)))
        expected_rows.append(row)

    # Read actual
    actual_rows = []
    with open(features_csv, 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                actual_rows.append(row)

    assert actual_rows == expected_rows, f"Contents of {features_csv} do not match expected output.\nExpected: {expected_rows}\nActual: {actual_rows}"