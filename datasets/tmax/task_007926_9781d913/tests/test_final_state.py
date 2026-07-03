# test_final_state.py

import os
import re

def test_energy_log_exists():
    log_path = "/home/user/energy.log"
    assert os.path.exists(log_path), f"The log file {log_path} does not exist. Did you run the script?"
    assert os.path.isfile(log_path), f"The path {log_path} is not a file."

def test_energy_log_content():
    log_path = "/home/user/energy.log"
    with open(log_path, 'r') as f:
        content = f.read().strip()

    assert content.startswith("Converged:"), f"The log file does not indicate successful convergence. Content: '{content}'"

    match = re.search(r"Converged:\s*([0-9.]+)", content)
    assert match is not None, "Could not parse the converged value from the log file."

    val_str = match.group(1)
    try:
        val = float(val_str)
    except ValueError:
        raise AssertionError(f"The converged value '{val_str}' is not a valid float.")

    # The true integral of exp(-x^2/2) from -5 to 5 is approximately 2.506628
    expected_val = 2.5066
    tolerance = 0.005

    assert abs(val - expected_val) <= tolerance, (
        f"The converged value {val} is not close enough to the expected integral value (~2.5066). "
        "Check your integration logic or bounds."
    )