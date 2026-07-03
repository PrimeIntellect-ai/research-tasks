# test_final_state.py

import os
import re

def test_profile_results_exists_and_format():
    """Test that profile_results.txt exists and contains cProfile output."""
    file_path = '/home/user/profile_results.txt'
    assert os.path.isfile(file_path), f"Missing file: {file_path}"

    with open(file_path, 'r') as f:
        content = f.read()

    # Check for standard cProfile headers
    assert 'ncalls' in content and 'tottime' in content and 'cumtime' in content, \
        f"File {file_path} does not appear to contain valid cProfile output."

def test_fast_sim_exists():
    """Test that the fast_sim.py script exists."""
    file_path = '/home/user/fast_sim.py'
    assert os.path.isfile(file_path), f"Missing file: {file_path}"

def test_result_txt_exists_and_correct():
    """Test that result.txt exists and contains a float within the acceptable range."""
    file_path = '/home/user/result.txt'
    assert os.path.isfile(file_path), f"Missing file: {file_path}"

    with open(file_path, 'r') as f:
        content = f.read().strip()

    try:
        prob = float(content)
    except ValueError:
        assert False, f"File {file_path} does not contain a valid float. Found: {content}"

    # The expected probability is around 0.18. Acceptable range: 0.16 to 0.20
    assert 0.16 <= prob <= 0.20, \
        f"Probability in {file_path} is {prob}, which is outside the acceptable range [0.16, 0.20]."