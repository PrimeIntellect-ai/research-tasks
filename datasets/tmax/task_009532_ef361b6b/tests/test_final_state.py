# test_final_state.py

import os

def test_final_size_output():
    """Test if the final_size.txt file contains the correct aggregated size."""
    output_path = '/home/user/final_size.txt'
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist. Did your script create it?"

    with open(output_path, 'r') as f:
        content = f.read().strip()

    assert content == "2500", f"Expected the final size to be exactly 2500, but found '{content}' in {output_path}."