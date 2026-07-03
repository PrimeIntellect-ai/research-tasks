# test_final_state.py

import os
import pytest

def test_pdf_eval_compiled_and_executable():
    """Verify that pdf_eval is compiled and executable."""
    executable_path = "/home/user/bin/pdf_eval"
    assert os.path.isfile(executable_path), f"Executable {executable_path} does not exist."
    assert os.access(executable_path, os.X_OK), f"File {executable_path} is not executable."

def test_scripts_exist_and_executable():
    """Verify that the required bash scripts exist and are executable."""
    scripts = [
        "/home/user/scripts/integrate.sh",
        "/home/user/scripts/monte_carlo.sh"
    ]
    for script in scripts:
        assert os.path.isfile(script), f"Script {script} does not exist."
        assert os.access(script, os.X_OK), f"Script {script} is not executable."

def test_integral_output():
    """Verify that integral.txt exists and contains a correct value."""
    output_file = "/home/user/data/integral.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    with open(output_file, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {output_file} is not a valid float: '{content}'")

    assert 3.74 < val < 3.77, f"Integral value {val} is not within the expected range (3.74, 3.77)."

def test_monte_carlo_output():
    """Verify that mc_area.txt exists and contains a correct value."""
    output_file = "/home/user/data/mc_area.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} does not exist."

    with open(output_file, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {output_file} is not a valid float: '{content}'")

    assert 3.4 < val < 4.1, f"Monte Carlo area estimate {val} is not within the expected range (3.4, 4.1)."