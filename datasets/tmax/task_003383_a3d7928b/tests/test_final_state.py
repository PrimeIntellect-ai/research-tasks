# test_final_state.py

import os
import requests
import pytest
import numpy as np
from scipy import stats

def parse_b_factors(filepath):
    b_factors = []
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith("ATOM"):
                atom_name = line[12:16].strip()
                if atom_name == "CA":
                    b_factor = float(line[60:66].strip())
                    b_factors.append(b_factor)
    return np.array(b_factors)

@pytest.fixture(scope="module")
def truth_data():
    b_factors_A = parse_b_factors("/app/data/proteinA.pdb")
    b_factors_B = parse_b_factors("/app/data/proteinB.pdb")

    ks_stat, ks_pvalue = stats.ks_2samp(b_factors_A, b_factors_B)

    kde_A = stats.gaussian_kde(b_factors_A)
    kde_B = stats.gaussian_kde(b_factors_B)

    density_A_25 = kde_A.evaluate(25.0)[0]
    density_B_30 = kde_B.evaluate(30.0)[0]

    return {
        "ks_stat": ks_stat,
        "ks_pvalue": ks_pvalue,
        "density_A_25": density_A_25,
        "density_B_30": density_B_30
    }

def test_ks_test_endpoint(truth_data):
    url = "http://127.0.0.1:8080/ks_test"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "stat" in data, f"Missing 'stat' in response: {data}"
    assert "pvalue" in data, f"Missing 'pvalue' in response: {data}"

    assert data["stat"] == pytest.approx(truth_data["ks_stat"], rel=1e-3), f"Expected stat ~ {truth_data['ks_stat']}, got {data['stat']}"
    assert data["pvalue"] == pytest.approx(truth_data["ks_pvalue"], rel=1e-3), f"Expected pvalue ~ {truth_data['ks_pvalue']}, got {data['pvalue']}"

def test_density_proteinA_endpoint(truth_data):
    url = "http://127.0.0.1:8080/density/proteinA/25.0"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "density" in data, f"Missing 'density' in response: {data}"

    assert data["density"] == pytest.approx(truth_data["density_A_25"], rel=1e-3), f"Expected density ~ {truth_data['density_A_25']}, got {data['density']}"

def test_density_proteinB_endpoint(truth_data):
    url = "http://127.0.0.1:8080/density/proteinB/30.0"
    try:
        response = requests.get(url, timeout=5)
    except requests.exceptions.RequestException as e:
        pytest.fail(f"Failed to connect to {url}: {e}")

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}. Response: {response.text}"

    data = response.json()
    assert "density" in data, f"Missing 'density' in response: {data}"

    assert data["density"] == pytest.approx(truth_data["density_B_30"], rel=1e-3), f"Expected density ~ {truth_data['density_B_30']}, got {data['density']}"