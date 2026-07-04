# test_final_state.py

import os
import re

def test_profiler_script_exists_and_executable():
    """Verify that /home/user/profiler.sh exists and is executable."""
    script_path = '/home/user/profiler.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_profiler_script_no_python_for_bootstrap():
    """Verify that the script does not use python or perl for the bootstrap logic."""
    script_path = '/home/user/profiler.sh'
    with open(script_path, 'r') as f:
        content = f.read()

    # It's allowed to call python for the simulation part, but let's just make sure
    # it doesn't have inline python scripts or perl scripts for bootstrap.
    # We will check if perl is used at all.
    assert 'perl' not in content.lower(), "Perl should not be used in the script."

def test_profile_results_exist():
    """Verify that /home/user/profile_results.txt exists."""
    results_path = '/home/user/profile_results.txt'
    assert os.path.isfile(results_path), f"Results file {results_path} does not exist."

def test_profile_results_format_and_values():
    """Verify the format and values in /home/user/profile_results.txt."""
    results_path = '/home/user/profile_results.txt'
    with open(results_path, 'r') as f:
        content = f.read().strip()

    # Expected format: N=50, B=5000, CI=[<lower>, <upper>]
    pattern = r'^N=50,\s*B=5000,\s*CI=\[\s*([\d\.]+)\s*,\s*([\d\.]+)\s*\]$'
    match = re.match(pattern, content)
    assert match, f"Content '{content}' does not match the expected format 'N=50, B=5000, CI=[<lower>, <upper>]'."

    lower_bound = float(match.group(1))
    upper_bound = float(match.group(2))

    assert 154.0 <= lower_bound <= 158.0, f"Lower bound {lower_bound} is outside the expected range [154.0, 158.0]."
    assert 174.0 <= upper_bound <= 178.5, f"Upper bound {upper_bound} is outside the expected range [174.0, 178.5]."