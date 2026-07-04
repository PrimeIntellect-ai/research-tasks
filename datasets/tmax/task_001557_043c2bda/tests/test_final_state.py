# test_final_state.py

import os
import pytest

class LCG:
    def __init__(self):
        self.seed = 12345

    def get_rand(self):
        self.seed = (self.seed * 1103515245 + 12345) % 2147483648
        return self.seed / 2147483648.0

def compute_expected_mean_lcc():
    lcg = LCG()
    iterations = 10000
    p = 0.25

    # Based on the prefix rule (length >= 3) for the given FASTA:
    # Seq0: MKVLLAY, Seq1: MKVAXYZ, Seq3: MKVXYZZ, Seq7: MKVPPPO -> MKV
    # Seq2: MKAALPQ, Seq4: MKAXYAA, Seq8: MKAQQQQ -> MKA
    # Seq5: MLKVYYY, Seq6: MLKZZZZ, Seq9: MLKAAAA -> MLK
    cliques = [
        [0, 1, 3, 7],
        [2, 4, 8],
        [5, 6, 9]
    ]

    total_lcc = 0
    for _ in range(iterations):
        active = set()
        for i in range(10):
            r = lcg.get_rand()
            if r >= p:
                active.add(i)

        max_comp = 0
        for c in cliques:
            comp_size = sum(1 for node in c if node in active)
            if comp_size > max_comp:
                max_comp = comp_size
        total_lcc += max_comp

    return f"Mean LCC: {total_lcc / iterations:.4f}"

def test_c_source_code_exists():
    c_file = "/home/user/simulate.c"
    assert os.path.exists(c_file), f"The C source file {c_file} does not exist."
    assert os.path.isfile(c_file), f"{c_file} is not a regular file."

def test_executable_exists():
    exe_file = "/home/user/simulate"
    assert os.path.exists(exe_file), f"The executable {exe_file} does not exist. Did you compile the code?"
    assert os.path.isfile(exe_file), f"{exe_file} is not a regular file."
    assert os.access(exe_file, os.X_OK), f"The file {exe_file} is not executable."

def test_simulation_results():
    results_file = "/home/user/simulation_results.txt"
    assert os.path.exists(results_file), f"The results file {results_file} does not exist."
    assert os.path.isfile(results_file), f"{results_file} is not a regular file."

    with open(results_file, "r") as f:
        content = f.read().strip()

    expected_result = compute_expected_mean_lcc()
    assert content == expected_result, f"Expected '{expected_result}', but found '{content}' in {results_file}."