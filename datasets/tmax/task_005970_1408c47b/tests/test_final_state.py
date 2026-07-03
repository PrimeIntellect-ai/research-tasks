# test_final_state.py

import os
import json
import math
import pytest

def test_c_source_and_executable_exist():
    assert os.path.exists("/home/user/model_fit.c"), "/home/user/model_fit.c does not exist"
    assert os.path.exists("/home/user/model_fit"), "Compiled executable /home/user/model_fit does not exist"
    assert os.path.exists("/home/user/results.json"), "/home/user/results.json does not exist"

def test_results_json_structure_and_values():
    results_path = "/home/user/results.json"
    assert os.path.exists(results_path), f"File {results_path} is missing."

    with open(results_path, "r") as f:
        try:
            res = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("results.json is not a valid JSON file.")

    required_keys = ["X_s", "mu", "ci_lower", "ci_upper", "integral_D1", "integral_D2", "bins_D1", "bins_D2"]
    for k in required_keys:
        assert k in res, f"Key '{k}' is missing from results.json"

    # 1. Verify X_s
    genome_path = "/home/user/genome.txt"
    assert os.path.exists(genome_path), "genome.txt is missing."
    with open(genome_path, "r") as f:
        genome = f.read().strip('\n')

    match_index = genome.find("TTAGGCAT")
    assert match_index != -1, "Primer sequence 'TTAGGCAT' not found in genome.txt"
    expected_Xs = match_index / len(genome)
    assert abs(res["X_s"] - expected_Xs) < 1e-5, f"Expected X_s approx {expected_Xs}, got {res['X_s']}"

    # 2. Verify mu
    affinity_path = "/home/user/affinity.csv"
    assert os.path.exists(affinity_path), "affinity.csv is missing."
    with open(affinity_path, "r") as f:
        vals = [float(x.strip()) for x in f.readlines() if x.strip()]

    expected_mu = sum(vals) / len(vals)
    assert abs(res["mu"] - expected_mu) < 1e-5, f"Expected mu approx {expected_mu}, got {res['mu']}"

    # 3. Verify CI ranges (approximate due to glibc rand() differences)
    # The true values depend on the CSV, but for the given distribution, they should be around the mean
    assert expected_mu - 1.0 < res["ci_lower"] < expected_mu, f"ci_lower {res['ci_lower']} out of expected range"
    assert expected_mu < res["ci_upper"] < expected_mu + 1.0, f"ci_upper {res['ci_upper']} out of expected range"

    # 4. Verify Integrals and Bins
    def f_val(x, mu, Xs):
        return mu * math.exp(-50.0 * (x - Xs)**2)

    def trapz(a, b, n, mu, Xs):
        h = (b - a) / n
        s = 0.5 * (f_val(a, mu, Xs) + f_val(b, mu, Xs))
        for i in range(1, n):
            s += f_val(a + i * h, mu, Xs)
        return s * h

    def refine(a, b, mu, Xs):
        n = 10
        prev = trapz(a, b, n, mu, Xs)
        while True:
            n *= 2
            curr = trapz(a, b, n, mu, Xs)
            if abs(curr - prev) < 1e-6:
                return curr, n
            prev = curr

    int1, bins1 = refine(0, expected_Xs, expected_mu, expected_Xs)
    int2, bins2 = refine(expected_Xs, 1.0, expected_mu, expected_Xs)

    assert abs(res["integral_D1"] - int1) < 1e-4, f"Expected integral_D1 approx {int1}, got {res['integral_D1']}"
    assert abs(res["integral_D2"] - int2) < 1e-4, f"Expected integral_D2 approx {int2}, got {res['integral_D2']}"
    assert res["bins_D1"] == bins1, f"Expected bins_D1={bins1}, got {res['bins_D1']}"
    assert res["bins_D2"] == bins2, f"Expected bins_D2={bins2}, got {res['bins_D2']}"