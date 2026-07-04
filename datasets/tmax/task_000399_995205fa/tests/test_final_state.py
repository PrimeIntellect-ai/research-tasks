# test_final_state.py

import os
import math
import pytest

def test_executable_exists():
    """Test that the compiled executable exists."""
    executable = "/home/user/seq_analyzer"
    assert os.path.isfile(executable), f"Executable {executable} is missing. Did you compile the C program?"
    assert os.access(executable, os.X_OK), f"File {executable} is not executable."

def test_output_file_exists():
    """Test that the analysis output file exists."""
    output_txt = "/home/user/analysis_output.txt"
    assert os.path.isfile(output_txt), f"Output file {output_txt} is missing. Did you redirect the output?"

def test_output_values():
    """Test that the output values match the expected mathematical results."""
    fasta_file = "/home/user/dataset.fasta"
    assert os.path.isfile(fasta_file), f"Dataset file {fasta_file} is missing."

    # Parse the FASTA file to compute expected values
    gc_contents = []
    with open(fasta_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(">"):
                continue
            gc_count = sum(1 for c in line if c in ('G', 'C'))
            gc_contents.append(gc_count / len(line))

    n = len(gc_contents)
    assert n > 0, "No sequences found in dataset."

    expected_mu = sum(gc_contents) / n
    expected_var = sum((x - expected_mu) ** 2 for x in gc_contents) / n
    if expected_var < 1e-9:
        expected_var = 1e-9

    expected_z = (expected_mu - 0.5) / math.sqrt(expected_var / n)

    output_txt = "/home/user/analysis_output.txt"
    with open(output_txt, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 3, f"Expected exactly 3 lines of output, found {len(lines)}."

    assert lines[0].startswith("Fitted Mean:"), "First line must start with 'Fitted Mean:'"
    assert lines[1].startswith("Fitted Variance:"), "Second line must start with 'Fitted Variance:'"
    assert lines[2].startswith("Z-score:"), "Third line must start with 'Z-score:'"

    try:
        actual_mu = float(lines[0].split(":")[1].strip())
        actual_var = float(lines[1].split(":")[1].strip())
        actual_z = float(lines[2].split(":")[1].strip())
    except ValueError:
        pytest.fail("Could not parse numeric values from the output file.")

    assert math.isclose(actual_mu, expected_mu, abs_tol=1e-3), f"Expected Fitted Mean ~{expected_mu:.4f}, got {actual_mu}"
    assert math.isclose(actual_var, expected_var, abs_tol=1e-3), f"Expected Fitted Variance ~{expected_var:.4f}, got {actual_var}"
    assert math.isclose(actual_z, expected_z, abs_tol=1e-3) or (expected_z == 0.0 and actual_z == 0.0), f"Expected Z-score ~{expected_z:.4f}, got {actual_z}"

def test_c_code_fixed():
    """Test that the C code was modified to fix the step size adaptation."""
    c_file = "/home/user/seq_analyzer.c"
    assert os.path.isfile(c_file), f"Missing C source file: {c_file}"

    with open(c_file, "r") as f:
        content = f.read()

    # Check that alpha / n or something equivalent is used
    # We can't be too strict on exact syntax, but we know the original was "mu = mu + alpha * grad;"
    assert "mu = mu + alpha * grad;" not in content, "The C file still contains the buggy update rule without dividing by n."