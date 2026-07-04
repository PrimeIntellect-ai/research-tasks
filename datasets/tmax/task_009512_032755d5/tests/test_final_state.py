# test_final_state.py

import os
import re
import math

def test_final_state():
    """
    Validates the final state of the OS after the bioinformatics task is completed.
    Checks for the existence of the source code, executable, and the result file.
    Validates the contents of the result file with a small tolerance for floating point values.
    """
    c_source_path = "/home/user/analyze.c"
    executable_path = "/home/user/analyze"
    result_path = "/home/user/analysis_result.txt"

    assert os.path.exists(c_source_path), f"C source file missing: {c_source_path}"
    assert os.path.isfile(c_source_path), f"Path is not a file: {c_source_path}"

    assert os.path.exists(executable_path), f"Executable missing: {executable_path}"
    assert os.path.isfile(executable_path), f"Path is not a file: {executable_path}"
    assert os.access(executable_path, os.X_OK), f"Executable is not executable: {executable_path}"

    assert os.path.exists(result_path), f"Result file missing: {result_path}"
    assert os.path.isfile(result_path), f"Path is not a file: {result_path}"

    with open(result_path, 'r') as f:
        content = f.read().strip().split('\n')

    assert len(content) == 4, f"Expected exactly 4 lines in {result_path}, found {len(content)}"

    # Define expected values
    expected_seq1 = {'A': 0.200000, 'C': 0.300000, 'G': 0.400000, 'T': 0.100000}
    expected_seq2 = {'A': 0.400000, 'C': 0.100000, 'G': 0.200000, 'T': 0.300000}
    expected_db = 0.092010
    expected_k = 0.045981
    tolerance = 0.000002

    # Parse Line 1: Seq1 Dist
    seq1_match = re.match(r"Seq1 Dist:\s*A=([0-9.]+),\s*C=([0-9.]+),\s*G=([0-9.]+),\s*T=([0-9.]+)", content[0])
    assert seq1_match, f"Line 1 format incorrect: {content[0]}"
    seq1_vals = [float(x) for x in seq1_match.groups()]
    assert math.isclose(seq1_vals[0], expected_seq1['A'], abs_tol=tolerance), f"Seq1 A value incorrect: {seq1_vals[0]}"
    assert math.isclose(seq1_vals[1], expected_seq1['C'], abs_tol=tolerance), f"Seq1 C value incorrect: {seq1_vals[1]}"
    assert math.isclose(seq1_vals[2], expected_seq1['G'], abs_tol=tolerance), f"Seq1 G value incorrect: {seq1_vals[2]}"
    assert math.isclose(seq1_vals[3], expected_seq1['T'], abs_tol=tolerance), f"Seq1 T value incorrect: {seq1_vals[3]}"

    # Parse Line 2: Seq2 Dist
    seq2_match = re.match(r"Seq2 Dist:\s*A=([0-9.]+),\s*C=([0-9.]+),\s*G=([0-9.]+),\s*T=([0-9.]+)", content[1])
    assert seq2_match, f"Line 2 format incorrect: {content[1]}"
    seq2_vals = [float(x) for x in seq2_match.groups()]
    assert math.isclose(seq2_vals[0], expected_seq2['A'], abs_tol=tolerance), f"Seq2 A value incorrect: {seq2_vals[0]}"
    assert math.isclose(seq2_vals[1], expected_seq2['C'], abs_tol=tolerance), f"Seq2 C value incorrect: {seq2_vals[1]}"
    assert math.isclose(seq2_vals[2], expected_seq2['G'], abs_tol=tolerance), f"Seq2 G value incorrect: {seq2_vals[2]}"
    assert math.isclose(seq2_vals[3], expected_seq2['T'], abs_tol=tolerance), f"Seq2 T value incorrect: {seq2_vals[3]}"

    # Parse Line 3: Bhattacharyya Distance
    db_match = re.match(r"Bhattacharyya Distance:\s*([0-9.]+)", content[2])
    assert db_match, f"Line 3 format incorrect: {content[2]}"
    db_val = float(db_match.group(1))
    assert math.isclose(db_val, expected_db, abs_tol=tolerance), f"Bhattacharyya Distance incorrect: {db_val}"

    # Parse Line 4: Mutation Factor k
    k_match = re.match(r"Mutation Factor k:\s*([0-9.]+)", content[3])
    assert k_match, f"Line 4 format incorrect: {content[3]}"
    k_val = float(k_match.group(1))
    assert math.isclose(k_val, expected_k, abs_tol=tolerance), f"Mutation Factor k incorrect: {k_val}"