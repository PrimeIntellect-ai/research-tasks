# test_final_state.py
import os

def test_precision_trigger_file():
    filepath = '/home/user/precision_trigger.txt'
    assert os.path.isfile(filepath), f"File {filepath} does not exist."

    with open(filepath, 'r') as f:
        content = f.read().strip()

    assert content == "1337.42", f"Expected precision trigger to be '1337.42', but got '{content}'."

def test_crash_trigger_file():
    filepath = '/home/user/crash_trigger.txt'
    assert os.path.isfile(filepath), f"File {filepath} does not exist."

    with open(filepath, 'r') as f:
        content = f.read().strip()

    assert content == "8888.88", f"Expected crash trigger to be '8888.88', but got '{content}'."