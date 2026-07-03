# test_final_state.py

import os
import pytest

def test_best_score_file():
    """Check that the best_score.txt file exists and contains the correct MSE score."""
    score_file = '/home/user/best_score.txt'

    assert os.path.isfile(score_file), f"The file {score_file} does not exist. Did you run the script?"

    with open(score_file, 'r') as f:
        content = f.read().strip()

    assert content == "0.2974", (
        f"Expected score '0.2974' in {score_file}, but found '{content}'. "
        "Did you fix the schema enforcement bug so that 'y' is treated as a float?"
    )

def test_results_png_file():
    """Check that the results.png file exists and is not an empty/cleared plot."""
    plot_file = '/home/user/results.png'

    assert os.path.isfile(plot_file), f"The file {plot_file} does not exist. Did you run the script?"

    file_size = os.path.getsize(plot_file)
    assert file_size > 5000, (
        f"The file {plot_file} is too small ({file_size} bytes). "
        "It appears to be a blank or cleared plot. Did you fix the matplotlib bug?"
    )