# test_final_state.py

import os
import math
import pytest

def calc_entropy(data):
    if not data:
        return 0
    entropy = 0
    for x in set(data):
        p_x = float(data.count(x)) / len(data)
        entropy += - p_x * math.log(p_x, 2)
    return entropy

def test_decoder_cpp_exists():
    """Verify that the user created the decoder.cpp file."""
    decoder_path = "/home/user/decoder.cpp"
    assert os.path.exists(decoder_path), f"File not found: {decoder_path}"
    assert os.path.isfile(decoder_path), f"Path is not a file: {decoder_path}"

def test_entropy_calculation_accuracy():
    """Verify that the entropy calculated by the agent is within the acceptable tolerance."""
    entropy_file_path = "/home/user/entropy.txt"
    assert os.path.exists(entropy_file_path), f"File not found: {entropy_file_path}"

    try:
        with open(entropy_file_path, 'r') as f:
            content = f.read().strip()
            agent_entropy = float(content)
    except ValueError:
        pytest.fail(f"Could not parse a floating-point number from {entropy_file_path}. Content was: '{content}'")
    except Exception as e:
        pytest.fail(f"Failed to read {entropy_file_path}: {e}")

    true_string = "EXFIL_DATA_CONFIDENTIAL_9921"
    true_entropy = calc_entropy(true_string)

    diff = abs(true_entropy - agent_entropy)
    tolerance = 0.01

    assert diff <= tolerance, (
        f"Metric failed: Absolute difference between true entropy ({true_entropy}) "
        f"and agent entropy ({agent_entropy}) is {diff}, which is greater than the tolerance of {tolerance}."
    )