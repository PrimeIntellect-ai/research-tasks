# test_final_state.py

import os
import math
import pytest

def parse_pdb(filename):
    atoms = []
    with open(filename, 'r') as f:
        for line in f:
            if line.startswith("ATOM"):
                atom_name = line[12:16].strip()
                if "CA" in atom_name:
                    x = float(line[30:38])
                    y = float(line[38:46])
                    z = float(line[46:54])
                    atoms.append((x, y, z))
    return atoms

def calc_dist(atoms):
    n = len(atoms)
    mat = [[0.0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dx = atoms[i][0] - atoms[j][0]
            dy = atoms[i][1] - atoms[j][1]
            dz = atoms[i][2] - atoms[j][2]
            mat[i][j] = math.sqrt(dx*dx + dy*dy + dz*dz)
    return mat

def lu_decompose(mat, n, eps):
    for i in range(n):
        mat[i][i] += eps

    u_diag = [0.0]*n
    for i in range(n):
        for j in range(i, n):
            s = sum(mat[i][k] * mat[k][j] for k in range(i))
            mat[i][j] -= s
        for j in range(i + 1, n):
            s = sum(mat[j][k] * mat[k][i] for k in range(i))
            if mat[i][i] == 0.0:
                raise ValueError("Zero pivot")
            mat[j][i] = (mat[j][i] - s) / mat[i][i]
        u_diag[i] = mat[i][i]
    return u_diag

def pearson(x, y):
    n = len(x)
    mean_x = sum(x)/n
    mean_y = sum(y)/n
    num = sum((x[i]-mean_x)*(y[i]-mean_y) for i in range(n))
    den_x = sum((x[i]-mean_x)**2 for i in range(n))
    den_y = sum((y[i]-mean_y)**2 for i in range(n))
    return num / math.sqrt(den_x * den_y)

def test_executable_exists():
    exe_path = "/home/user/analyze_struct"
    assert os.path.isfile(exe_path), f"Compiled executable not found at {exe_path}"
    assert os.access(exe_path, os.X_OK), f"File at {exe_path} is not executable"

def test_h5_files_exist():
    h5_a = "/home/user/A_eps0.01.h5"
    h5_b = "/home/user/B_eps0.01.h5"
    assert os.path.isfile(h5_a), f"HDF5 output not found at {h5_a}"
    assert os.path.isfile(h5_b), f"HDF5 output not found at {h5_b}"

def test_python_script_and_plot_exist():
    script_path = "/home/user/compare.py"
    plot_path = "/home/user/plot.png"
    assert os.path.isfile(script_path), f"Python script not found at {script_path}"
    assert os.path.isfile(plot_path), f"Plot image not found at {plot_path}"

def test_correlation_value():
    corr_file = "/home/user/correlation.txt"
    assert os.path.isfile(corr_file), f"Correlation output file not found at {corr_file}"

    # Compute expected correlation
    atoms_a = parse_pdb("/home/user/structA.pdb")
    atoms_b = parse_pdb("/home/user/structB.pdb")

    dist_a = calc_dist(atoms_a)
    dist_b = calc_dist(atoms_b)

    u_diag_a = lu_decompose(dist_a, len(atoms_a), 0.01)
    u_diag_b = lu_decompose(dist_b, len(atoms_b), 0.01)

    expected_corr = pearson(u_diag_a, u_diag_b)

    with open(corr_file, 'r') as f:
        content = f.read().strip()

    try:
        student_val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse correlation value from {corr_file}. Content was: '{content}'")

    assert abs(student_val - expected_corr) < 1e-3, (
        f"Correlation value in {corr_file} is {student_val}, "
        f"but expected approximately {expected_corr:.4f}."
    )