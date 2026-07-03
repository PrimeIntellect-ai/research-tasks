# test_final_state.py

import os
import json
import numpy as np
from scipy.stats import multivariate_normal
import pytest

def test_evaluate_models_script_exists():
    script_path = "/home/user/evaluate_models.py"
    assert os.path.isfile(script_path), f"The script {script_path} was not created."

def test_results_json_exists_and_valid():
    json_path = "/home/user/results.json"
    assert os.path.isfile(json_path), f"The results file {json_path} was not created."

    with open(json_path, 'r') as f:
        try:
            results = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {json_path} does not contain valid JSON.")

    expected_keys = {
        "lambda_extracted",
        "bic_model1_full_reg",
        "bic_model2_diag",
        "best_model_test_nll"
    }

    missing_keys = expected_keys - set(results.keys())
    assert not missing_keys, f"The results.json is missing keys: {missing_keys}"

def test_extracted_lambda():
    json_path = "/home/user/results.json"
    if not os.path.isfile(json_path):
        pytest.skip("results.json not found.")

    with open(json_path, 'r') as f:
        results = json.load(f)

    lambda_extracted = results.get("lambda_extracted")
    assert lambda_extracted is not None, "lambda_extracted is missing."

    assert np.isclose(lambda_extracted, 0.035, atol=1e-5), \
        f"Incorrect lambda extracted. Expected ~0.035, got {lambda_extracted}"

def test_best_model_test_nll():
    json_path = "/home/user/results.json"
    if not os.path.isfile(json_path):
        pytest.skip("results.json not found.")

    with open(json_path, 'r') as f:
        results = json.load(f)

    agent_nll = results.get("best_model_test_nll")
    assert agent_nll is not None, "best_model_test_nll is missing."

    train_data_path = "/app/train_data.npy"
    test_data_path = "/app/test_data.npy"

    assert os.path.isfile(train_data_path), f"Missing {train_data_path}"
    assert os.path.isfile(test_data_path), f"Missing {test_data_path}"

    X_train = np.load(train_data_path)
    X_test = np.load(test_data_path)
    N, D = X_train.shape

    mu = np.mean(X_train, axis=0)
    cov_sample = np.cov(X_train, rowvar=False, bias=True)
    cov_reg = cov_sample + 0.035 * np.eye(D)

    mvn_reg = multivariate_normal(mean=mu, cov=cov_reg)
    target_nll = -np.sum(mvn_reg.logpdf(X_test))

    error = abs(agent_nll - target_nll)
    assert error <= 2.0, \
        f"NLL error {error} exceeds threshold of 2.0. Expected ~{target_nll}, but got {agent_nll}"