# test_final_state.py
import os
import difflib

def test_decoder_exists():
    assert os.path.isfile('/home/user/decoder.rs'), "Source code /home/user/decoder.rs is missing."
    assert os.path.isfile('/home/user/decoder'), "Compiled binary /home/user/decoder is missing."
    assert os.access('/home/user/decoder', os.X_OK), "/home/user/decoder is not executable."

def test_recovered_log_similarity():
    recovered_path = '/home/user/recovered.log'
    original_path = '/tmp/original.log'

    assert os.path.isfile(recovered_path), f"Recovered log file {recovered_path} is missing."
    assert os.path.isfile(original_path), f"Original log file {original_path} is missing."

    with open(original_path, 'r', encoding='utf-8', errors='ignore') as f:
        expected = f.read()

    with open(recovered_path, 'r', encoding='utf-8', errors='ignore') as f:
        actual = f.read()

    ratio = difflib.SequenceMatcher(None, expected, actual).ratio()
    assert ratio >= 0.99, f"Similarity ratio {ratio:.4f} is below threshold 0.99."