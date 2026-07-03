# test_final_state.py

import os
import subprocess

def test_recovered_logs_exists():
    """Test that the recovered_logs.txt file exists."""
    log_path = '/home/user/app/recovered_logs.txt'
    assert os.path.isfile(log_path), f"File {log_path} is missing. Did you extract the logs?"

    with open(log_path, 'r') as f:
        content = f.read()

    assert "UPTIME_PING=" in content, f"{log_path} does not contain the expected 'UPTIME_PING=' string."

def test_final_metric_correct():
    """Test that final_metric.txt contains the correct total uptime."""
    metric_path = '/home/user/final_metric.txt'
    assert os.path.isfile(metric_path), f"File {metric_path} is missing. Did you pipe the output?"

    with open(metric_path, 'r') as f:
        content = f.read().strip()

    assert content == "Total Uptime: 50000", f"Expected 'Total Uptime: 50000' in {metric_path}, but got '{content}'."

def test_aggregator_is_deterministic():
    """Test that aggregator.py has been fixed and consistently outputs the correct value."""
    script_path = '/home/user/app/aggregator.py'
    log_path = '/home/user/app/recovered_logs.txt'

    assert os.path.isfile(script_path), f"{script_path} is missing."
    assert os.path.isfile(log_path), f"{log_path} is missing."

    # Run the script a few times to ensure the race condition is fixed
    for i in range(5):
        result = subprocess.run(
            ['python3', script_path, log_path],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"aggregator.py failed to run on iteration {i+1}."
        output = result.stdout.strip()
        assert output == "Total Uptime: 50000", f"aggregator.py is not deterministic or incorrect. Expected 'Total Uptime: 50000', got '{output}' on iteration {i+1}."