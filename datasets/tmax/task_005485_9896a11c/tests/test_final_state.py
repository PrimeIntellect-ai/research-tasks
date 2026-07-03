# test_final_state.py
import os
import re

def test_venv_and_directories():
    """Check if the virtual environment and data directory are created."""
    assert os.path.isdir("/home/user/venv"), "Virtual environment directory /home/user/venv is missing."
    assert os.path.isfile("/home/user/venv/bin/python"), "Python executable not found in /home/user/venv/bin/."
    assert os.path.isdir("/home/user/ml_data"), "Directory /home/user/ml_data is missing."

def test_results_file_structure_and_values():
    """Check if results.txt exists and contains the correct structure and approximate values."""
    results_path = "/home/user/ml_data/results.txt"
    assert os.path.isfile(results_path), f"Results file {results_path} is missing."

    with open(results_path, "r") as f:
        content = f.read()

    # Regex to match the expected format
    gamma_match = re.search(r"gamma:\s*([\d\.]+)", content)
    omega_match = re.search(r"omega:\s*([\d\.]+)", content)
    gamma_ci_match = re.search(r"gamma_ci:\s*\[([\d\.]+),\s*([\d\.]+)\]", content)
    omega_ci_match = re.search(r"omega_ci:\s*\[([\d\.]+),\s*([\d\.]+)\]", content)

    assert gamma_match, "Could not parse 'gamma: <value>' from results.txt."
    assert omega_match, "Could not parse 'omega: <value>' from results.txt."
    assert gamma_ci_match, "Could not parse 'gamma_ci: [<low>, <high>]' from results.txt."
    assert omega_ci_match, "Could not parse 'omega_ci: [<low>, <high>]' from results.txt."

    gamma = float(gamma_match.group(1))
    omega = float(omega_match.group(1))
    gamma_ci_low, gamma_ci_high = float(gamma_ci_match.group(1)), float(gamma_ci_match.group(2))
    omega_ci_low, omega_ci_high = float(omega_ci_match.group(1)), float(omega_ci_match.group(2))

    # Check approximate values (allowing for minor differences due to scipy versions)
    assert 0.45 <= gamma <= 0.55, f"Expected gamma to be around 0.5054, got {gamma}"
    assert 1.95 <= omega <= 2.05, f"Expected omega to be around 1.9995, got {omega}"

    # Check CI logic
    assert gamma_ci_low < gamma_ci_high, "gamma_ci lower bound must be less than upper bound"
    assert omega_ci_low < omega_ci_high, "omega_ci lower bound must be less than upper bound"

    assert 0.40 <= gamma_ci_low <= 0.51, f"gamma_ci low out of expected range, got {gamma_ci_low}"
    assert 0.50 <= gamma_ci_high <= 0.60, f"gamma_ci high out of expected range, got {gamma_ci_high}"

    assert 1.90 <= omega_ci_low <= 2.00, f"omega_ci low out of expected range, got {omega_ci_low}"
    assert 1.99 <= omega_ci_high <= 2.10, f"omega_ci high out of expected range, got {omega_ci_high}"