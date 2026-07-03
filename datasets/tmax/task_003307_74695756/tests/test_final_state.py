# test_final_state.py
import os
import re
import pytest

def test_results_exist_and_valid():
    results_file = "/home/user/results.txt"
    assert os.path.isfile(results_file), f"{results_file} does not exist. Did you run the compiled simulator?"

    with open(results_file, "r") as f:
        content = f.read()

    assert "nan" not in content.lower(), "Output contains NaN. The integration likely diverged due to an incorrect step size."

    # Parse KL divergence
    kl_match = re.search(r"KL_Divergence:\s*\[([0-9\.]+)\]", content)
    assert kl_match is not None, "Could not parse KL_Divergence from results.txt. Make sure the format matches exactly."

    kl_value = float(kl_match.group(1))
    assert kl_value < 0.01, f"KL Divergence is too high: {kl_value} (expected < 0.01). The empirical distribution did not converge to the theoretical one."

    # Parse Theoretical
    theo_match = re.search(r"Theoretical:\s*\[([0-9\.,\s]+)\]", content)
    assert theo_match is not None, "Could not parse Theoretical distribution from results.txt."
    theo_vals = [float(x.strip()) for x in theo_match.group(1).split(",")]
    assert len(theo_vals) == 4, f"Theoretical distribution should have 4 values, found {len(theo_vals)}."

    expected_theo = [0.2308, 0.2692, 0.2692, 0.2308]
    for v, exp in zip(theo_vals, expected_theo):
        assert abs(v - exp) < 0.01, f"Theoretical distribution value {v} does not match expected {exp}."

    # Parse Empirical
    emp_match = re.search(r"Empirical:\s*\[([0-9\.,\s]+)\]", content)
    assert emp_match is not None, "Could not parse Empirical distribution from results.txt."
    emp_vals = [float(x.strip()) for x in emp_match.group(1).split(",")]
    assert len(emp_vals) == 4, f"Empirical distribution should have 4 values, found {len(emp_vals)}."

    for v, exp in zip(emp_vals, expected_theo):
        assert abs(v - exp) < 0.01, f"Empirical distribution value {v} does not match expected {exp}."

def test_simulator_compiled():
    executable = "/home/user/simulator"
    assert os.path.isfile(executable), f"Compiled executable {executable} does not exist. Did you compile the code?"
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."