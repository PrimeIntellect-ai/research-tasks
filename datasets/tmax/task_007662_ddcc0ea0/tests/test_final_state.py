# test_final_state.py
import os
import math
import pytest

def test_run_pipeline_exists_and_executable():
    """Test that the extracted script exists and is executable."""
    path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(path), f"Missing extracted script at {path}"
    assert os.access(path, os.X_OK), f"The script {path} is not executable"

def test_analyze_spectra_exists_and_executable():
    """Test that the analyze_spectra.sh script exists and is executable."""
    path = "/home/user/analyze_spectra.sh"
    assert os.path.isfile(path), f"Missing script at {path}"
    assert os.access(path, os.X_OK), f"The script {path} is not executable"

def test_spectral_output():
    """Test that the spectral output matches the expected computed DFT power."""
    fasta_path = "/home/user/protein.fasta"
    assert os.path.isfile(fasta_path), f"Missing FASTA file at {fasta_path}"

    with open(fasta_path, "r") as f:
        lines = f.readlines()

    # Extract sequence ignoring headers
    seq = "".join(line.strip() for line in lines if not line.startswith(">"))

    hydrophobic = set("AILMFWV")
    polar_charged = set("RNDEQKST")

    x = []
    for char in seq:
        if char in hydrophobic:
            x.append(1.0)
        elif char in polar_charged:
            x.append(-1.0)
        else:
            x.append(0.0)

    f_val = 0.2777
    pi_val = 3.14159265359

    X = 0.0
    Y = 0.0
    for n, val in enumerate(x):
        X += val * math.cos(2 * pi_val * f_val * n)
        Y += val * math.sin(2 * pi_val * f_val * n)

    expected_P = X**2 + Y**2

    output_path = "/home/user/spectral_output.txt"
    assert os.path.isfile(output_path), f"Missing output file at {output_path}"

    with open(output_path, "r") as f:
        content = f.read().strip()

    try:
        actual_P = float(content)
    except ValueError:
        pytest.fail(f"Output file {output_path} does not contain a valid float. Found: '{content}'")

    # Allow a small tolerance for floating point rounding differences across awk versions
    assert math.isclose(actual_P, expected_P, abs_tol=0.02), (
        f"Computed power {actual_P} in {output_path} does not match expected {expected_P:.2f}"
    )