# test_final_state.py

import os
import json
import csv

def test_executable_exists():
    executable = "/home/user/bin/seq_processor"
    assert os.path.isfile(executable), f"Executable {executable} does not exist. Did you compile the C program?"
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_measurements_csv():
    csv_file = "/home/user/measurements.csv"
    assert os.path.isfile(csv_file), f"Measurements file {csv_file} does not exist."

    with open(csv_file, 'r') as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert len(rows) > 1, "CSV file should have a header and data rows."
    assert rows[0] == ["time", "marker_freq"], "CSV header is incorrect."

    # Check the first and last row values based on the C program logic and sequences.txt
    # First sequence: 20 GC out of 40 = 0.5000
    assert float(rows[1][0]) == 0.0, "First time point should be 0.0"
    assert abs(float(rows[1][1]) - 0.5000) < 1e-4, "First marker_freq should be 0.5000"

def test_analyze_script_exists():
    script_file = "/home/user/analyze.py"
    assert os.path.isfile(script_file), f"Python script {script_file} does not exist."

def test_mcmc_results():
    results_file = "/home/user/mcmc_results.json"
    assert os.path.isfile(results_file), f"Results file {results_file} does not exist."

    with open(results_file, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, "Results file is not valid JSON."

    assert "alpha" in results, "Key 'alpha' missing in results."
    assert "beta" in results, "Key 'beta' missing in results."

    assert isinstance(results["alpha"], (int, float)), "'alpha' must be a number."
    assert isinstance(results["beta"], (int, float)), "'beta' must be a number."

    # Basic bounds check based on the uniform priors [0.0, 2.0]
    assert 0.0 <= results["alpha"] <= 2.0, "'alpha' is outside the prior bounds [0.0, 2.0]."
    assert 0.0 <= results["beta"] <= 2.0, "'beta' is outside the prior bounds [0.0, 2.0]."