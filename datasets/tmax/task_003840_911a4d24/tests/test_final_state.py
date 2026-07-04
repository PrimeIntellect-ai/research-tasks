# test_final_state.py
import os
import re

def get_expected_energy():
    with open("/home/user/molecule.dat", "r") as f:
        lines = f.read().split()

    N = int(lines[0])
    potentials = [float(x) for x in lines[1:N+1]]

    # Simulate the Jacobi iteration exactly as in the C code
    for _ in range(10):
        new_potentials = potentials[:]
        for i in range(1, N - 1):
            new_potentials[i] = (potentials[i-1] + potentials[i+1] + potentials[i]) / 3.0
        potentials = new_potentials

    # Kahan Summation
    total_energy = 0.0
    c = 0.0
    for i in range(N):
        y = potentials[i] - c
        t = total_energy + y
        c = (t - total_energy) - y
        total_energy = t

    return total_energy

def test_executable_exists():
    assert os.path.isfile("/home/user/model_fit"), "The compiled executable /home/user/model_fit is missing."
    assert os.access("/home/user/model_fit", os.X_OK), "/home/user/model_fit is not executable."

def test_output_file_exists():
    assert os.path.isfile("/home/user/fixed_output.txt"), "The output file /home/user/fixed_output.txt is missing."

def test_kahan_summation_output():
    expected_energy = get_expected_energy()
    expected_output_str = f"Total Energy: {expected_energy:.10f}"

    with open("/home/user/fixed_output.txt", "r") as f:
        output_content = f.read().strip()

    # We allow slight floating point formatting differences, but it should closely match
    match = re.search(r"Total Energy:\s*([0-9]+\.[0-9]+)", output_content)
    assert match is not None, "Could not find 'Total Energy: <number>' in fixed_output.txt"

    actual_energy = float(match.group(1))

    # Compare with a very small tolerance (C double precision)
    assert abs(actual_energy - expected_energy) < 1e-5, f"Expected energy close to {expected_energy:.10f}, but got {actual_energy}"

def test_source_code_modified():
    with open("/home/user/model_fit.c", "r") as f:
        content = f.read()

    # The naive sum should ideally be gone or replaced, but we mainly check that Kahan summation variables/logic are introduced
    assert "total_energy = t" in content or "c =" in content or "y =" in content, "Could not find Kahan summation logic in model_fit.c"