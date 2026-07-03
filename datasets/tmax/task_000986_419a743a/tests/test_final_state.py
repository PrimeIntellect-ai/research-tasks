# test_final_state.py
import os

def test_db_secret_file():
    path = '/home/user/db_secret.txt'
    assert os.path.isfile(path), f"File {path} does not exist. You need to create it."
    with open(path, 'r') as f:
        content = f.read().strip()
    assert content == 'auth_token_xyz987', "The file db_secret.txt does not contain the correct recovered password."

def test_train_model_sql_query():
    path = '/home/user/ml_project/train_model.py'
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read()

    # Check if the query filters out the -999.0 values
    content_upper = content.upper()
    assert 'WHERE' in content_upper and '999' in content, "The SQL query in train_model.py does not appear to filter out the corrupted rows (target = -999.0)."

def test_train_model_learning_rate():
    path = '/home/user/ml_project/train_model.py'
    assert os.path.isfile(path), f"File {path} does not exist."
    with open(path, 'r') as f:
        content = f.read()

    # Check if the learning rate was changed to 0.01
    assert '0.01' in content, "The learning rate in train_model.py does not appear to be updated to 0.01."

def test_diagnostics_log():
    path = '/home/user/diagnostics.log'
    assert os.path.isfile(path), f"File {path} does not exist. Did you run the script successfully?"
    with open(path, 'r') as f:
        content = f.read().strip()

    assert content.startswith('Loss:'), "diagnostics.log does not contain the expected 'Loss: ' prefix."

    try:
        loss_str = content.split('Loss:')[1].strip()
        loss_val = float(loss_str)
    except (IndexError, ValueError):
        assert False, "Could not parse a valid numerical loss value from diagnostics.log."

    assert loss_val < 1.0, f"The loss value ({loss_val}) is too high. The model did not converge properly."