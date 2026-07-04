# test_final_state.py

import os
import pytest

def test_filtered_reads():
    raw_file = "/home/user/dna_sim/raw_reads.dat"
    filtered_file = "/home/user/dna_sim/filtered_reads.txt"

    assert os.path.exists(filtered_file), "filtered_reads.txt is missing"

    expected_seqs = []
    with open(raw_file, "r") as f:
        lines = f.read().splitlines()
        for i in range(1, len(lines), 2):
            seq = lines[i]
            if seq.startswith("GATTACA"):
                expected_seqs.append(seq)

    with open(filtered_file, "r") as f:
        actual_seqs = f.read().splitlines()

    assert actual_seqs == expected_seqs, "filtered_reads.txt does not contain the correct sequences extracted from raw_reads.dat"

def test_sim_c_modified():
    sim_file = "/home/user/dna_sim/sim.c"
    assert os.path.exists(sim_file), "sim.c is missing"

    with open(sim_file, "r") as f:
        content = f.read()

    assert "#pragma omp" not in content, "OpenMP pragma was not removed from sim.c"
    assert "qsort" in content, "qsort was not used in sim.c as requested"

def test_final_scores():
    ref_file = "/home/user/dna_sim/reference.txt"
    scores_file = "/home/user/dna_sim/final_scores.txt"

    assert os.path.exists(scores_file), "final_scores.txt is missing"

    with open(ref_file, "r") as f:
        ref_lines = f.read().splitlines()

    with open(scores_file, "r") as f:
        scores_lines = f.read().splitlines()

    assert scores_lines == ref_lines, "final_scores.txt does not match the exact values in reference.txt"