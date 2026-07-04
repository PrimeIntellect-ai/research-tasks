# test_final_state.py

import os
import csv
import pytest

def solve_3x3(M, y):
    """Solves a 3x3 linear system using Cramer's rule."""
    def det(A):
        return (A[0][0] * (A[1][1] * A[2][2] - A[1][2] * A[2][1]) -
                A[0][1] * (A[1][0] * A[2][2] - A[1][2] * A[2][0]) +
                A[0][2] * (A[1][0] * A[2][1] - A[1][1] * A[2][0]))

    d = det(M)
    if d == 0:
        raise ValueError("Determinant is zero, singular matrix.")

    M0 = [[y[i] if j == 0 else M[i][j] for j in range(3)] for i in range(3)]
    M1 = [[y[i] if j == 1 else M[i][j] for j in range(3)] for i in range(3)]
    M2 = [[y[i] if j == 2 else M[i][j] for j in range(3)] for i in range(3)]

    return [det(M0)/d, det(M1)/d, det(M2)/d]

def compute_expected_results():
    """Computes the expected normalized OLS coefficients from the raw data."""
    basis = []
    with open('/home/user/data/basis.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            basis.append([float(row['alpha']), float(row['beta']), float(row['coil'])])

    spectra = {}
    with open('/home/user/data/spectra.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            seq_id = row['seq_id']
            if seq_id not in spectra:
                spectra[seq_id] = []
            spectra[seq_id].append(float(row['intensity']))

    # Compute B^T B
    M = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    for i in range(3):
        for j in range(3):
            M[i][j] = sum(basis[k][i] * basis[k][j] for k in range(len(basis)))

    expected = {}
    for seq_id, S in spectra.items():
        # Compute B^T S
        y = [0, 0, 0]
        for i in range(3):
            y[i] = sum(basis[k][i] * S[k] for k in range(len(basis)))

        c = solve_3x3(M, y)
        c_sum = sum(c)
        c_norm = [round(x / c_sum, 4) for x in c]
        expected[seq_id] = c_norm

    return expected

def test_venv_exists():
    """Test that the Python virtual environment is set up."""
    venv_path = '/home/user/venv'
    assert os.path.isdir(venv_path), f"Virtual environment directory {venv_path} does not exist."
    assert os.path.isfile(os.path.join(venv_path, 'bin', 'python')), "Python executable not found in the virtual environment."

def test_scripts_exist_and_executable():
    """Test that the required scripts exist and the bash script is executable."""
    bash_script = '/home/user/run_pipeline.sh'
    python_script = '/home/user/fit_spectra.py'

    assert os.path.isfile(bash_script), f"Bash script {bash_script} does not exist."
    assert os.access(bash_script, os.X_OK), f"Bash script {bash_script} is not executable."

    assert os.path.isfile(python_script), f"Python script {python_script} does not exist."

def test_results_csv_correctness():
    """Test that results.csv exists, is formatted correctly, and contains the correct OLS results."""
    results_file = '/home/user/results.csv'
    assert os.path.isfile(results_file), f"Results file {results_file} does not exist."

    expected = compute_expected_results()

    with open(results_file, 'r') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        assert header == ['seq_id', 'alpha', 'beta', 'coil'], f"Incorrect header in results.csv: {header}"

        rows = list(reader)

    assert len(rows) == len(expected), f"Expected {len(expected)} rows, found {len(rows)}."

    # Check that rows are sorted alphabetically by seq_id
    seq_ids = [row[0] for row in rows]
    assert seq_ids == sorted(seq_ids), "The results.csv file is not sorted alphabetically by seq_id."

    for row in rows:
        seq_id = row[0]
        assert seq_id in expected, f"Unexpected seq_id {seq_id} in results.csv."

        try:
            alpha = float(row[1])
            beta = float(row[2])
            coil = float(row[3])
        except ValueError:
            pytest.fail(f"Non-numeric coefficient found for {seq_id}.")

        exp_alpha, exp_beta, exp_coil = expected[seq_id]

        assert abs(alpha - exp_alpha) <= 1e-4, f"Alpha coefficient for {seq_id} incorrect. Expected {exp_alpha}, got {alpha}."
        assert abs(beta - exp_beta) <= 1e-4, f"Beta coefficient for {seq_id} incorrect. Expected {exp_beta}, got {beta}."
        assert abs(coil - exp_coil) <= 1e-4, f"Coil coefficient for {seq_id} incorrect. Expected {exp_coil}, got {coil}."