# test_final_state.py

import os
import pytest

def test_posterior_means_metric():
    target_file = "/home/user/posterior_means.txt"
    assert os.path.exists(target_file), f"Error: {target_file} not found."

    with open(target_file, "r") as f:
        content = f.read().strip()

    try:
        alpha_str, beta_str = content.split(',')
        alpha_est = float(alpha_str)
        beta_est = float(beta_str)
    except Exception as e:
        pytest.fail(f"Error parsing {target_file}: {e}. Expected format: alpha_mean,beta_mean")

    true_alpha = 4.2
    true_beta = 1.5

    error = abs(alpha_est - true_alpha) + abs(beta_est - true_beta)
    threshold = 0.2

    assert error <= threshold, f"Estimated alpha={alpha_est}, beta={beta_est}. Error metric (Sum of Absolute Differences) is {error}, which is > {threshold}."

def test_fit_model_binary_exists():
    binary_path = "/home/user/fit_model"
    assert os.path.exists(binary_path), f"Error: {binary_path} not found. Ensure fit_model.cpp is compiled."
    assert os.path.isfile(binary_path), f"Error: {binary_path} is not a file."
    assert os.access(binary_path, os.X_OK), f"Error: {binary_path} is not executable."

def test_bootstrap_ci_exists_and_valid():
    ci_file = "/home/user/bootstrap_ci.txt"
    assert os.path.exists(ci_file), f"Error: {ci_file} not found."

    with open(ci_file, "r") as f:
        content = f.read().strip()

    try:
        lower_str, upper_str = content.split(',')
        lower_bound = float(lower_str)
        upper_bound = float(upper_str)
    except Exception as e:
        pytest.fail(f"Error parsing {ci_file}: {e}. Expected format: lower_bound,upper_bound")

    assert lower_bound <= upper_bound, f"Lower bound ({lower_bound}) is greater than upper bound ({upper_bound})."

def test_fit_plot_exists():
    plot_file = "/home/user/fit_plot.png"
    assert os.path.exists(plot_file), f"Error: {plot_file} not found."
    assert os.path.isfile(plot_file), f"Error: {plot_file} is not a file."
    assert os.path.getsize(plot_file) > 0, f"Error: {plot_file} is empty."