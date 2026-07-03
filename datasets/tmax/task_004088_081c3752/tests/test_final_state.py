# test_final_state.py
import os
import re

def test_files_exist():
    """Check if all required files were created."""
    assert os.path.exists('/home/user/mc_ruin.cpp'), "/home/user/mc_ruin.cpp does not exist."
    assert os.path.exists('/home/user/run_convergence.sh'), "/home/user/run_convergence.sh does not exist."
    assert os.path.exists('/home/user/convergence_report.md'), "/home/user/convergence_report.md does not exist."

def test_executable_exists():
    """Check if the C++ program was compiled into the expected executable."""
    assert os.path.exists('/home/user/mc_ruin'), "/home/user/mc_ruin executable does not exist."
    assert os.access('/home/user/mc_ruin', os.X_OK), "/home/user/mc_ruin is not executable."

def test_convergence_report_contents():
    """Check the contents of the convergence report for correct N and probabilities."""
    report_path = '/home/user/convergence_report.md'
    assert os.path.exists(report_path), f"{report_path} does not exist."

    with open(report_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines in {report_path}, found {len(lines)}."

    expected_results = {
        1000: 0.551,
        10000: 0.5364,
        100000: 0.53587
    }

    parsed_results = {}
    pattern = re.compile(r'^N=(\d+),\s*P=([0-9.]+)$')

    for line in lines:
        match = pattern.match(line)
        assert match, f"Line '{line}' does not match the expected format 'N=<N>, P=<probability>'."
        n_val = int(match.group(1))
        p_val = float(match.group(2))
        parsed_results[n_val] = p_val

    for expected_n, expected_p in expected_results.items():
        assert expected_n in parsed_results, f"Missing result for N={expected_n} in the report."
        actual_p = parsed_results[expected_n]
        assert abs(actual_p - expected_p) < 1e-5, f"For N={expected_n}, expected P approx {expected_p}, got {actual_p}."