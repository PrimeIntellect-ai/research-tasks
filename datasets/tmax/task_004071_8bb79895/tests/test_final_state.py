# test_final_state.py
import os
import re

def test_source_files_exist():
    """Check that the required source files and scripts have been created."""
    assert os.path.isfile("/home/user/heat.c"), "/home/user/heat.c is missing."
    assert os.path.isfile("/home/user/regression.c"), "/home/user/regression.c is missing."

def test_script_exists_and_executable():
    """Check that the bash script exists and is executable."""
    script_path = "/home/user/run_simulation.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

def test_convergence_rate_output():
    """Check that the convergence rate output file exists and contains the correct slope."""
    output_path = "/home/user/convergence_rate.txt"
    assert os.path.isfile(output_path), f"{output_path} is missing. The simulation may not have run successfully."

    with open(output_path, "r") as f:
        content = f.read().strip()

    # Look for the required format: "Slope: %.3f"
    match = re.search(r"Slope:\s*(-?\d+\.\d+)", content)
    assert match is not None, f"Could not find the expected 'Slope: <value>' format in {output_path}. Content was: '{content}'"

    slope = float(match.group(1))
    # The theoretical spatial order of accuracy for FTCS is O(dx^2), so slope should be very close to -2.0
    assert abs(slope - (-2.0)) < 0.05, f"Expected slope to be near -2.000, but got {slope:.3f}"