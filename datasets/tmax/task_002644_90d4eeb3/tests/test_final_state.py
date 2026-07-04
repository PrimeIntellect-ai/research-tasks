# test_final_state.py
import os

def test_script_exists():
    """Check that the Python script was created."""
    assert os.path.isfile("/home/user/duffing_mc.py"), "The script /home/user/duffing_mc.py does not exist."

def test_output_file_exists_and_valid():
    """Check that the output file exists and contains a valid float rounded to 3 decimal places."""
    output_path = "/home/user/dominant_freq.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} does not exist."

    with open(output_path, 'r') as f:
        content = f.read().strip()

    assert content != "", "The output file is empty."

    try:
        val = float(content)
    except ValueError:
        assert False, f"The content of {output_path} is not a valid float: '{content}'"

    # Check if it has 3 decimal places (if there is a decimal point)
    if '.' in content:
        decimals = content.split('.')[1]
        assert len(decimals) == 3, f"Expected 3 decimal places, found {len(decimals)} in '{content}'"
    else:
        # If it's an integer like "1", it should be "1.000"
        assert False, f"Expected 3 decimal places, but no decimal point found in '{content}'"

    # The driving frequency is 1.2 rad/s -> ~0.191 Hz. 
    # The dominant frequency should be somewhere around this range.
    assert 0.0 < val < 1.0, f"The dominant frequency {val} is outside the expected physical range (0.0, 1.0) Hz."