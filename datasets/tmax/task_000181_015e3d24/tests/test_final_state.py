# test_final_state.py

import os
import subprocess

def test_script_exists_and_executable():
    """Verify that the analyze_deps.sh script exists and is executable."""
    script_path = '/home/user/analyze_deps.sh'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

def test_critical_path_output():
    """Verify that the critical_path.txt file contains the correct shortest path."""
    output_path = '/home/user/critical_path.txt'
    assert os.path.isfile(output_path), f"Output file {output_path} does not exist."

    with open(output_path, 'r') as f:
        content = f.read().strip()

    expected = "extract_users->fast_track_load->aggregate_metrics->report_generation"
    assert content == expected, f"Content of {output_path} is incorrect. Expected '{expected}', got '{content}'."

def test_script_functionality():
    """Verify that the script correctly computes the shortest path for a different set of inputs."""
    script_path = '/home/user/analyze_deps.sh'

    if not (os.path.isfile(script_path) and os.access(script_path, os.X_OK)):
        return # Skip if script doesn't exist or isn't executable (handled by previous test)

    result = subprocess.run(
        [script_path, 'extract_users', 'aggregate_metrics'], 
        capture_output=True, 
        text=True
    )

    assert result.returncode == 0, f"Script failed to execute successfully. Stderr: {result.stderr}"

    output = result.stdout.strip()
    expected = "extract_users->fast_track_load->aggregate_metrics"
    assert output == expected, f"Script output incorrect for 'extract_users' to 'aggregate_metrics'. Expected '{expected}', got '{output}'."