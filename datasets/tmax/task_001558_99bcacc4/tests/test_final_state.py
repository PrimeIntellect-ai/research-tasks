# test_final_state.py
import os

def test_pipeline_script_exists_and_executable():
    path = '/home/user/pipeline.sh'
    assert os.path.exists(path), f"{path} does not exist."
    assert os.access(path, os.X_OK), f"{path} is not executable."

def test_python_scripts_exist():
    for script in ['pca.py', 'train.py']:
        path = f'/home/user/{script}'
        assert os.path.exists(path), f"{path} does not exist."

def test_csv_splits():
    train_path = '/home/user/train.csv'
    test_path = '/home/user/test.csv'

    assert os.path.exists(train_path), f"{train_path} does not exist."
    assert os.path.exists(test_path), f"{test_path} does not exist."

    with open(train_path, 'r') as f:
        train_lines = sum(1 for _ in f)
    assert train_lines == 800, f"Expected 800 lines in {train_path}, found {train_lines}."

    with open(test_path, 'r') as f:
        test_lines = sum(1 for _ in f)
    assert test_lines == 200, f"Expected 200 lines in {test_path}, found {test_lines}."

def test_accuracy_result():
    path = '/home/user/accuracy.txt'
    assert os.path.exists(path), f"{path} does not exist."

    with open(path, 'r') as f:
        content = f.read().strip()

    try:
        accuracy = float(content)
    except ValueError:
        assert False, f"Could not parse '{content}' as a float in {path}."

    assert abs(accuracy - 0.825) < 1e-4, f"Expected accuracy to be 0.825, but got {accuracy}."