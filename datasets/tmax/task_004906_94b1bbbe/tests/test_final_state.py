# test_final_state.py

import os
import csv
import stat
import pytest

def test_pipeline_script_exists_and_executable():
    """Check if the master bash script exists and is executable."""
    script_path = '/home/user/run_pipeline.sh'
    assert os.path.exists(script_path), f"{script_path} does not exist."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable by the user."

def test_python_scripts_exist():
    """Check if the required Python scripts were created."""
    for script in ['pca_transform.py', 'bayesian_train_predict.py']:
        path = f'/home/user/{script}'
        assert os.path.exists(path), f"Python script {path} does not exist."
        assert os.path.isfile(path), f"{path} is not a file."

def test_generated_csv_files_exist():
    """Check if the pipeline generated the expected CSV files."""
    expected_files = [
        'train_raw.csv',
        'test_raw.csv',
        'train_pca.csv',
        'test_pca.csv',
        'predictions.csv'
    ]
    for filename in expected_files:
        path = f'/home/user/{filename}'
        assert os.path.exists(path), f"Expected generated file {path} does not exist."
        assert os.path.isfile(path), f"{path} is not a file."

def test_split_files_row_counts():
    """Verify that train_raw.csv and test_raw.csv have the correct number of rows."""
    def count_rows(filepath):
        with open(filepath, 'r', newline='') as f:
            return sum(1 for _ in f)

    train_count = count_rows('/home/user/train_raw.csv')
    test_count = count_rows('/home/user/test_raw.csv')

    # 800 data rows + 1 header = 801
    assert train_count == 801, f"train_raw.csv should have 801 rows (including header), found {train_count}."
    # 200 data rows + 1 header = 201
    assert test_count == 201, f"test_raw.csv should have 201 rows (including header), found {test_count}."

def test_predictions_format():
    """Verify predictions.csv has the correct columns and row count."""
    preds_path = '/home/user/predictions.csv'
    with open(preds_path, 'r', newline='') as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        assert headers == ['id', 'predicted_target'], f"predictions.csv headers are incorrect: {headers}"

        row_count = sum(1 for _ in reader)
        assert row_count == 200, f"predictions.csv should have 200 data rows, found {row_count}."

def test_mse_calculation():
    """Verify that the MSE calculated by the bash script matches the actual MSE of the predictions."""
    mse_file = '/home/user/mse_result.txt'
    assert os.path.exists(mse_file), f"{mse_file} does not exist."

    with open(mse_file, 'r') as f:
        content = f.read().strip()

    try:
        reported_mse = float(content)
    except ValueError:
        pytest.fail(f"Content of {mse_file} is not a valid float: '{content}'")

    # Calculate the actual MSE from predictions and test_raw
    preds = {}
    with open('/home/user/predictions.csv', 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            preds[row['id']] = float(row['predicted_target'])

    actual_targets = {}
    with open('/home/user/test_raw.csv', 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            actual_targets[row['id']] = float(row['target'])

    assert len(preds) == len(actual_targets), "Mismatch in number of predictions and actual targets."

    squared_errors = []
    for id_val, pred_val in preds.items():
        assert id_val in actual_targets, f"ID {id_val} from predictions not found in test_raw.csv"
        actual_val = actual_targets[id_val]
        squared_errors.append((pred_val - actual_val) ** 2)

    calculated_mse = sum(squared_errors) / len(squared_errors)
    expected_mse_str = f"{calculated_mse:.2f}"

    # Check if the reported MSE matches the expected rounded MSE
    assert content == expected_mse_str, f"Reported MSE in {mse_file} ({content}) does not match the computed MSE rounded to 2 decimal places ({expected_mse_str})."