# test_final_state.py
import os
import math

def test_final_mse():
    final_mse_path = "/home/user/final_mse.txt"
    data_csv_path = "/home/user/data.csv"

    assert os.path.isfile(final_mse_path), f"{final_mse_path} does not exist. Did you save the output?"
    assert os.path.isfile(data_csv_path), f"{data_csv_path} does not exist."

    # Read the dataset
    with open(data_csv_path, "r") as f:
        lines = f.read().strip().split('\n')

    X = []
    y = []
    for line in lines:
        if not line.strip():
            continue
        parts = line.split(',')
        X.append(float(parts[0]))
        y.append(float(parts[1]))

    # Split dataset as specified (80 train, 20 test)
    X_train = X[:80]
    y_train = y[:80]
    X_test = X[80:]
    y_test = y[80:]

    # Calculate training statistics (ignoring missing values: -999.0)
    train_valid = [x for x in X_train if x != -999.0]
    train_mean = sum(train_valid) / len(train_valid)
    train_var = sum((x - train_mean)**2 for x in train_valid) / len(train_valid)
    train_std = math.sqrt(train_var)

    # Impute and normalize both train and test sets using ONLY training statistics
    X_train_norm = [((x if x != -999.0 else train_mean) - train_mean) / train_std for x in X_train]
    X_test_norm = [((x if x != -999.0 else train_mean) - train_mean) / train_std for x in X_test]

    # Fit 1D linear regression on training set
    n = len(X_train_norm)
    sum_x = sum(X_train_norm)
    sum_y = sum(y_train)
    sum_xy = sum(x * y_val for x, y_val in zip(X_train_norm, y_train))
    sum_xx = sum(x * x for x in X_train_norm)

    weight = (n * sum_xy - sum_x * sum_y) / (n * sum_xx - sum_x * sum_x)
    bias = (sum_y - weight * sum_x) / n

    # Evaluate on test set
    mse = 0.0
    for x, y_true in zip(X_test_norm, y_test):
        pred = weight * x + bias
        mse += (pred - y_true)**2
    expected_mse = mse / len(X_test_norm)

    # Read actual MSE
    with open(final_mse_path, "r") as f:
        actual_mse_str = f.read().strip()

    try:
        actual_mse = float(actual_mse_str)
    except ValueError:
        assert False, f"Could not parse the content of {final_mse_path} as a float. Content: '{actual_mse_str}'"

    # Compare with a tolerance to account for C float (single precision) vs Python float (double precision) differences
    assert math.isclose(actual_mse, expected_mse, rel_tol=1e-3), \
        f"The computed MSE ({actual_mse}) does not match the expected MSE without data leakage (~{expected_mse:.6f})."