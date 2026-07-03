# test_final_state.py

import os
import subprocess

def test_mc_sim_executable_exists():
    """Check if /home/user/mc_sim exists and is executable."""
    exe_path = '/home/user/mc_sim'
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_times_txt_validity():
    """Check if /home/user/times.txt exists, has 50 lines, and contains floats."""
    times_path = '/home/user/times.txt'
    assert os.path.isfile(times_path), f"File {times_path} does not exist."

    with open(times_path, 'r') as f:
        lines = [line.strip() for line in f if line.strip()]

    assert len(lines) == 50, f"Expected exactly 50 lines in {times_path}, found {len(lines)}."

    for i, line in enumerate(lines):
        try:
            float(line)
        except ValueError:
            assert False, f"Line {i+1} in {times_path} is not a valid float: '{line}'"

def test_bootstrap_ci_exists():
    """Check if /home/user/bootstrap_ci.txt exists."""
    ci_path = '/home/user/bootstrap_ci.txt'
    assert os.path.isfile(ci_path), f"File {ci_path} does not exist."

def test_bootstrap_ci_correctness():
    """Verify the contents of bootstrap_ci.txt match the expected numpy computation."""
    times_path = '/home/user/times.txt'
    ci_path = '/home/user/bootstrap_ci.txt'

    # Ensure times.txt exists to avoid subprocess error masking
    assert os.path.isfile(times_path), f"Cannot verify CI because {times_path} is missing."
    assert os.path.isfile(ci_path), f"Cannot verify CI because {ci_path} is missing."

    with open(ci_path, 'r') as f:
        agent_output = f.read().strip()

    # We use a subprocess to run the exact numpy script to avoid third-party imports in the test file
    numpy_script = f"""
import numpy as np
with open('{times_path}', 'r') as f:
    times = np.array([float(line.strip()) for line in f if line.strip()])
np.random.seed(42)
B = 10000
means = []
for _ in range(B):
    sample = np.random.choice(times, size=len(times), replace=True)
    means.append(np.mean(sample))
lower, upper = np.percentile(means, [2.5, 97.5])
print(f"{{lower:.6f}},{{upper:.6f}}")
"""

    try:
        result = subprocess.run(
            ['python3', '-c', numpy_script],
            check=True,
            capture_output=True,
            text=True
        )
        expected_output = result.stdout.strip()
    except subprocess.CalledProcessError as e:
        assert False, f"Failed to compute expected CI using numpy: {e.stderr}"

    assert agent_output == expected_output, \
        f"Bootstrap CI mismatch. Expected '{expected_output}', but got '{agent_output}'."