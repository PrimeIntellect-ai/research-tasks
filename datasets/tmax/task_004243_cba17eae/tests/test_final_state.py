# test_final_state.py

import os
import sys
import math
import subprocess
import pytest

def test_venv_exists_and_packages_installed():
    """Check if the virtual environment exists and contains the required packages."""
    venv_python = "/home/user/venv/bin/python"
    assert os.path.isfile(venv_python), "Virtual environment Python executable not found at /home/user/venv/bin/python"

    # Check for installed packages
    try:
        output = subprocess.check_output(
            [venv_python, "-c", "import numpy, scipy, matplotlib; print('OK')"],
            stderr=subprocess.STDOUT,
            text=True
        )
        assert "OK" in output, "Required packages (numpy, scipy, matplotlib) are not properly installed in the venv."
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Failed to import required packages in the venv. Error: {e.output}")

def test_wave_sim_fixed():
    """Check if wave_sim.py was modified to fix the reproducibility bug."""
    wave_sim_path = "/home/user/sim/wave_sim.py"
    assert os.path.isfile(wave_sim_path), f"File {wave_sim_path} does not exist."

    with open(wave_sim_path, 'r') as f:
        content = f.read()

    # The bug was `random.shuffle(items)`. It should either be removed or items should be sorted.
    # We will check if the file was modified to remove the shuffle or add sorting.
    # A simple check is that if random.shuffle is still there, it must be followed by a sort.
    if "random.shuffle(items)" in content:
        assert "sort" in content or "sorted" in content, "random.shuffle is still in wave_sim.py and no sorting was added."

def test_energy_npy_exists():
    """Check if energy.npy was generated."""
    energy_path = "/home/user/sim/energy.npy"
    assert os.path.isfile(energy_path), f"File {energy_path} was not generated."

def test_analyze_script_exists():
    """Check if analyze.py exists."""
    analyze_path = "/home/user/sim/analyze.py"
    assert os.path.isfile(analyze_path), f"File {analyze_path} was not created."

def test_peak_txt_correct():
    """Check if peak.txt contains the correct dominant frequency."""
    peak_path = "/home/user/sim/peak.txt"
    assert os.path.isfile(peak_path), f"File {peak_path} was not created."

    with open(peak_path, 'r') as f:
        content = f.read().strip()

    try:
        peak_freq = float(content)
    except ValueError:
        pytest.fail(f"Content of {peak_path} is not a valid float: '{content}'")

    # The expected peak is around 7.2 (due to binning) or 7.0 (if interpolated)
    assert math.isclose(peak_freq, 7.2, abs_tol=0.3) or math.isclose(peak_freq, 7.0, abs_tol=0.3), \
        f"Peak frequency {peak_freq} is not close to the expected 7.0 or 7.2 Hz."

def test_spectrum_png_exists():
    """Check if spectrum.png was generated."""
    spectrum_path = "/home/user/sim/spectrum.png"
    assert os.path.isfile(spectrum_path), f"File {spectrum_path} was not generated."
    assert os.path.getsize(spectrum_path) > 0, f"File {spectrum_path} is empty."