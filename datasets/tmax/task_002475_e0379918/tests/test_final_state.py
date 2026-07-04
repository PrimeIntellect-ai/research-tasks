# test_final_state.py

import os
import json
import pytest

def test_result_json_metric():
    result_path = '/home/user/result.json'
    assert os.path.isfile(result_path), f"Expected result file {result_path} does not exist."

    with open(result_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {result_path} is not valid JSON.")

    assert 'mu' in data, "Key 'mu' missing from result.json"
    assert 'sigma' in data, "Key 'sigma' missing from result.json"
    assert 'kl_divergence' in data, "Key 'kl_divergence' missing from result.json"

    mu_opt = data['mu']
    sigma_opt = data['sigma']

    true_mu = 6.2
    true_sigma = 2.5

    error = abs(mu_opt - true_mu) + abs(sigma_opt - true_sigma)
    assert error < 0.1, f"Metric threshold failed: MAE(mu) + MAE(sigma) = {error} which is not < 0.1"

def test_distmetric_go_mod_fixed():
    path = "/app/distmetric/go.mod"
    assert os.path.isfile(path), f"Expected file {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    assert "github.com/scicomp/distmetric" in content, f"Expected correct module name 'github.com/scicomp/distmetric' not found in {path}."
    assert "github.com/scicompp/distmetric" not in content, f"Typo 'scicompp' is still present in {path}."

def test_distmetric_kl_go_fixed():
    path = "/app/distmetric/kl.go"
    assert os.path.isfile(path), f"Expected file {path} does not exist."

    with open(path, 'r') as f:
        content = f.read()

    assert "p[i] * math.Log(p[i]/q[i])" in content.replace(" ", ""), f"Expected fixed logic 'p[i]*math.Log(p[i]/q[i])' not found in {path}."
    assert "p[i] * math.Log(q[i]/p[i])" not in content.replace(" ", ""), f"Logic error 'p[i]*math.Log(q[i]/p[i])' is still present in {path}."