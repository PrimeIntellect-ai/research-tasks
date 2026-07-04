# test_final_state.py
import os
import re

def test_files_exist():
    expected_files = [
        "/home/user/heat_ode.c",
        "/home/user/run_convergence.sh",
        "/home/user/heat_ode",
        "/home/user/convergence.txt"
    ]
    for f in expected_files:
        assert os.path.exists(f), f"Expected file {f} is missing."

def test_openmp_usage():
    with open("/home/user/heat_ode.c", "r") as f:
        source = f.read()
    assert "omp" in source.lower(), "The C source code does not appear to use OpenMP directives."

def test_compilation_script():
    with open("/home/user/run_convergence.sh", "r") as f:
        script = f.read()
    assert "gcc" in script and "fopenmp" in script, "The bash script must compile the code using gcc with OpenMP enabled (-fopenmp)."
    assert os.access("/home/user/run_convergence.sh", os.X_OK), "The bash script must have executable permissions."

def test_convergence_output():
    with open("/home/user/convergence.txt", "r") as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]

    assert len(lines) == 3, f"Expected 3 lines of output in convergence.txt, found {len(lines)}."

    # Check dt=0.1
    assert "0.1" in lines[0], f"First line should contain dt=0.1, got: {lines[0]}"
    t0_1_match = re.search(r"T0=([0-9.]+)", lines[0])
    assert t0_1_match, f"Could not parse T0 from first line: {lines[0]}"
    t0_1 = float(t0_1_match.group(1))
    assert 296.0 < t0_1 < 298.0, f"Expected T0 for dt=0.1 to be ~296.87, got {t0_1}"

    # Check dt=0.01
    assert "0.01" in lines[1], f"Second line should contain dt=0.01, got: {lines[1]}"
    t0_2_match = re.search(r"T0=([0-9.]+)", lines[1])
    assert t0_2_match, f"Could not parse T0 from second line: {lines[1]}"
    t0_2 = float(t0_2_match.group(1))
    assert 305.0 < t0_2 < 307.0, f"Expected T0 for dt=0.01 to be ~305.82, got {t0_2}"

    # Check dt=0.001
    assert "0.001" in lines[2], f"Third line should contain dt=0.001, got: {lines[2]}"
    t0_3_match = re.search(r"T0=([0-9.]+)", lines[2])
    assert t0_3_match, f"Could not parse T0 from third line: {lines[2]}"
    t0_3 = float(t0_3_match.group(1))
    assert 306.0 < t0_3 < 308.0, f"Expected T0 for dt=0.001 to be ~306.74, got {t0_3}"