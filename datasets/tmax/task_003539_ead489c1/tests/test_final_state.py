# test_final_state.py
import os
import stat
import subprocess
import csv
import re

def test_scripts_exist():
    assert os.path.exists('/home/user/extract.py'), "/home/user/extract.py is missing."
    assert os.path.exists('/home/user/compute.py'), "/home/user/compute.py is missing."
    assert os.path.exists('/home/user/pipeline.sh'), "/home/user/pipeline.sh is missing."

    # Check if pipeline.sh is executable
    st = os.stat('/home/user/pipeline.sh')
    assert bool(st.st_mode & stat.S_IXUSR), "/home/user/pipeline.sh is not executable."

def test_cron_file():
    cron_path = '/home/user/schedule.cron'
    assert os.path.exists(cron_path), f"{cron_path} is missing."

    with open(cron_path, 'r') as f:
        content = f.read().strip()

    # Check for correct 15-minute interval syntax
    valid_prefixes = ["*/15 * * * *", "0,15,30,45 * * * *"]
    has_valid_prefix = any(content.startswith(prefix) for prefix in valid_prefixes)
    assert has_valid_prefix, f"Cron schedule does not match every 15 minutes. Found: {content}"

    assert "/home/user/pipeline.sh" in content, "Cron file does not contain the pipeline script path."

def test_pipeline_execution_and_output():
    incoming_dir = '/home/user/incoming_logs'
    archive_dir = '/home/user/archive'
    output_csv = '/home/user/output_metrics.csv'

    # If day1.log is still in incoming_logs, the pipeline hasn't been run or failed to move it.
    # We execute it to test the agent's scripts.
    if os.path.exists(os.path.join(incoming_dir, 'day1.log')):
        try:
            subprocess.run(['/bin/bash', '/home/user/pipeline.sh'], cwd='/home/user', check=True)
        except subprocess.CalledProcessError as e:
            assert False, f"Executing pipeline.sh failed with return code {e.returncode}"

    assert os.path.exists(output_csv), f"{output_csv} was not created."

    with open(output_csv, 'r') as f:
        reader = csv.reader(f)
        rows = [row for row in reader if row] # filter out empty lines

    assert len(rows) > 0, "output_metrics.csv is empty."
    assert rows[0] == ['route_id', 'distance'], f"Incorrect CSV header. Expected ['route_id', 'distance'], got {rows[0]}"

    expected_data = [
        ['alpha-01', '5.00'],
        ['beta-02', '5.00'],
        ['delta-04', '12.00']
    ]

    data_rows = rows[1:]
    assert data_rows == expected_data, f"CSV data mismatch.\nExpected:\n{expected_data}\nGot:\n{data_rows}"

    # Check that logs were moved to archive
    assert not os.path.exists(os.path.join(incoming_dir, 'day1.log')), "day1.log was not removed from incoming_logs."
    assert os.path.exists(os.path.join(archive_dir, 'day1.log')), "day1.log was not moved to archive."