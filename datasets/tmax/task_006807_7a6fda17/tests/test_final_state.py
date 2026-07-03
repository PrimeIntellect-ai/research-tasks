# test_final_state.py

import os
import pstats
import pytest

def test_opt_result_file():
    """Verify opt_result.txt contains the correct optimized coordinates."""
    filepath = "/home/user/opt_result.txt"
    assert os.path.exists(filepath), f"File {filepath} is missing."
    with open(filepath, "r") as f:
        content = f.read().strip()

    parts = content.split()
    assert len(parts) == 2, f"Expected 2 values in {filepath}, found {len(parts)}."

    try:
        x, y = map(float, parts)
    except ValueError:
        pytest.fail(f"Could not parse floats from {filepath}. Content: {content}")

    # BFGS on Rosenbrock from (0,0) hits (1,1)
    assert abs(x - 1.0) < 1e-2, f"Optimized x coordinate {x} is not close to 1.0"
    assert abs(y - 1.0) < 1e-2, f"Optimized y coordinate {y} is not close to 1.0"

def test_mcmc_mean_file():
    """Verify mcmc_mean.txt exists and contains valid floats."""
    filepath = "/home/user/mcmc_mean.txt"
    assert os.path.exists(filepath), f"File {filepath} is missing."
    with open(filepath, "r") as f:
        content = f.read().strip()

    parts = content.split()
    assert len(parts) == 2, f"Expected 2 values in {filepath}, found {len(parts)}."

    try:
        x, y = map(float, parts)
    except ValueError:
        pytest.fail(f"Could not parse floats from {filepath}. Content: {content}")

def test_mcmc_profile_file():
    """Verify mcmc_profile.prof exists and is a valid pstats file."""
    filepath = "/home/user/mcmc_profile.prof"
    assert os.path.exists(filepath), f"File {filepath} is missing."
    try:
        stats = pstats.Stats(filepath)
        assert stats.total_calls > 0, "Profile data seems empty."
    except Exception as e:
        pytest.fail(f"Could not load profile data from {filepath}: {e}")

def test_profile_stats_file():
    """Verify profile_stats.txt exists and contains expected pstats output."""
    filepath = "/home/user/profile_stats.txt"
    assert os.path.exists(filepath), f"File {filepath} is missing."
    with open(filepath, "r") as f:
        content = f.read()

    assert "function calls" in content, f"'function calls' not found in {filepath}"
    assert "tottime" in content, f"'tottime' not found in {filepath}"

def test_makefile_exists():
    """Verify Makefile exists."""
    filepath = "/home/user/Makefile"
    assert os.path.exists(filepath), f"File {filepath} is missing."

def test_sampler_script_exists():
    """Verify sampler.py exists."""
    filepath = "/home/user/sampler.py"
    assert os.path.exists(filepath), f"File {filepath} is missing."