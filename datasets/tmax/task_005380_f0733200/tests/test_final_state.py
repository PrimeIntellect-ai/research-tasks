# test_final_state.py

import os
import pytest

def test_compute_shift_cpp_exists():
    """Verify that the C++ source file exists."""
    cpp_file = "/home/user/compute_shift.cpp"
    assert os.path.isfile(cpp_file), f"Expected C++ file {cpp_file} does not exist."

def test_run_pipeline_sh_exists_and_executable():
    """Verify that the bash script exists and is executable."""
    sh_file = "/home/user/run_pipeline.sh"
    assert os.path.isfile(sh_file), f"Expected bash script {sh_file} does not exist."
    assert os.access(sh_file, os.X_OK), f"Bash script {sh_file} is not executable."

def test_shift_report_exists_and_correct():
    """Verify that the shift report exists and contains the correct KS statistic and decision."""
    report_file = "/home/user/shift_report.txt"
    assert os.path.isfile(report_file), f"Expected report file {report_file} does not exist."

    with open(report_file, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 2, f"Expected exactly 2 lines in {report_file}, found {len(lines)}."

    ks_stat_str = lines[0]
    decision = lines[1]

    # Check KS stat
    try:
        ks_stat = float(ks_stat_str)
    except ValueError:
        pytest.fail(f"First line of {report_file} is not a valid float: {ks_stat_str}")

    assert ks_stat_str in ["0.0592", "0.0593"], f"Expected KS distance to be 0.0592 or 0.0593, got {ks_stat_str}"

    # Check decision
    assert decision == "REJECT", f"Expected decision to be REJECT, got {decision}"