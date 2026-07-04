# test_final_state.py
import os
import re
import pytest

def test_script_exists():
    script_path = "/home/user/bootstrap_ci.sh"
    assert os.path.exists(script_path), f"Script {script_path} is missing."
    assert os.path.isfile(script_path), f"{script_path} is not a file."

    # Check if it's a bash/shell script and not python/R/perl
    with open(script_path, 'r') as f:
        content = f.read().lower()
        assert "python" not in content[:100], "Script appears to be a Python script, but must be Bash/CLI."
        assert "perl" not in content[:100], "Script appears to be a Perl script, but must be Bash/CLI."
        assert " rscript" not in content[:100], "Script appears to be an R script, but must be Bash/CLI."

def test_ci_output_format_and_values():
    output_path = "/home/user/ci_output.txt"
    assert os.path.exists(output_path), f"Output file {output_path} is missing."

    with open(output_path, 'r') as f:
        content = f.read().strip()

    match = re.match(r"^Lower:\s*([0-9.]+),\s*Upper:\s*([0-9.]+)$", content)
    assert match is not None, f"Format of {output_path} is incorrect. Expected 'Lower: X.XXX, Upper: Y.YYY', got '{content}'"

    lower_val = float(match.group(1))
    upper_val = float(match.group(2))

    assert 0.930 <= lower_val <= 1.010, f"Lower bound {lower_val} is out of expected statistical range [0.930, 1.010]."
    assert 1.060 <= upper_val <= 1.140, f"Upper bound {upper_val} is out of expected statistical range [1.060, 1.140]."

def test_convergence_output():
    output_path = "/home/user/convergence.txt"
    assert os.path.exists(output_path), f"Output file {output_path} is missing."

    with open(output_path, 'r') as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 10, f"Expected 10 lines in {output_path}, got {len(lines)}."

    for i, line in enumerate(lines):
        expected_iter = (i + 1) * 100
        match = re.match(rf"^Iteration {expected_iter}:\s*([0-9.]+)$", line)
        assert match is not None, f"Line {i+1} format is incorrect. Expected 'Iteration {expected_iter}: <value>', got '{line}'"

        val = float(match.group(1))
        assert 0.900 <= val <= 1.200, f"Cumulative average {val} at iteration {expected_iter} is out of expected range."