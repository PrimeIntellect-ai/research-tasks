# test_final_state.py
import json
import math
import os

def test_results_json():
    results_path = "/home/user/results.json"
    assert os.path.exists(results_path), f"The file {results_path} does not exist."

    with open(results_path, "r") as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{results_path} is not a valid JSON file."

    expected_keys = {"com_x", "com_y", "com_z", "wasserstein_distance", "ks_statistic", "ks_pvalue"}
    actual_keys = set(results.keys())
    assert actual_keys == expected_keys, (
        f"results.json keys do not match the expected keys.\n"
        f"Missing: {expected_keys - actual_keys}\n"
        f"Unexpected: {actual_keys - expected_keys}"
    )

    # Recompute the expected values
    coords = []
    ala_coords = []
    pdb_path = "/home/user/protein.pdb"
    assert os.path.exists(pdb_path), f"{pdb_path} is missing, cannot verify results."

    with open(pdb_path, "r") as f:
        for line in f:
            if line.startswith("ATOM") and line[12:16].strip() == "CA":
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                coords.append((x, y, z))
                if line[17:20].strip() == "ALA":
                    ala_coords.append((x, y, z))

    assert len(coords) > 0, "No CA atoms found in the PDB file."

    # Center of Mass
    com_x = sum(c[0] for c in coords) / len(coords)
    com_y = sum(c[1] for c in coords) / len(coords)
    com_z = sum(c[2] for c in coords) / len(coords)

    # ALA Distances
    distances = []
    for c in ala_coords:
        d = math.sqrt((c[0] - com_x)**2 + (c[1] - com_y)**2 + (c[2] - com_z)**2)
        distances.append(d)

    distances.sort()
    n = len(distances)

    # KS Statistic against Rayleigh(scale=15.0)
    # CDF of Rayleigh is 1 - exp(-x^2 / (2 * sigma^2))
    ks_stat = 0
    sigma = 15.0
    for i, d in enumerate(distances):
        cdf = 1.0 - math.exp(- (d**2) / (2.0 * sigma**2))
        d_plus = (i + 1) / n - cdf
        d_minus = cdf - i / n
        ks_stat = max(ks_stat, d_plus, d_minus)

    # Assertions with tolerance
    tol = 0.0002

    assert abs(results["com_x"] - round(com_x, 4)) <= tol, \
        f"com_x is incorrect. Expected {round(com_x, 4)}, got {results['com_x']}"

    assert abs(results["com_y"] - round(com_y, 4)) <= tol, \
        f"com_y is incorrect. Expected {round(com_y, 4)}, got {results['com_y']}"

    assert abs(results["com_z"] - round(com_z, 4)) <= tol, \
        f"com_z is incorrect. Expected {round(com_z, 4)}, got {results['com_z']}"

    assert abs(results["ks_statistic"] - round(ks_stat, 4)) <= tol, \
        f"ks_statistic is incorrect. Expected {round(ks_stat, 4)}, got {results['ks_statistic']}"

    # The Wasserstein distance depends on a specific numpy random sample which is non-trivial 
    # to replicate exactly without numpy. We use a slightly looser tolerance around the known 
    # expected value for the fixed random seed.
    expected_w_dist = 8.9221
    assert abs(results["wasserstein_distance"] - expected_w_dist) <= 0.005, \
        f"wasserstein_distance is incorrect. Expected ~{expected_w_dist}, got {results['wasserstein_distance']}"

    expected_pvalue = 0.0
    assert abs(results["ks_pvalue"] - expected_pvalue) <= tol, \
        f"ks_pvalue is incorrect. Expected ~{expected_pvalue}, got {results['ks_pvalue']}"