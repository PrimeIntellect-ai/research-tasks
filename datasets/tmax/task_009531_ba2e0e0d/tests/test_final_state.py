# test_final_state.py
import os

def test_energy_diff_file():
    """Verify that energy_diff.txt exists and contains a value less than 1.0."""
    diff_file = "/home/user/energy_diff.txt"
    assert os.path.exists(diff_file), f"File {diff_file} does not exist."

    with open(diff_file, "r") as f:
        content = f.read().strip()

    assert content, f"File {diff_file} is empty."

    try:
        diff_value = float(content)
    except ValueError:
        assert False, f"Content of {diff_file} ('{content}') cannot be parsed as a float."

    assert diff_value < 1.0, f"Energy difference {diff_value} is not less than 1.0."

def test_dominant_freq_file():
    """Verify that dominant_freq.txt exists and contains the correct dominant frequency."""
    freq_file = "/home/user/dominant_freq.txt"
    assert os.path.exists(freq_file), f"File {freq_file} does not exist."

    with open(freq_file, "r") as f:
        content = f.read().strip()

    assert content, f"File {freq_file} is empty."

    try:
        freq_value = int(float(content))
    except ValueError:
        assert False, f"Content of {freq_file} ('{content}') cannot be parsed as an integer."

    assert freq_value == 50, f"Expected dominant frequency to be 50, but got {freq_value}."

def test_analyze_signal_script_exists():
    """Verify that analyze_signal.py still exists."""
    script_file = "/home/user/analyze_signal.py"
    assert os.path.exists(script_file), f"File {script_file} does not exist. You should have modified it, not deleted it."