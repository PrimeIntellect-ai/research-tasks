# test_final_state.py

import os
import json
import math
import subprocess
import pytest

def test_virtual_environment_and_packages():
    venv_python = "/home/user/bio_env/bin/python"
    assert os.path.exists(venv_python), "Virtual environment Python executable not found at /home/user/bio_env/bin/python"

    # Check if required packages can be imported
    cmd = [venv_python, "-c", "import Bio; import numpy; import scipy; import emcee; import pytest"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Failed to import required packages in the virtual environment. Error:\n{result.stderr}"

def test_results_json_exists_and_valid():
    results_path = "/home/user/pipeline/results.json"
    assert os.path.exists(results_path), f"Results file {results_path} does not exist"

    with open(results_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {results_path} is not valid JSON")

    assert "kde_peak" in results, "Missing 'kde_peak' in results.json"
    assert "mcmc_mu" in results, "Missing 'mcmc_mu' in results.json"
    assert "mcmc_sigma" in results, "Missing 'mcmc_sigma' in results.json"

    assert isinstance(results["kde_peak"], (int, float)), "'kde_peak' must be a float"
    assert isinstance(results["mcmc_mu"], (int, float)), "'mcmc_mu' must be a float"
    assert isinstance(results["mcmc_sigma"], (int, float)), "'mcmc_sigma' must be a float"

def test_results_values():
    fasta_path = "/home/user/data/reads.fasta"
    assert os.path.exists(fasta_path), f"Fasta file {fasta_path} missing"

    gc_contents = []
    with open(fasta_path, "r") as f:
        seq = []
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                if seq:
                    s = "".join(seq)
                    gc = (s.count('G') + s.count('C')) / len(s) * 100
                    gc_contents.append(gc)
                    seq = []
            else:
                seq.append(line.upper())
        if seq:
            s = "".join(seq)
            gc = (s.count('G') + s.count('C')) / len(s) * 100
            gc_contents.append(gc)

    n = len(gc_contents)
    assert n > 0, "No sequences found in fasta file to compute GC contents."
    emp_mu = sum(gc_contents) / n
    emp_var = sum((x - emp_mu)**2 for x in gc_contents) / n
    emp_sigma = math.sqrt(emp_var)

    results_path = "/home/user/pipeline/results.json"
    with open(results_path, "r") as f:
        results = json.load(f)

    # kde_peak should be roughly near empirical mean
    assert 48.0 <= results["kde_peak"] <= 56.0, f"kde_peak {results['kde_peak']} is out of expected range."

    # mcmc_mu should be close to empirical mean
    assert abs(results["mcmc_mu"] - emp_mu) <= 0.5, f"mcmc_mu {results['mcmc_mu']} is not within 0.5 of empirical mean {emp_mu}"

    # mcmc_sigma should be close to empirical std
    assert abs(results["mcmc_sigma"] - emp_sigma) <= 0.5, f"mcmc_sigma {results['mcmc_sigma']} is not within 0.5 of empirical sigma {emp_sigma}"

def test_regression_test_exists_and_passes():
    test_file = "/home/user/pipeline/test_regression.py"
    assert os.path.exists(test_file), f"Test file {test_file} does not exist"

    with open(test_file, "r") as f:
        content = f.read()
        assert "mcmc_mu" in content and "mcmc_sigma" in content, "test_regression.py doesn't seem to check mcmc_mu and mcmc_sigma"

    pytest_bin = "/home/user/bio_env/bin/pytest"
    assert os.path.exists(pytest_bin), f"pytest executable not found at {pytest_bin}"

    cmd = [pytest_bin, test_file]
    result = subprocess.run(cmd, capture_output=True, text=True)
    assert result.returncode == 0, f"Regression tests failed. Pytest output:\n{result.stdout}\n{result.stderr}"