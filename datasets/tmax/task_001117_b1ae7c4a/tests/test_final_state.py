# test_final_state.py

import os
import re

def test_solution_file_exists():
    """Verify that the solution file exists."""
    assert os.path.isfile('/home/user/solution.txt'), "/home/user/solution.txt is missing."

def test_solution_content():
    """Verify that the solution file contains the correctly rounded optimized value."""
    with open('/home/user/solution.txt', 'r') as f:
        content = f.read().strip()

    assert content == "2.00", f"Expected the solution file to contain exactly '2.00', but found '{content}'."

def test_gd_optimizer_modified():
    """Verify that the gradient descent script was modified to apply learning rate decay."""
    script_path = '/home/user/gd_optimizer.sh'
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

    with open(script_path, 'r') as f:
        content = f.read()

    # Check if the learning rate decay logic (multiplying by 0.5) was added
    assert "0.5" in content, "The script /home/user/gd_optimizer.sh does not appear to multiply the learning rate by 0.5 as requested."
    assert "bc -l" in content, "The script does not appear to use 'bc -l' for the math operations."