# test_final_state.py
import os

def test_accuracy_file():
    accuracy_file = '/home/user/accuracy.txt'
    assert os.path.isfile(accuracy_file), f"The file {accuracy_file} does not exist. Did you run the modified script?"

    with open(accuracy_file, 'r') as f:
        content = f.read().strip()

    assert content == "0.7700", f"Expected accuracy to be '0.7700' after fixing data leakage, but got '{content}'. Ensure the scaler is only fitted on the training data."

def test_train_script_fixed():
    script_path = '/home/user/train.py'
    assert os.path.isfile(script_path), f"The script {script_path} does not exist."

    with open(script_path, 'r') as f:
        content = f.read()

    assert 'scaler.fit_transform(X)' not in content, "The script still contains data leakage: `scaler.fit_transform(X)` was found before splitting."
    assert 'scaler.fit(X)' not in content, "The script still contains data leakage: `scaler.fit(X)` was found before splitting."