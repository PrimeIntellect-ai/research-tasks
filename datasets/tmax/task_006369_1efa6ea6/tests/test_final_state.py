# test_final_state.py
import os
import csv
import subprocess
import stat

def test_bash_script_exists_and_executable():
    script_path = '/home/user/test_repro.sh'
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

def test_bash_script_execution():
    script_path = '/home/user/test_repro.sh'
    result = subprocess.run(['bash', script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"{script_path} failed to execute successfully. stderr: {result.stderr}"

def test_encoded_files_exist():
    assert os.path.isfile('/home/user/train_encoded.csv'), "train_encoded.csv is missing."
    assert os.path.isfile('/home/user/test_encoded.csv'), "test_encoded.csv is missing."

def test_encoded_values():
    # Expected values derived from the 80/20 split of the dataset
    # Train: first 8 rows
    # Test: last 2 rows
    # Global mean (train) = 4.0 / 8 = 0.5
    # Prior weight = 10.0
    # A encoded = (3 * (2/3) + 10 * 0.5) / 13 = 7 / 13 ≈ 0.5385
    # B encoded = (3 * (2/3) + 10 * 0.5) / 13 = 7 / 13 ≈ 0.5385
    # C encoded = (2 * 0 + 10 * 0.5) / 12 = 5 / 12 ≈ 0.4167
    # D encoded (unseen) = 0.5

    expected_train = {
        '1': '0.538', # Check prefix to avoid strict rounding issues
        '2': '0.538',
        '3': '0.538',
        '4': '0.416',
        '5': '0.538',
        '6': '0.538',
        '7': '0.538',
        '8': '0.416',
    }

    expected_test = {
        '9': '0.538',
        '10': '0.500',
    }

    with open('/home/user/train_encoded.csv', 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 8, "train_encoded.csv should have exactly 8 data rows."
        for row in rows:
            assert 'encoded_feature' in row, "Missing 'encoded_feature' column in train_encoded.csv"
            expected_prefix = expected_train[row['id']]
            assert row['encoded_feature'].startswith(expected_prefix), \
                f"Row {row['id']} in train_encoded.csv has wrong encoded_feature. Expected starting with {expected_prefix}, got {row['encoded_feature']}"

    with open('/home/user/test_encoded.csv', 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert len(rows) == 2, "test_encoded.csv should have exactly 2 data rows."
        for row in rows:
            assert 'encoded_feature' in row, "Missing 'encoded_feature' column in test_encoded.csv"
            expected_prefix = expected_test[row['id']]
            assert row['encoded_feature'].startswith(expected_prefix), \
                f"Row {row['id']} in test_encoded.csv has wrong encoded_feature. Expected starting with {expected_prefix}, got {row['encoded_feature']}"