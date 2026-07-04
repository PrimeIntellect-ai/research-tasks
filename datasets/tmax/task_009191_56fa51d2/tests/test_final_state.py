# test_final_state.py
import os
import pytest

def test_bootstrap_ci_file():
    filepath = '/home/user/bootstrap_ci.txt'
    assert os.path.isfile(filepath), f"Expected file {filepath} is missing. The bootstrap CI results were not saved."

    with open(filepath, 'r') as f:
        content = f.read().strip()

    # The expected values are derived from the joined dataset:
    # values = [10.5, 12.2, 9.8, 11.1]
    # np.random.seed(42)
    # 1000 iterations of sampling with replacement (size 4) and calculating the mean
    # 2.5th and 97.5th percentiles of those means
    expected_ci = "9.8000,11.8750"

    assert content == expected_ci, f"Content of {filepath} is incorrect. Expected '{expected_ci}', got '{content}'."

def test_rmse_file():
    filepath = '/home/user/rmse.txt'
    assert os.path.isfile(filepath), f"Expected file {filepath} is missing. The RMSE result was not saved."

    with open(filepath, 'r') as f:
        content = f.read().strip()

    # The expected RMSE is derived from training a LinearRegression model on the joined dataset:
    # X = [[10.5, 2015], [12.2, 2016], [9.8, 2018], [11.1, 2019]]
    # y = [105, 120, 95, 110]
    expected_rmse = "1.7772"

    assert content == expected_rmse, f"Content of {filepath} is incorrect. Expected '{expected_rmse}', got '{content}'."