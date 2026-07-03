# test_final_state.py
import os
import csv
import pytest

def test_executable_exists():
    executable = "/home/user/model_trainer"
    assert os.path.isfile(executable), f"{executable} does not exist."
    assert os.access(executable, os.X_OK), f"{executable} is not executable."

def test_bash_script_exists():
    script = "/home/user/run_experiments.sh"
    assert os.path.isfile(script), f"{script} does not exist."
    assert os.access(script, os.X_OK), f"{script} is not executable."

def test_experiments_csv_contents():
    csv_file = "/home/user/experiments.csv"
    assert os.path.isfile(csv_file), f"{csv_file} does not exist."

    expected_lrs = [0.01, 0.05, 0.1]
    results = {}

    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if not row:
                continue
            assert len(row) == 2, f"Expected exactly 2 columns in CSV, got {len(row)}: {row}"
            try:
                lr = float(row[0])
                loss = float(row[1])
                # Store by string formatted to avoid float key issues, or just use close match
                # We'll store in a list and match later, or just round the key
                results[round(lr, 3)] = loss
            except ValueError:
                pytest.fail(f"Could not parse row as floats: {row}")

    for lr in expected_lrs:
        lr_key = round(lr, 3)
        assert lr_key in results, f"Learning rate {lr} not found in {csv_file}"

        expected_loss = 100.0 / (1.0 + lr * 100.5)
        actual_loss = results[lr_key]

        # Check that it's close to the expected precision value
        assert abs(actual_loss - expected_loss) < 0.01, \
            f"Loss for LR {lr} is {actual_loss}, expected ~{expected_loss:.4f}. Precision might be lost."

        # Explicitly check it's not the truncated integer value
        truncated_loss = float(int(expected_loss))
        assert abs(actual_loss - truncated_loss) > 0.01, \
            f"Loss for LR {lr} appears to be truncated to {truncated_loss}. The bug in the C++ code was not properly fixed."