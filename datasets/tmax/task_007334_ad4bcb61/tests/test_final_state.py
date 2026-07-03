# test_final_state.py
import os
import re

def test_run_pipeline_exists_and_executable():
    path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(path), f"Script {path} does not exist."
    assert os.access(path, os.X_OK), f"Script {path} is not executable."

def test_run_pipeline_parallelization():
    path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(path), f"Script {path} does not exist."
    with open(path, "r") as f:
        content = f.read()
    assert "&" in content, "Script does not appear to use background processes (&)."
    assert "wait" in content, "Script does not appear to use the 'wait' command."

def test_final_posterior_output():
    reads_path = "/home/user/spatial_reads.csv"
    assert os.path.isfile(reads_path), f"Input file {reads_path} is missing."

    # Calculate the expected count dynamically
    count = 0
    with open(reads_path, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            if len(parts) >= 3:
                seq = parts[2]
                if "GATTACA" in seq:
                    count += 1

    expected_val = count * 1.374 + 15.2

    out_path = "/home/user/final_posterior.txt"
    assert os.path.isfile(out_path), f"Output file {out_path} does not exist."

    with open(out_path, "r") as f:
        content = f.read().strip()

    match = re.search(r"MCMC Posterior Mean:\s*([0-9.]+)", content)
    assert match is not None, f"Could not parse MCMC Posterior Mean from {out_path}. Content: {content}"

    actual_val = float(match.group(1))
    assert abs(actual_val - expected_val) < 1e-4, f"Expected posterior mean approx {expected_val}, but got {actual_val}"