# test_final_state.py

import os
import pytest
import numpy as np
from scipy.stats import wasserstein_distance
from scipy.signal import savgol_filter

def test_bug_fixed():
    """Test that the deliberate bug in core.py has been fixed."""
    core_py_path = "/app/spec_smooth/spec_smooth/core.py"
    assert os.path.isfile(core_py_path), f"{core_py_path} is missing."

    with open(core_py_path, "r") as f:
        content = f.read()

    assert "import nump as np" not in content, "The deliberate bug 'import nump as np' is still present in core.py."
    assert "import numpy as np" in content, "The import statement was not correctly fixed to 'import numpy as np'."

def test_output_file_exists():
    """Test that the output file was created."""
    output_path = "/home/user/mean_distance.txt"
    assert os.path.isfile(output_path), f"The output file {output_path} was not created."

def test_metric_threshold():
    """Test that the computed mean Wasserstein distance meets the threshold."""
    output_path = "/home/user/mean_distance.txt"
    assert os.path.isfile(output_path), f"Cannot find {output_path} to check metric."

    with open(output_path, "r") as f:
        content = f.read().strip()

    try:
        val = float(content)
    except ValueError:
        pytest.fail(f"Content of {output_path} is not a valid float: {content}")

    threshold = 0.005
    assert val <= threshold, f"Mean Wasserstein distance {val} is greater than threshold {threshold}."

def test_actual_computation_correctness():
    """Test that the value in the output file matches the actual expected computation."""
    theoretical_path = "/app/data/theoretical_spectra.npy"
    noisy_path = "/app/data/noisy_spectra.npy"

    assert os.path.isfile(theoretical_path), f"{theoretical_path} is missing."
    assert os.path.isfile(noisy_path), f"{noisy_path} is missing."

    theoretical = np.load(theoretical_path)
    noisy = np.load(noisy_path)

    N = noisy.shape[0]
    distances = []

    for i in range(N):
        smoothed = savgol_filter(noisy[i], window_length=15, polyorder=3)

        # Normalize
        smoothed_norm = smoothed / np.sum(smoothed)
        theoretical_norm = theoretical[i] / np.sum(theoretical[i])

        # Calculate distance
        dist = wasserstein_distance(smoothed_norm, theoretical_norm)
        distances.append(dist)

    expected_mean_distance = np.mean(distances)

    output_path = "/home/user/mean_distance.txt"
    with open(output_path, "r") as f:
        val = float(f.read().strip())

    # Allow a small tolerance for floating point differences
    assert np.isclose(val, expected_mean_distance, rtol=1e-3, atol=1e-5), \
        f"Submitted distance {val} does not match the expected computed distance {expected_mean_distance}."