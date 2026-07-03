# test_final_state.py

import os
import re
import pytest

def test_convergence_log_exists_and_content():
    """Test that convergence.log exists and contains the expected output."""
    log_file = "/home/user/convergence.log"
    assert os.path.isfile(log_file), f"Expected log file {log_file} does not exist."

    with open(log_file, "r") as f:
        content = f.read()

    expected_lines = [
        "N=1024, PeakFreq=15.430 Hz",
        "N=2048, PeakFreq=15.430 Hz",
        "N=4096, PeakFreq=15.381 Hz",
        "N=8192, PeakFreq=15.405 Hz"
    ]

    for expected in expected_lines:
        assert expected in content, (
            f"Expected line '{expected}' not found in {log_file}. "
            f"Actual content:\n{content}"
        )

def test_spectrum_svg_exists_and_format():
    """Test that spectrum.svg exists and is a valid SVG file."""
    svg_file = "/home/user/spectrum.svg"
    assert os.path.isfile(svg_file), f"Expected plot file {svg_file} does not exist."

    with open(svg_file, "r") as f:
        # Read the first few kilobytes to check for the SVG tag
        header = f.read(2048).lower()

    assert "<svg" in header, f"The file {svg_file} does not appear to be a valid SVG file."

def test_spectral_directory_exists():
    """Test that the spectral directory was created."""
    spectral_dir = "/home/user/spectral"
    assert os.path.isdir(spectral_dir), f"Expected directory {spectral_dir} does not exist."