# test_final_state.py
import os
import subprocess
import pytest

def test_magic_seed_recovered():
    seed_file = '/home/user/magic_seed.txt'
    assert os.path.exists(seed_file), f"File {seed_file} does not exist."
    with open(seed_file, 'r') as f:
        seed = f.read().strip()
    expected_seed = "a1b2c3d4e5f678901234567890abcdef"
    assert seed == expected_seed, f"Incorrect magic seed in {seed_file}. Expected {expected_seed}, got {seed}"

def test_solver_bug_fixed():
    solver_path = '/home/user/nbody_relax/solver.c'
    assert os.path.exists(solver_path), f"File {solver_path} does not exist."
    with open(solver_path, 'r') as f:
        content = f.read()
    assert "int dfx" not in content, "The integer truncation bug 'int dfx' is still present in solver.c."

def test_mre_compiles_and_runs():
    mre_c = '/home/user/mre.c'
    solver_c = '/home/user/nbody_relax/solver.c'
    mre_bin = '/home/user/mre'

    assert os.path.exists(mre_c), f"File {mre_c} does not exist."

    # Re-compile to ensure it builds correctly with the fixed solver
    compile_res = subprocess.run(
        ['gcc', '-o', mre_bin, mre_c, solver_c, '-lm'],
        capture_output=True,
        text=True
    )
    assert compile_res.returncode == 0, f"Compilation of MRE failed:\n{compile_res.stderr}"

    # Run the compiled binary
    run_res = subprocess.run([mre_bin], capture_output=True, text=True)
    assert run_res.returncode == 0, f"Execution of {mre_bin} failed with exit code {run_res.returncode}:\n{run_res.stderr}"

def test_convergence_result():
    result_file = '/home/user/convergence_result.txt'
    assert os.path.exists(result_file), f"File {result_file} does not exist."
    with open(result_file, 'r') as f:
        result = f.read().strip()
    assert result == "5.0000", f"Incorrect convergence result. Expected '5.0000', got '{result}'."