# test_final_state.py
import os

def test_training_data_exists():
    assert os.path.exists("/home/user/training_data.csv"), "training_data.csv was not generated."

def test_optimize_script_exists():
    assert os.path.exists("/home/user/optimize.sh"), "optimize.sh script is missing."
    assert os.path.isfile("/home/user/optimize.sh"), "optimize.sh is not a file."

def test_weights_csv_exists_and_correct():
    weights_file = "/home/user/weights.csv"
    assert os.path.exists(weights_file), f"The file {weights_file} is missing."

    with open(weights_file, 'r') as f:
        content = f.read().strip()

    assert content, f"The file {weights_file} is empty."

    parts = content.split(',')
    assert len(parts) == 3, f"The file {weights_file} must contain exactly 3 comma-separated values (w1,w2,b)."

    try:
        w1, w2, b = map(float, parts)
    except ValueError:
        raise AssertionError(f"The values in {weights_file} could not be parsed as floats: {content}")

    assert abs(w1 - 4.5) < 0.1, f"w1 ({w1}) is not within 0.1 of the expected value 4.5"
    assert abs(w2 - (-2.0)) < 0.1, f"w2 ({w2}) is not within 0.1 of the expected value -2.0"
    assert abs(b - 1.5) < 0.1, f"b ({b}) is not within 0.1 of the expected value 1.5"