# test_final_state.py

import os
import json
import numpy as np
import pytest

def parse_pdb(filepath):
    coords = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith("ATOM") and line[12:16].strip() == "CA":
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                coords.append([x, y, z])
    return np.array(coords)

def generate_ensembles(coords):
    np.random.seed(42)
    n_atoms = coords.shape[0]

    # WT Ensemble: 10,000 conformations, std = 0.2
    wt_noise = np.random.normal(0, 0.2, (10000, n_atoms, 3))
    wt_ensemble = coords + wt_noise

    # Mutant Ensemble: 10,000 conformations, std = 0.5
    mut_noise = np.random.normal(0, 0.5, (10000, n_atoms, 3))
    mut_ensemble = coords + mut_noise

    return wt_ensemble, mut_ensemble

def calc_rg(ensemble):
    # ensemble shape: (10000, n_atoms, 3)
    centroids = np.mean(ensemble, axis=1, keepdims=True)
    diff = ensemble - centroids
    sq_dist = np.sum(diff**2, axis=2)
    rg = np.sqrt(np.mean(sq_dist, axis=1))
    return rg

def get_expected_results():
    pdb_path = '/home/user/data/reference.pdb'
    assert os.path.exists(pdb_path), f"Reference PDB missing at {pdb_path}"

    coords = parse_pdb(pdb_path)
    assert len(coords) > 0, "No CA atoms found in reference PDB."

    wt_ens, mut_ens = generate_ensembles(coords)
    wt_rg = calc_rg(wt_ens)
    mut_rg = calc_rg(mut_ens)

    # Replicate the permutation test logic to get the exact expected test statistic
    # The permutation test calculates diff_obs = mean(dist_b) - mean(dist_a)
    # dist_a = WT, dist_b = Mutant
    diff_obs = np.mean(mut_rg) - np.mean(wt_rg)

    return float(diff_obs)

def test_results_json_exists_and_correct():
    results_path = '/home/user/results.json'
    assert os.path.exists(results_path), f"Results file missing at {results_path}"

    with open(results_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File at {results_path} is not valid JSON.")

    assert 'test_statistic' in data, f"Missing 'test_statistic' key in {results_path}"
    assert 'p_value' in data, f"Missing 'p_value' key in {results_path}"

    agent_stat = data['test_statistic']
    expected_stat = get_expected_results()

    threshold = 0.01
    error = abs(agent_stat - expected_stat) / (abs(expected_stat) + 1e-9)

    assert error <= threshold, (
        f"test_statistic metric failure: agent value {agent_stat} differs from "
        f"expected {expected_stat} by {error*100:.3f}% (threshold is {threshold*100}%)."
    )

def test_vendored_package_fixed():
    setup_path = '/app/vendored/struct-stats-1.1.0/setup.py'
    assert os.path.exists(setup_path), f"Setup file missing at {setup_path}"

    with open(setup_path, 'r') as f:
        content = f.read()

    assert 'numpy==0.1.0' not in content, "The impossible dependency numpy==0.1.0 is still present in setup.py."