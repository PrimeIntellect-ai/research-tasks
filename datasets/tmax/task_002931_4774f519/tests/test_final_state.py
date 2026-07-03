# test_final_state.py

import os
import subprocess
import numpy as np

def test_reproducibility():
    """Verify that running the Go simulation 5 times produces identical output."""
    go_file = "/home/user/sim/main.go"
    assert os.path.isfile(go_file), f"Go file {go_file} does not exist."

    outputs = []
    for _ in range(5):
        res = subprocess.run(["go", "run", go_file], capture_output=True, text=True)
        assert res.returncode == 0, f"Go program failed to run: {res.stderr}"
        outputs.append(res.stdout.strip())

    assert len(set(outputs)) == 1, "Variance > 0: Output is not reproducible across runs."

def test_steady_state_mse():
    """Verify that the steady state output matches the analytical solution with MSE < 1e-20."""
    target = np.array([0.3448275862068966, 0.1149425287356322, 0.2298850574712644, 0.3103448275862069])

    file_path = "/home/user/steady_state.txt"
    assert os.path.isfile(file_path), f"Output file {file_path} does not exist."

    with open(file_path, "r") as f:
        lines = f.readlines()

    assert len(lines) == 4, f"Expected exactly 4 lines in {file_path}, found {len(lines)}"

    try:
        agent_state = np.array([float(x.strip()) for x in lines])
    except ValueError as e:
        assert False, f"Could not parse floats from {file_path}: {e}"

    mse = np.mean((agent_state - target)**2)
    assert mse < 1e-20, f"MSE {mse} is not less than threshold 1e-20. Agent state: {agent_state}"