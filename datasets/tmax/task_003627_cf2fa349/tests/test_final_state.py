# test_final_state.py

import os
import math
import pytest

def compute_expected_result():
    pdb_path = '/home/user/trajectory.pdb'
    fasta_path = '/home/user/sequence.fasta'

    # Read FASTA sequence
    with open(fasta_path, 'r') as f:
        lines = f.read().strip().split('\n')
        seq = "".join(line for line in lines if not line.startswith('>'))

    # Read PDB and extract CA coordinates
    models = []
    current_model = []
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith('MODEL'):
                current_model = []
            elif line.startswith('ATOM') and line[12:16].strip() == 'CA':
                res_seq = int(line[22:26].strip())
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())
                current_model.append((res_seq, x, y, z))
            elif line.startswith('ENDMDL'):
                models.append(current_model)

    # Group coordinates by residue sequence number
    res_coords = {}
    for model in models:
        for res_seq, x, y, z in model:
            if res_seq not in res_coords:
                res_coords[res_seq] = []
            res_coords[res_seq].append((x, y, z))

    # Compute RMSF for each CA atom
    max_rmsf = -1.0
    max_res = None

    for res_seq, coords in res_coords.items():
        N = len(coords)
        avg_x = sum(c[0] for c in coords) / N
        avg_y = sum(c[1] for c in coords) / N
        avg_z = sum(c[2] for c in coords) / N

        variance_sum = sum((c[0] - avg_x)**2 + (c[1] - avg_y)**2 + (c[2] - avg_z)**2 for c in coords)
        rmsf = math.sqrt(variance_sum / N)

        if rmsf > max_rmsf:
            max_rmsf = rmsf
            max_res = res_seq

    # Lookup the 1-letter amino acid code
    aa = seq[max_res - 1]

    return f"Residue: {max_res} ({aa}), Max_RMSF: {max_rmsf:.3f}"

def test_highest_fluctuation_file_exists():
    """Test that the output file was created at the correct location."""
    result_path = '/home/user/highest_fluctuation.txt'
    assert os.path.exists(result_path), f"The file {result_path} was not created."
    assert os.path.isfile(result_path), f"The path {result_path} exists but is not a file."

def test_highest_fluctuation_content():
    """Test that the output file contains the correctly computed result."""
    result_path = '/home/user/highest_fluctuation.txt'

    # Fail gracefully if file does not exist (caught by previous test, but prevents crash here)
    if not os.path.exists(result_path):
        pytest.fail(f"Cannot check content because {result_path} is missing.")

    expected_content = compute_expected_result()

    with open(result_path, 'r') as f:
        actual_content = f.read().strip()

    assert actual_content == expected_content, (
        f"The content of {result_path} is incorrect.\n"
        f"Expected: '{expected_content}'\n"
        f"Actual:   '{actual_content}'"
    )