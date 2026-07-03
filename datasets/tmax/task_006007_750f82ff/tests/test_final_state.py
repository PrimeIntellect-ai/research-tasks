# test_final_state.py

import os
import re
import subprocess
import pytest

SIMULATION_DIR = "/home/user/simulation"
C_FILE = os.path.join(SIMULATION_DIR, "objective.c")
SO_FILE = os.path.join(SIMULATION_DIR, "libobjective.so")
PY_FILE = os.path.join(SIMULATION_DIR, "optimize.py")
RESULT_FILE = os.path.join(SIMULATION_DIR, "result.txt")

def test_objective_c_fixed():
    """Verify that the floating-point precision issue in objective.c has been fixed."""
    assert os.path.isfile(C_FILE), f"File {C_FILE} is missing."
    with open(C_FILE, "r") as f:
        content = f.read()

    # The reduction variable should be double, not float
    assert "float sum" not in content, "The accumulator 'sum' is still declared as a float in objective.c."
    assert "double sum" in content, "The accumulator 'sum' should be declared as a double in objective.c."

def test_shared_library_compiled():
    """Verify that libobjective.so has been compiled successfully."""
    assert os.path.isfile(SO_FILE), f"Shared library {SO_FILE} is missing."

    # Check if it's an ELF file
    with open(SO_FILE, "rb") as f:
        magic = f.read(4)
    assert magic == b"\x7fELF", f"{SO_FILE} is not a valid ELF file."

def test_optimize_script_exists():
    """Verify that optimize.py exists."""
    assert os.path.isfile(PY_FILE), f"Python script {PY_FILE} is missing."

def test_optimize_script_execution_and_result():
    """Run optimize.py and verify the output in result.txt."""
    # Run the script to generate/overwrite result.txt
    result = subprocess.run(["python3", PY_FILE], capture_output=True, text=True, cwd=SIMULATION_DIR)
    assert result.returncode == 0, f"Running optimize.py failed with error:\n{result.stderr}"

    assert os.path.isfile(RESULT_FILE), f"Result file {RESULT_FILE} was not created by optimize.py."

    with open(RESULT_FILE, "r") as f:
        content = f.read().strip()

    # Verify the format is x,y with exactly 4 decimal places
    match = re.fullmatch(r"(-?\d+\.\d{4}),(-?\d+\.\d{4})", content)
    assert match is not None, f"Content of {RESULT_FILE} ('{content}') does not match the required format 'x.xxxx,y.yyyy'."

    x_str, y_str = match.groups()
    x = float(x_str)
    y = float(y_str)

    # Verify the optimized coordinates are close to the expected minimum (2.0, 3.0)
    assert abs(x - 2.0) < 0.05, f"Optimized x-coordinate {x} is not close enough to the expected value 2.0."
    assert abs(y - 3.0) < 0.05, f"Optimized y-coordinate {y} is not close enough to the expected value 3.0."

def test_determinism():
    """Run the optimization multiple times to ensure the result is deterministic."""
    results = set()
    for _ in range(3):
        subprocess.run(["python3", PY_FILE], capture_output=True, cwd=SIMULATION_DIR)
        with open(RESULT_FILE, "r") as f:
            results.add(f.read().strip())

    assert len(results) == 1, f"Optimization results are not deterministic! Got different results: {results}"