# test_final_state.py

import os
import pytest

def test_prob_file_exists_and_correct():
    """Check if /home/user/prob_B_better.txt exists and contains the correct probability."""
    prob_path = '/home/user/prob_B_better.txt'
    assert os.path.isfile(prob_path), f"Missing file: {prob_path}"

    with open(prob_path, 'r') as f:
        content = f.read().strip()

    assert content == "0.9839", f"Expected probability '0.9839', but found '{content}' in {prob_path}"

def test_plot_file_exists_and_not_blank():
    """Check if /home/user/posterior_plot.png exists and is not a blank image."""
    plot_path = '/home/user/posterior_plot.png'
    assert os.path.isfile(plot_path), f"Missing file: {plot_path}"

    # A blank matplotlib canvas is very small. A plot with data should be > 5KB.
    file_size = os.path.getsize(plot_path)
    assert file_size > 5000, f"Plot file {plot_path} is too small ({file_size} bytes), likely blank."