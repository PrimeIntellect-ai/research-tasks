# test_final_state.py

import os
import pytest

PROJECT_DIR = "/home/user/spectroscopy_project"
RESULTS_FILE = os.path.join(PROJECT_DIR, "results.txt")

def test_results_file_exists():
    assert os.path.isfile(RESULTS_FILE), f"The results file {RESULTS_FILE} was not found. Did you run the pipeline?"

def test_results_format_and_values():
    assert os.path.isfile(RESULTS_FILE), "Results file missing."

    results = {}
    with open(RESULTS_FILE, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if "=" in line:
                key, val = line.split("=", 1)
                try:
                    results[key.strip()] = float(val.strip())
                except ValueError:
                    pytest.fail(f"Value for {key} is not a valid float: {val}")

    for key in ["mu", "sigma", "loss"]:
        assert key in results, f"Key '{key}' is missing from {RESULTS_FILE}"

    mu = results["mu"]
    sigma = results["sigma"]
    loss = results["loss"]

    import math
    assert not math.isnan(mu), "mu is NaN"
    assert not math.isnan(sigma), "sigma is NaN"
    assert not math.isnan(loss), "loss is NaN"

    assert 4.8 <= mu <= 5.2, f"mu ({mu}) is not within the expected range [4.8, 5.2]. Optimization may have failed or diverged."
    assert 1.0 <= sigma <= 1.4, f"sigma ({sigma}) is not within the expected range [1.0, 1.4]. Optimization may have failed or diverged."
    assert loss < 0.1, f"loss ({loss}) is not less than 0.1. Optimization did not converge sufficiently."