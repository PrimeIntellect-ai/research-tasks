# test_final_state.py

import os
import subprocess
import stat

def test_aggregate_c_exists():
    """Test that the C program source file exists."""
    assert os.path.isfile('/home/user/aggregate.c'), "/home/user/aggregate.c does not exist."

def test_run_pipeline_script_exists_and_executable():
    """Test that the shell script exists and is executable."""
    script_path = '/home/user/run_pipeline.sh'
    assert os.path.isfile(script_path), f"{script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

def test_pipeline_execution_and_output():
    """Test that running the pipeline works and produces the correct summary.csv."""
    script_path = '/home/user/run_pipeline.sh'
    summary_path = '/home/user/summary.csv'

    # Remove summary.csv and aggregate executable if they exist to ensure the script recreates them
    if os.path.exists(summary_path):
        os.remove(summary_path)
    if os.path.exists('/home/user/aggregate'):
        os.remove('/home/user/aggregate')

    # Run the script
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script failed with return code {result.returncode}. stderr: {result.stderr}"

    assert os.path.isfile('/home/user/aggregate'), "The executable /home/user/aggregate was not created."
    assert os.path.isfile(summary_path), f"{summary_path} was not created."

    with open(summary_path, 'r') as f:
        content = f.read().strip().split('\n')

    expected_content = [
        "472222,9.00",
        "472223,6.50",
        "472224,13.00"
    ]

    assert content == expected_content, f"Expected summary.csv content {expected_content}, but got {content}."

def test_cron_job_installed():
    """Test that the cron job is installed correctly."""
    result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab."

    cron_jobs = result.stdout.strip().split('\n')
    expected_command = '/home/user/run_pipeline.sh'

    found = False
    for job in cron_jobs:
        if job.startswith('#') or not job.strip():
            continue
        parts = job.split()
        if len(parts) >= 6:
            minute, hour, dom, mon, dow = parts[:5]
            command = ' '.join(parts[5:])
            if minute == '15' and hour == '*' and dom == '*' and mon == '*' and dow == '*' and expected_command in command:
                found = True
                break

    assert found, "Cron job for /home/user/run_pipeline.sh at 15 minutes past every hour is not installed."