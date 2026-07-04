# test_final_state.py

import time
import subprocess
import os
import pytest
import shutil

def test_backup_errors_performance_and_correctness():
    script_path = '/home/user/backup_errors.py'
    assert os.path.exists(script_path), f"Script not found at {script_path}"

    # Clear active_logs and backup_staging to ensure a clean test environment
    active_logs_dir = '/home/user/active_logs'
    staging_dir = '/home/user/backup_staging'

    for d in [active_logs_dir, staging_dir]:
        if os.path.exists(d):
            shutil.rmtree(d)
        os.makedirs(d)

    # 1. Generate a ~300MB JSON log file for the test
    log_path = os.path.join(active_logs_dir, 'test_huge.json')
    with open(log_path, 'w') as f:
        f.write('[\n')
        for i in range(2500000):
            if i == 1500000:
                f.write('{"timestamp": "2023-10-01T12:00:00Z", "level": "CRITICAL", "service": "auth", "message": "DB connection lost"},\n')
            else:
                f.write('{"timestamp": "2023-10-01T12:00:00Z", "level": "INFO", "service": "web", "message": "Request processed"}' + (',' if i < 2499999 else '') + '\n')
        f.write(']\n')

    # 2. Run the agent's script and measure time
    start_time = time.time()
    result = subprocess.run(['python3', script_path], capture_output=True, text=True)
    end_time = time.time()

    elapsed = end_time - start_time

    # Ensure the script completed successfully
    assert result.returncode == 0, f"Script failed with error:\n{result.stderr}"

    # 3. Check CSV contents
    csv_path = '/home/user/critical_logs.csv'
    assert os.path.exists(csv_path), "CSV not found at /home/user/critical_logs.csv"

    with open(csv_path, 'r') as f:
        content = f.read()
        assert "DB connection lost" in content, "Critical log not extracted to the CSV."
        assert "timestamp" in content and "service" in content and "message" in content, "CSV headers missing or incorrect."

    # Verify hard links were created
    staged_file = os.path.join(staging_dir, 'test_huge.json')
    assert os.path.exists(staged_file), "File was not hard-linked to the backup_staging directory."

    stat_active = os.stat(log_path)
    stat_staged = os.stat(staged_file)
    assert stat_active.st_ino == stat_staged.st_ino, "The file in backup_staging is not a hard link to the active log (inodes do not match)."

    # 4. Metric threshold assertion
    assert elapsed <= 4.0, f"Execution too slow: {elapsed:.2f} seconds (Threshold: 4.0s). The agent likely failed to fix the C-extension in the vendored package."