# test_final_state.py
import os
import numpy as np
import pytest

def get_analytical_posterior():
    data_path = '/app/sequence_features.csv'
    assert os.path.isfile(data_path), f"Data file {data_path} is missing."

    data = np.loadtxt(data_path, delimiter=',', skiprows=1)
    N = len(data)
    x_bar = np.mean(data, axis=0)

    Sigma = np.array([[2.0, 0.8], [0.8, 3.0]])
    Lambda = np.linalg.inv(Sigma)

    mu_0 = np.array([0.0, 0.0])
    Lambda_0 = np.linalg.inv(np.array([[10.0, 0.0], [0.0, 10.0]]))

    Lambda_n = Lambda_0 + N * Lambda
    mu_n = np.linalg.inv(Lambda_n).dot(Lambda_0.dot(mu_0) + N * Lambda.dot(x_bar))
    return mu_n

def test_posterior_mean_accuracy():
    output_path = '/home/user/posterior_mean.txt'
    assert os.path.isfile(output_path), f"Agent output file {output_path} is missing."

    try:
        with open(output_path, 'r') as f:
            content = f.read().strip().split()
            agent_mu = np.array([float(content[0]), float(content[1])])
    except Exception as e:
        pytest.fail(f"Failed to read or parse {output_path}. Ensure it contains two space-separated floats. Error: {e}")

    true_mu_n = get_analytical_posterior()
    dist = np.linalg.norm(agent_mu - true_mu_n)

    threshold = 0.05
    assert dist <= threshold, (
        f"Euclidean distance between estimated posterior mean and analytical posterior mean is too large.\n"
        f"Distance: {dist:.6f}\n"
        f"Threshold: {threshold}\n"
        f"Agent estimate: {agent_mu}\n"
        f"Analytical truth: {true_mu_n}"
    )