# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def test_scripts_exist_and_executable():
    scripts = [
        "/home/user/validate.sh",
        "/home/user/process.sh",
        "/home/user/setup_cron.sh"
    ]
    for script in scripts:
        assert os.path.isfile(script), f"Script {script} does not exist."
        assert os.access(script, os.X_OK), f"Script {script} is not executable."

def test_validate_corpus():
    script_path = "/home/user/validate.sh"
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.csv')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.csv')]

    clean_failed = []
    for cf in clean_files:
        result = subprocess.run([script_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_failed = []
    for ef in evil_files:
        result = subprocess.run([script_path, ef], capture_output=True)
        if result.returncode == 0:
            evil_failed.append(os.path.basename(ef))

    assert not clean_failed, f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}"
    assert not evil_failed, f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}"

def test_process_logic():
    script_path = "/home/user/process.sh"

    # Create a dummy CSV
    csv_content = """timestamp,sensor_id,value,status
2023-10-01T10:05:00Z,1,10.5,ok
2023-10-01T10:15:00Z,2,11.0,ok
2023-10-01T10:25:00Z,3,12.0,ok
2023-10-01T11:05:00Z,1,10.0,ok
2023-10-01T11:15:00Z,2,11.5,ok
2023-10-01T11:25:00Z,3,12.5,ok
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
        tmp.write(csv_content)
        tmp_path = tmp.name

    try:
        # Assuming process.sh reads from file or stdin. The prompt says "reads a clean CSV", 
        # but doesn't specify if it's passed as arg or stdin. Let's try stdin first, then arg.
        # "Write a script... that reads a clean CSV, applies the time-based bucketing... outputs to stdout"
        # We will pass it via stdin.
        with open(tmp_path, 'r') as f:
            result = subprocess.run([script_path, tmp_path], capture_output=True, text=True)
            if not result.stdout.strip():
                # fallback to stdin
                f.seek(0)
                result = subprocess.run([script_path], stdin=f, capture_output=True, text=True)

        output_lines = [line for line in result.stdout.strip().split('\n') if line]

        # We expect 4 lines (2 for hour 10, 2 for hour 11) + maybe header.
        data_lines = [line for line in output_lines if '2023' in line]

        hour_10 = [line for line in data_lines if 'T10:' in line]
        hour_11 = [line for line in data_lines if 'T11:' in line]

        assert len(hour_10) == 2, f"Expected 2 rows for hour 10, got {len(hour_10)}"
        assert len(hour_11) == 2, f"Expected 2 rows for hour 11, got {len(hour_11)}"

    finally:
        os.remove(tmp_path)

def test_cron_setup():
    script_path = "/home/user/setup_cron.sh"

    # Run the setup script
    subprocess.run([script_path], check=True)

    # Check crontab
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Crontab was not installed successfully."

    cron_jobs = result.stdout.strip()
    assert "/home/user/pipeline.sh" in cron_jobs, "pipeline.sh is not in crontab."

    # Check schedule "0 */4 * * *"
    # The actual line might have different spacing, so we check for the pattern
    import re
    assert re.search(r'^0\s+\*/4\s+\*\s+\*\s+\*.*pipeline\.sh', cron_jobs, re.MULTILINE), f"Crontab schedule is incorrect. Got: {cron_jobs}"