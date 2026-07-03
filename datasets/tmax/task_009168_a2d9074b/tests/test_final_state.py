# test_final_state.py
import os
import json
import math
import pytest

def get_ca_coordinates(pdb_path):
    coords = []
    with open(pdb_path, 'r') as f:
        for line in f:
            if line.startswith("ATOM") and line[12:16].strip() == "CA":
                x = float(line[30:38].strip())
                y = float(line[38:46].strip())
                z = float(line[46:54].strip())
                coords.append((x, y, z))
    return coords

def compute_distance_matrix(coords):
    n = len(coords)
    D = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dx = coords[i][0] - coords[j][0]
            dy = coords[i][1] - coords[j][1]
            dz = coords[i][2] - coords[j][2]
            D[i][j] = math.sqrt(dx*dx + dy*dy + dz*dz)
    return D

def power_iteration_max_sv(A, iters=100):
    # For a symmetric matrix with non-negative eigenvalues (or if we just want max abs eigenvalue),
    # power iteration finds the dominant eigenvalue, which is the max singular value.
    n = len(A)
    b_k = [1.0] * n
    for _ in range(iters):
        b_k1 = [sum(A[i][j] * b_k[j] for j in range(n)) for i in range(n)]
        norm = math.sqrt(sum(x*x for x in b_k1))
        b_k = [x / norm for x in b_k1]

    # Rayleigh quotient
    Ax = [sum(A[i][j] * b_k[j] for j in range(n)) for i in range(n)]
    eigenvalue = sum(b_k[i] * Ax[i] for i in range(n))
    return abs(eigenvalue)

def test_extract_svd_output():
    svd_file = "/home/user/results/svd_max.txt"
    assert os.path.isfile(svd_file), f"{svd_file} is missing. Did extract_svd.py run?"

    coords = get_ca_coordinates("/home/user/data/input.pdb")
    D = compute_distance_matrix(coords)
    expected_sigma_max = power_iteration_max_sv(D)

    with open(svd_file, 'r') as f:
        content = f.read().strip()

    try:
        actual_sigma_max = float(content)
    except ValueError:
        pytest.fail(f"Could not parse float from {svd_file}. Content: {content}")

    assert math.isclose(actual_sigma_max, expected_sigma_max, rel_tol=1e-3), \
        f"Expected max singular value ~{expected_sigma_max:.4f}, got {actual_sigma_max}"

def test_integrator_implementation():
    integrator_path = "/home/user/sim/integrator.py"
    assert os.path.isfile(integrator_path), f"{integrator_path} is missing."

    with open(integrator_path, 'r') as f:
        code = f.read()

    assert "solve_ivp" in code, "integrator.py must use scipy.integrate.solve_ivp"
    assert "'RK45'" in code or '"RK45"' in code, "integrator.py must specify the 'RK45' method"

def test_ensemble_output():
    ensemble_file = "/home/user/results/ensemble_final.json"
    assert os.path.isfile(ensemble_file), f"{ensemble_file} is missing. Did run_ensemble.py run?"

    coords = get_ca_coordinates("/home/user/data/input.pdb")
    D = compute_distance_matrix(coords)
    sigma_max = power_iteration_max_sv(D)

    with open(ensemble_file, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{ensemble_file} is not valid JSON.")

    expected_c_values = ["0.5", "1.0", "1.5", "2.0"]
    for c_str in expected_c_values:
        assert c_str in results, f"Missing scaling factor {c_str} in ensemble results."
        c = float(c_str)
        k = c * sigma_max
        # Analytical solution to dy/dt = -k*y, y(0)=100 is y(t) = 100 * exp(-k*t)
        expected_y = 100.0 * math.exp(-k * 5.0)
        actual_y = results[c_str]

        assert math.isclose(actual_y, expected_y, rel_tol=1e-2), \
            f"For c={c_str}, expected y ~ {expected_y:.4f}, but got {actual_y}"

def test_pipeline_script():
    pipeline_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(pipeline_path), f"{pipeline_path} is missing."
    assert os.access(pipeline_path, os.X_OK), f"{pipeline_path} is not executable."

    with open(pipeline_path, 'r') as f:
        script_content = f.read()

    assert "extract_svd.py" in script_content, "Pipeline script must run extract_svd.py"
    assert "run_ensemble.py" in script_content, "Pipeline script must run run_ensemble.py"
    assert "mkdir" in script_content and "results" in script_content, "Pipeline script must create the results directory"