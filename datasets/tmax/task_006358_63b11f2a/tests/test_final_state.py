# test_final_state.py
import os
import re

def test_go_script_exists():
    assert os.path.exists('/home/user/rolling_stats.go'), "/home/user/rolling_stats.go does not exist"

def test_stats_log_content():
    stats_log_path = '/home/user/stats.log'
    assert os.path.exists(stats_log_path), f"{stats_log_path} does not exist"

    with open(stats_log_path, 'r') as f:
        content = f.read().strip()

    expected = "45.00,78.00,111.00,144.00,177.00"
    assert content == expected, f"Expected {stats_log_path} to contain '{expected}', but got '{content}'"

def test_pipeline_log_content():
    pipeline_log_path = '/home/user/pipeline.log'
    assert os.path.exists(pipeline_log_path), f"{pipeline_log_path} does not exist"

    with open(pipeline_log_path, 'r') as f:
        content = f.read().strip()

    # It should end with the exact success message, or contain it.
    expected_msg = "SUCCESS: Processed 7 records"
    assert expected_msg in content, f"Expected {pipeline_log_path} to contain '{expected_msg}'"

def test_cron_file_content():
    cron_path = '/home/user/stats_cron'
    assert os.path.exists(cron_path), f"{cron_path} does not exist"

    with open(cron_path, 'r') as f:
        content = f.read().strip()

    # Check for */5 * * * *
    cron_regex = re.compile(r'^\*/5\s+\*\s+\*\s+\*\s+\*')
    assert cron_regex.search(content), f"{cron_path} does not contain a valid cron schedule for every 5 minutes (e.g. '*/5 * * * *')"

    assert "go run" in content and "/home/user/rolling_stats.go" in content, f"{cron_path} does not contain the correct command to execute the Go script"