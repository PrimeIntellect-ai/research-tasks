# test_final_state.py

import os
import math
from collections import Counter

def test_analyze_cpp_exists():
    path = "/home/user/analyze.cpp"
    assert os.path.exists(path), f"Source file {path} is missing."
    assert os.path.isfile(path), f"{path} is not a file."

def test_analyze_executable_exists():
    path = "/home/user/analyze"
    assert os.path.exists(path), f"Executable {path} is missing. Did you compile the code?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_result_txt_content():
    fasta_path = "/home/user/sequences.fasta"
    pdb_path = "/home/user/structure.pdb"
    result_path = "/home/user/result.txt"

    assert os.path.exists(result_path), f"Result file {result_path} is missing."

    # Standard amino acids
    std_aa_1 = set("ARNDCQEGHILKMFPSTWYV")
    std_aa_3_to_1 = {
        "ALA": "A", "ARG": "R", "ASN": "N", "ASP": "D", "CYS": "C",
        "GLN": "Q", "GLU": "E", "GLY": "G", "HIS": "H", "ILE": "I",
        "LEU": "L", "LYS": "K", "MET": "M", "PHE": "F", "PRO": "P",
        "SER": "S", "THR": "T", "TRP": "W", "TYR": "Y", "VAL": "V"
    }

    # Parse FASTA
    fasta_counts = Counter()
    with open(fasta_path, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                continue
            for char in line:
                if char in std_aa_1:
                    fasta_counts[char] += 1

    total_fasta = sum(fasta_counts.values())
    P = {aa: (fasta_counts[aa] / total_fasta if total_fasta > 0 else 0.0) for aa in std_aa_1}

    # Parse PDB
    pdb_counts = Counter()
    with open(pdb_path, "r") as f:
        for line in f:
            if line.startswith("ATOM"):
                atom_name = line[12:16].strip()
                if atom_name == "CA":
                    res_name = line[17:20].strip()
                    if res_name in std_aa_3_to_1:
                        pdb_counts[std_aa_3_to_1[res_name]] += 1

    total_pdb = sum(pdb_counts.values())
    Q = {aa: (pdb_counts[aa] / total_pdb if total_pdb > 0 else 0.0) for aa in std_aa_1}

    # Calculate TVD
    tvd = 0.5 * sum(abs(P[aa] - Q[aa]) for aa in std_aa_1)
    expected_result = f"{tvd:.4f}"

    # Read actual result
    with open(result_path, "r") as f:
        actual_result = f.read().strip()

    assert actual_result == expected_result, f"Expected TVD {expected_result} in {result_path}, but got {actual_result}"