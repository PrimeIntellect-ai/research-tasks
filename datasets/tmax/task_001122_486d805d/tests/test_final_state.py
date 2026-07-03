# test_final_state.py

import os
import re
import pytest

def test_analysis_result_exists():
    """Test that the analysis_result.txt file exists."""
    file_path = "/home/user/analysis_result.txt"
    assert os.path.exists(file_path), f"The result file {file_path} is missing."
    assert os.path.isfile(file_path), f"The path {file_path} is not a file."

def test_analysis_result_contents():
    """Test the contents of the analysis_result.txt file."""
    file_path = "/home/user/analysis_result.txt"
    if not os.path.exists(file_path):
        pytest.fail(f"File {file_path} not found.")

    with open(file_path, "r") as f:
        content = f.read()

    # Time Energy
    time_energy_match = re.search(r"Time Energy:\s*([0-9.]+)", content)
    assert time_energy_match is not None, "Could not find 'Time Energy: <value>' in the result file."
    time_energy = float(time_energy_match.group(1))
    assert abs(time_energy - 10240.00) < 0.1, f"Expected Time Energy ~10240.00, got {time_energy}"

    # Freq Energy
    freq_energy_match = re.search(r"Freq Energy:\s*([0-9.]+)", content)
    assert freq_energy_match is not None, "Could not find 'Freq Energy: <value>' in the result file."
    freq_energy = float(freq_energy_match.group(1))
    assert abs(freq_energy - 10240.00) < 0.1, f"Expected Freq Energy ~10240.00, got {freq_energy}"

    # Stability Error
    error_match = re.search(r"Stability Error:\s*([0-9.]+)", content)
    assert error_match is not None, "Could not find 'Stability Error: <value>' in the result file."
    stability_error = float(error_match.group(1))
    assert stability_error < 1e-3, f"Expected Stability Error close to 0, got {stability_error}"

    # Dominant Frequency Bin
    bin_match = re.search(r"Dominant Frequency Bin:\s*([0-9]+)", content)
    assert bin_match is not None, "Could not find 'Dominant Frequency Bin: <integer>' in the result file."
    dominant_bin = int(bin_match.group(1))
    assert dominant_bin == 1365, f"Expected Dominant Frequency Bin to be 1365, got {dominant_bin}"

def test_c_source_code_exists():
    """Test that the C source code was created."""
    file_path = "/home/user/analyze_seq.c"
    assert os.path.exists(file_path), f"The C source file {file_path} is missing."