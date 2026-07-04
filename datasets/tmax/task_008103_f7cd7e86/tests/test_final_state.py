# test_final_state.py
import os
import re
import subprocess

def test_mcmc_integration_fixed():
    script_path = "/home/user/mcmc_project/mcmc_integration.py"
    assert os.path.exists(script_path), f"File {script_path} is missing."

    # Run the script to ensure it does not crash with LinAlgError
    result = subprocess.run(
        ["python3", script_path],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"mcmc_integration.py failed to run. Stderr: {result.stderr}"

    # Check if the output is a valid float
    try:
        float(result.stdout.strip())
    except ValueError:
        assert False, f"mcmc_integration.py did not output a valid float. Output: {result.stdout}"

def test_profile_runs_script():
    script_path = "/home/user/mcmc_project/profile_runs.sh"
    assert os.path.exists(script_path), f"File {script_path} is missing."
    assert os.access(script_path, os.X_OK), f"File {script_path} is not executable."

def test_integral_samples():
    samples_path = "/home/user/mcmc_project/integral_samples.txt"
    assert os.path.exists(samples_path), f"File {samples_path} is missing."

    with open(samples_path, "r") as f:
        lines = f.read().strip().split('\n')

    assert len(lines) == 30, f"Expected 30 lines in {samples_path}, found {len(lines)}."

    for i, line in enumerate(lines):
        try:
            float(line.strip())
        except ValueError:
            assert False, f"Line {i+1} in {samples_path} is not a valid float: '{line}'"

def test_ci_output():
    ci_path = "/home/user/mcmc_project/ci_output.txt"
    assert os.path.exists(ci_path), f"File {ci_path} is missing."

    with open(ci_path, "r") as f:
        content = f.read().strip()

    # Regex to match: 95% CI: [lower_bound, upper_bound] rounded to 4 decimal places
    pattern = r"^95% CI: \[-?\d+\.\d{4}, -?\d+\.\d{4}\]$"
    assert re.match(pattern, content), f"ci_output.txt content '{content}' does not match expected format '95% CI: [lower_bound, upper_bound]' with 4 decimal places."