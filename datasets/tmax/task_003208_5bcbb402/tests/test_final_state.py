# test_final_state.py

import os
import stat
import pytest

def test_pipeline_script_exists_and_executable():
    """Test that pipeline.sh exists and is executable."""
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    st = os.stat(script_path)
    is_executable = bool(st.st_mode & stat.S_IXUSR)
    assert is_executable, f"Script {script_path} is not executable."

def test_total_energy_output():
    """Test that the total_energy.txt contains the correct computed value."""
    output_path = "/home/user/total_energy.txt"
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, "r") as f:
        content = f.read().strip()

    # Recompute the expected value to be robust
    matches = [14, 14, 18, 12, 18, 16]
    seed = 123
    total_energy = 0.0

    for L in matches:
        sum_y = 0.0
        for _ in range(1000):
            seed = (1103515245 * seed + 12345) % 2147483648
            r = seed / 2147483648
            x = r * L
            y = (x * x) / L
            sum_y += y

        integral = (sum_y / 1000.0) * L
        total_energy += integral

    expected_output = f"{total_energy:.2f}"

    assert content == expected_output, f"Output file {output_path} contains '{content}', expected '{expected_output}'."