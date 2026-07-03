# test_final_state.py

import os
import hashlib
import pytest

def test_recovered_pins_accuracy():
    log_path = "/home/user/redirect_logs.txt"
    recovered_path = "/home/user/recovered_pins.txt"

    assert os.path.exists(log_path), f"Original log file {log_path} is missing."
    assert os.path.exists(recovered_path), f"Recovered PINs file {recovered_path} is missing."

    with open(log_path, "r") as f:
        expected_lines = [l.strip().split(',') for l in f.readlines() if l.strip()]

    expected_dict = {k: v for k, v in expected_lines}
    assert len(expected_dict) > 0, "Original log file is empty or invalid."

    try:
        with open(recovered_path, "r") as f:
            recovered_lines = [l.strip() for l in f.readlines() if l.strip()]
    except Exception as e:
        pytest.fail(f"Could not read {recovered_path}: {e}")

    correct = 0
    for line in recovered_lines:
        try:
            parts = line.split(',')
            if len(parts) == 2:
                thumb, pin = parts
                if thumb in expected_dict:
                    target_hash = expected_dict[thumb]
                    test_str = f"{thumb}:{pin}".encode('utf-8')
                    if hashlib.md5(test_str).hexdigest() == target_hash:
                        correct += 1
        except Exception:
            pass

    accuracy = correct / len(expected_dict)

    assert accuracy >= 0.99, f"Accuracy {accuracy:.2%} is below the threshold of 99.0%. Correctly recovered {correct} out of {len(expected_dict)} PINs."