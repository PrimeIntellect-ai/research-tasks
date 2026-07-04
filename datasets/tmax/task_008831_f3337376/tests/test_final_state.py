# test_final_state.py
import os
import csv
import math
import subprocess
import pytest

CPP_FILE = "/home/user/kepler_solver.cpp"
EXE_FILE = "/home/user/kepler_solver"
INPUT_FILE = "/home/user/inputs.csv"
OUTPUT_FILE = "/home/user/ml_dataset.csv"

def test_source_and_executable_exist():
    """Verify that the source code and compiled executable exist."""
    assert os.path.isfile(CPP_FILE), f"Source file {CPP_FILE} is missing."
    assert os.path.isfile(EXE_FILE), f"Executable file {EXE_FILE} is missing."
    assert os.access(EXE_FILE, os.X_OK), f"File {EXE_FILE} is not executable."

def test_analytical_validation_mode():
    """Verify that the executable supports --test mode and passes."""
    try:
        result = subprocess.run(
            [EXE_FILE, "--test"],
            capture_output=True,
            text=True,
            check=True
        )
        assert "Tests passed" in result.stdout, "The output of --test did not contain 'Tests passed'."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"The --test command failed with exit code {e.returncode}. Output: {e.stdout} {e.stderr}")

def test_ml_dataset_output():
    """Verify that the generated dataset matches the expected Newton-Raphson results."""
    assert os.path.isfile(OUTPUT_FILE), f"Output dataset {OUTPUT_FILE} is missing."

    expected = {}
    with open(INPUT_FILE, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            e = float(row['e'])
            M = float(row['M'])

            # Newton Raphson in Python
            E = M
            iters = 0
            while True:
                f_val = E - e * math.sin(E) - M
                if abs(f_val) < 1e-8:
                    break
                f_prime = 1.0 - e * math.cos(E)
                E = E - f_val / f_prime
                iters += 1
                if iters > 50:
                    break
            expected[row['id']] = (E, iters)

    agent_results = {}
    with open(OUTPUT_FILE, 'r') as f:
        reader = csv.DictReader(f)
        assert 'id' in reader.fieldnames and 'E' in reader.fieldnames and 'iterations' in reader.fieldnames, \
            "Output CSV is missing required headers (id, E, iterations)."
        for row in reader:
            agent_results[row['id']] = (float(row['E']), int(row['iterations']))

    assert len(agent_results) == len(expected), "Output dataset row count does not match input dataset."

    for idx, (expected_E, expected_iters) in expected.items():
        assert idx in agent_results, f"ID {idx} missing in output dataset."
        agent_E, agent_iters = agent_results[idx]

        assert abs(agent_E - expected_E) < 1e-7, f"Mismatch in E for id {idx}. Expected {expected_E}, got {agent_E}."
        assert agent_iters == expected_iters, f"Mismatch in iterations for id {idx}. Expected {expected_iters}, got {agent_iters}."