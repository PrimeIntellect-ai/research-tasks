# test_final_state.py
import os
import pytest

def test_posterior_file_exists():
    assert os.path.isfile("/home/user/posterior.txt"), "The file /home/user/posterior.txt does not exist."

def test_posterior_value():
    # Dynamically calculate the expected value based on the CSV file
    data_file = "/home/user/processed/data.csv"
    assert os.path.isfile(data_file), f"Data file {data_file} is missing."

    with open(data_file, "r") as f:
        lines = f.read().strip().split("\n")

    assert len(lines) > 1, "Data file is empty or missing rows."

    header = lines[0].split(",")
    try:
        user_id_idx = header.index("user_id")
    except ValueError:
        pytest.fail("Column 'user_id' not found in data.csv header.")

    total_tx = len(lines) - 1
    corrupt_tx = 0

    for line in lines[1:]:
        cols = line.split(",")
        if len(cols) > user_id_idx:
            user_id_val = cols[user_id_idx]
            if "." in user_id_val or "NaN" in user_id_val:
                corrupt_tx += 1

    assert total_tx > 0, "No transactions found."
    assert corrupt_tx > 0, "No corrupted transactions found."

    p_corrupt = corrupt_tx / total_tx
    p_fraud = 0.05
    p_corrupt_given_fraud = 0.80

    # P(Fraud|Corrupt) = (P(Corrupt|Fraud) * P(Fraud)) / P(Corrupt)
    p_fraud_given_corrupt = (p_corrupt_given_fraud * p_fraud) / p_corrupt

    # bc with scale=4 truncates, it does not round.
    # We can simulate bc truncation to 4 decimal places
    expected_val_str = f"{p_fraud_given_corrupt:.5f}"[:-1]

    with open("/home/user/posterior.txt", "r") as f:
        actual_val = f.read().strip()

    # Accept both '0.3333' and '.3333' (bc default behavior)
    acceptable_values = [expected_val_str, expected_val_str.lstrip("0")]

    assert actual_val in acceptable_values, (
        f"Expected posterior value to be one of {acceptable_values} (derived from "
        f"{corrupt_tx} corrupted out of {total_tx} total transactions), but got '{actual_val}'."
    )

def test_script_exists():
    script_path = "/home/user/analyze_pipeline.sh"
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."