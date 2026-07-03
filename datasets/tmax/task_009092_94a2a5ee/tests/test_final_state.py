# test_final_state.py
import os
import stat
import subprocess
import pytest

def test_run_pipeline_sh():
    """Test that run_pipeline.sh exists, is executable, and runs successfully."""
    script_path = "/home/user/run_pipeline.sh"
    assert os.path.isfile(script_path), f"{script_path} does not exist."

    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"{script_path} is not executable."

    # Remove outputs if they exist to ensure the script actually generates them
    for fpath in ["/home/user/clean_events.csv", "/home/user/aggregated_events.csv", "/home/user/etl_processor"]:
        if os.path.exists(fpath):
            os.remove(fpath)

    # Run the script
    result = subprocess.run([script_path], cwd="/home/user", capture_output=True, text=True)
    assert result.returncode == 0, f"Running {script_path} failed with return code {result.returncode}.\nStderr: {result.stderr}"

def test_clean_events_content():
    """Test that clean_events.csv has the correctly deduplicated and masked data."""
    file_path = "/home/user/clean_events.csv"
    assert os.path.isfile(file_path), f"{file_path} was not created by the pipeline."

    expected_lines = [
        "1700000000,101,MASKED,101@anonymized.local,click",
        "1700000050,102,MASKED,102@anonymized.local,view",
        "1700003500,103,MASKED,103@anonymized.local,purchase",
        "1700003600,101,MASKED,101@anonymized.local,view",
        "1700007200,104,MASKED,104@anonymized.local,click"
    ]

    with open(file_path, "r") as f:
        content = f.read().strip().splitlines()

    assert content == expected_lines, f"Content of {file_path} does not match the expected output."

def test_aggregated_events_content():
    """Test that aggregated_events.csv has the correctly bucketed and aggregated counts."""
    file_path = "/home/user/aggregated_events.csv"
    assert os.path.isfile(file_path), f"{file_path} was not created by the pipeline."

    expected_lines = [
        "1699999200,click,1",
        "1699999200,view,1",
        "1700002800,purchase,1",
        "1700002800,view,1",
        "1700006400,click,1"
    ]

    with open(file_path, "r") as f:
        content = f.read().strip().splitlines()

    assert content == expected_lines, f"Content of {file_path} does not match the expected output."

def test_cron_txt_content():
    """Test that cron.txt contains the correct schedule and script path."""
    file_path = "/home/user/cron.txt"
    assert os.path.isfile(file_path), f"{file_path} does not exist."

    with open(file_path, "r") as f:
        content = f.read().strip()

    # Allow multiple spaces/tabs between cron fields by splitting and checking the first 5 fields
    parts = content.split()
    assert len(parts) >= 6, "cron.txt content is incomplete or malformed."

    cron_schedule = " ".join(parts[:5])
    assert cron_schedule == "0 * * * *", f"Expected cron schedule '0 * * * *', but got '{cron_schedule}'."
    assert "/home/user/run_pipeline.sh" in content, "cron.txt does not contain the expected script path '/home/user/run_pipeline.sh'."