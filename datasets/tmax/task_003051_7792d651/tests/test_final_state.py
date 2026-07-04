# test_final_state.py

import os

def test_influencers_file_exists():
    """Verify that the influencers.csv file exists."""
    assert os.path.isfile('/home/user/influencers.csv'), "The file /home/user/influencers.csv was not found."

def test_influencers_file_content():
    """Verify that the influencers.csv file contains the correct top 3 managers and path counts."""
    file_path = '/home/user/influencers.csv'
    assert os.path.isfile(file_path), "The file /home/user/influencers.csv is missing."

    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "10,5",
        "20,4",
        "30,2"
    ]

    assert len(lines) == 3, f"Expected exactly 3 lines in the output, but found {len(lines)}."

    for i, (actual, expected) in enumerate(zip(lines, expected_lines)):
        assert actual == expected, f"Line {i+1} is incorrect. Expected '{expected}', got '{actual}'."