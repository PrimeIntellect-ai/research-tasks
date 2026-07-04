# test_final_state.py

import os
import math
import re

def test_posterior_stats_file():
    stats_path = "/home/user/posterior_stats.txt"
    assert os.path.isfile(stats_path), f"File missing: {stats_path}"

    with open(stats_path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 2, f"Expected exactly 2 lines in {stats_path}, found {len(lines)}"

    mu_match = re.match(r"^mu:\s*([0-9.]+)$", lines[0])
    sigma_match = re.match(r"^sigma:\s*([0-9.]+)$", lines[1])

    assert mu_match, "First line must be formatted as 'mu: <value>'"
    assert sigma_match, "Second line must be formatted as 'sigma: <value>'"

    mu_val = float(mu_match.group(1))
    sigma_val = float(sigma_match.group(1))

    # Calculate actual sample mean and stddev from the PDB file
    pdb_path = "/home/user/protein.pdb"
    assert os.path.isfile(pdb_path), f"File missing: {pdb_path}"

    ca_b_factors = []
    with open(pdb_path, "r") as f:
        for line in f:
            if line.startswith("ATOM"):
                atom_name = line[12:16]
                if atom_name == " CA ":
                    b_factor = float(line[60:66].strip())
                    ca_b_factors.append(b_factor)

    assert len(ca_b_factors) > 0, "No CA atoms found in the PDB file."

    n = len(ca_b_factors)
    sample_mean = sum(ca_b_factors) / n
    variance = sum((x - sample_mean) ** 2 for x in ca_b_factors) / n
    sample_sigma = math.sqrt(variance)

    # Check if the estimated mu and sigma are within 0.3 of the sample estimates
    assert abs(mu_val - sample_mean) <= 0.3, f"Estimated mu ({mu_val}) is not within 0.3 of the sample mean ({sample_mean:.2f})"
    assert abs(sigma_val - sample_sigma) <= 0.3, f"Estimated sigma ({sigma_val}) is not within 0.3 of the sample standard deviation ({sample_sigma:.2f})"

    # Check rounding
    assert len(mu_match.group(1).split('.')[-1]) == 1, "mu value must be rounded to exactly one decimal place"
    assert len(sigma_match.group(1).split('.')[-1]) == 1, "sigma value must be rounded to exactly one decimal place"