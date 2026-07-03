# test_final_state.py

import os
import subprocess
import re

def test_analysis_log_exists():
    assert os.path.isfile("/home/user/results/analysis.log"), "The file /home/user/results/analysis.log does not exist."

def test_analysis_log_contents():
    log_path = "/home/user/results/analysis.log"
    assert os.path.isfile(log_path), "The file /home/user/results/analysis.log does not exist."

    with open(log_path, 'r') as f:
        content = f.read().strip()

    # We expect two sequences: read_A and read_B
    # Format:
    # Sequence: read_A
    # Dominant Period: 6
    # GC Posterior Mean: 0.67
    # ---
    # Sequence: read_B
    # Dominant Period: 2
    # GC Posterior Mean: 0.03

    blocks = content.split("---")
    assert len(blocks) >= 2, "The analysis.log file should contain at least two sequence blocks separated by '---'."

    # Parse read_A
    read_a_block = blocks[0].strip()
    assert "Sequence: read_A" in read_a_block, "Sequence read_A not found in the first block."

    period_match_a = re.search(r"Dominant Period:\s*(\d+)", read_a_block)
    assert period_match_a, "Dominant Period not found for read_A."
    assert int(period_match_a.group(1)) == 6, f"Expected Dominant Period 6 for read_A, got {period_match_a.group(1)}."

    gc_match_a = re.search(r"GC Posterior Mean:\s*([\d\.]+)", read_a_block)
    assert gc_match_a, "GC Posterior Mean not found for read_A."
    gc_val_a = float(gc_match_a.group(1))
    assert abs(gc_val_a - 0.67) <= 0.02, f"Expected GC Posterior Mean ~0.67 for read_A, got {gc_val_a}."

    # Parse read_B
    read_b_block = blocks[1].strip()
    assert "Sequence: read_B" in read_b_block, "Sequence read_B not found in the second block."

    period_match_b = re.search(r"Dominant Period:\s*(\d+)", read_b_block)
    assert period_match_b, "Dominant Period not found for read_B."
    assert int(period_match_b.group(1)) == 2, f"Expected Dominant Period 2 for read_B, got {period_match_b.group(1)}."

    gc_match_b = re.search(r"GC Posterior Mean:\s*([\d\.]+)", read_b_block)
    assert gc_match_b, "GC Posterior Mean not found for read_B."
    gc_val_b = float(gc_match_b.group(1))
    assert abs(gc_val_b - 0.03) <= 0.02, f"Expected GC Posterior Mean ~0.03 for read_B, got {gc_val_b}."

def test_regression_tests_pass():
    script_path = "/home/user/seq_analyzer/run_tests.sh"
    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.access(script_path, os.X_OK), f"{script_path} is not executable."

    result = subprocess.run(
        [script_path],
        cwd="/home/user/seq_analyzer",
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Regression tests failed. Output: {result.stdout}\n{result.stderr}"
    assert "Tests passed!" in result.stdout, "Expected 'Tests passed!' in output of run_tests.sh."