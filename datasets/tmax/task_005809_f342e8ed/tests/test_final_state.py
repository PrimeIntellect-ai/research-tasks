# test_final_state.py

import os
import re

def test_stat_log_exists_and_correct():
    stat_log_path = '/home/user/results/stat_log.txt'
    assert os.path.isfile(stat_log_path), f"File {stat_log_path} is missing. Did you create the results directory and save the variance?"

    with open(stat_log_path, 'r') as f:
        content = f.read().strip()

    assert "Variance: 0.0000" in content, f"Expected 'Variance: 0.0000' in {stat_log_path}, but found: {content}"

def test_fit_log_exists_and_correct():
    fit_log_path = '/home/user/results/fit_log.txt'
    assert os.path.isfile(fit_log_path), f"File {fit_log_path} is missing. Did you save the curve fitting output?"

    with open(fit_log_path, 'r') as f:
        content = f.read().strip()

    # The expected coefficients for x=[1,2,3,4,5] and y=[2.1, 5.9, 11.8, 20.2, 30.5]
    # c0 = 0.3800, c1 = 0.5229, c2 = 0.9857
    expected_str = "Coeffs: 0.3800, 0.5229, 0.9857"
    assert expected_str in content, f"Expected '{expected_str}' in {fit_log_path}, but found: {content}"

def test_cpp_code_fixed():
    cpp_path = '/home/user/src/energy_sim.cpp'
    assert os.path.isfile(cpp_path), f"File {cpp_path} is missing."

    with open(cpp_path, 'r') as f:
        content = f.read()

    # Check that atomic is removed
    assert "#pragma omp atomic" not in content, "The code still contains '#pragma omp atomic', which causes non-deterministic reduction."

    # Check for reduction clause
    assert re.search(r'#pragma\s+omp\s+parallel\s+for\s+reduction\s*\(\s*\+\s*:\s*total_energy\s*\)', content) or \
           re.search(r'reduction\s*\(\s*\+\s*:\s*total_energy\s*\)', content), \
           "The code does not seem to contain a proper OpenMP reduction clause for 'total_energy'."

    # Check that total_energy is a double
    assert re.search(r'double\s+total_energy\s*=\s*0\.0', content), "The 'total_energy' accumulator should be changed to a 'double'."