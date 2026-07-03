# test_final_state.py
import os
import math

def test_top_pc_file_exists():
    """Check if the output file was created."""
    file_path = "/home/user/top_pc.txt"
    assert os.path.exists(file_path), f"{file_path} does not exist."
    assert os.path.isfile(file_path), f"{file_path} is not a file."

def test_top_pc_content():
    """Check if the output file contains the correct principal component."""
    file_path = "/home/user/top_pc.txt"
    with open(file_path, "r") as f:
        content = f.read().strip()

    assert content, f"The file {file_path} is empty."

    parts = [p.strip() for p in content.split(",")]
    assert len(parts) == 3, f"Expected 3 comma-separated values in {file_path}, got {len(parts)}."

    expected = [0.3533, 0.6121, 0.7071]
    for i in range(3):
        try:
            val = float(parts[i])
        except ValueError:
            assert False, f"Could not parse '{parts[i]}' as a float."

        assert math.isclose(val, expected[i], abs_tol=0.0002), (
            f"Value at index {i} is {val}, expected {expected[i]} (within 0.0002 tolerance)."
        )