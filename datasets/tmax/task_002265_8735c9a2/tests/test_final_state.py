# test_final_state.py
import os
import pytest

def test_final_kl_divergence():
    output_path = '/home/user/final_kl.txt'
    assert os.path.isfile(output_path), f"Output file missing: {output_path}"

    with open(output_path, 'r') as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Could not parse '{content}' as a float in {output_path}")

    assert 0.0 <= val < 0.05, f"KL divergence {val} is outside acceptable bounds [0.0, 0.05)"