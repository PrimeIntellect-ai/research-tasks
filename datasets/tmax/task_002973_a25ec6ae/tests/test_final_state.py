# test_final_state.py

import os
import re

def test_mcmc_opt_exists_and_executable():
    path = "/home/user/mcmc_opt"
    assert os.path.isfile(path), f"File {path} does not exist. Did you compile the C code?"
    assert os.access(path, os.X_OK), f"File {path} is not executable."

def test_trace_csv():
    path = "/home/user/trace.csv"
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, "r") as f:
        lines = f.read().strip().split("\n")
    assert len(lines) == 10000, f"Expected exactly 10,000 lines in {path}, got {len(lines)}."

    # Verify format of the first line
    parts = lines[0].split(',')
    assert len(parts) == 2, f"Expected 2 comma-separated values per line in {path}, got {len(parts)}."
    try:
        float(parts[0])
        float(parts[1])
    except ValueError:
        assert False, f"Values in {path} are not valid floats."

def test_trace_plot_png():
    path = "/home/user/trace_plot.png"
    assert os.path.isfile(path), f"File {path} does not exist. Did you generate the plot?"

def test_results_txt():
    path = "/home/user/results.txt"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read().strip()

    mu_match = re.search(r"^mu=([0-9\.]+)$", content, re.MULTILINE)
    sigma_match = re.search(r"^sigma=([0-9\.]+)$", content, re.MULTILINE)

    assert mu_match, f"Could not find 'mu=X.XX' format in {path}."
    assert sigma_match, f"Could not find 'sigma=Y.YY' format in {path}."

    mu_val = float(mu_match.group(1))
    sigma_val = float(sigma_match.group(1))

    assert 5.5 <= mu_val <= 5.7, f"mu value {mu_val} is out of expected range (5.5 - 5.7)."
    assert 1.0 <= sigma_val <= 1.3, f"sigma value {sigma_val} is out of expected range (1.0 - 1.3)."

def test_mcmc_c_optimized():
    path = "/home/user/mcmc.c"
    assert os.path.isfile(path), f"File {path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # The original file had fopen inside log_likelihood and in main.
    # A properly optimized file should read the file only once in main.
    fopen_count = content.count("fopen")
    assert fopen_count <= 1, "The C code still seems to call fopen multiple times. The bottleneck in log_likelihood might not be fixed."