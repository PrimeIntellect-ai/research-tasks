# test_final_state.py
import os
import subprocess
import pytest

def test_cron_job_exists():
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True, check=True)
        crontab_content = result.stdout
    except subprocess.CalledProcessError:
        pytest.fail("Failed to read crontab or crontab is empty.")

    # Check if the correct cron job is present
    expected_cron = "*/15 * * * * /home/user/run_pipeline.sh"
    found = any(expected_cron in line for line in crontab_content.splitlines())
    assert found, f"Cron job '{expected_cron}' not found in crontab."

def test_executables_exist():
    cpp_binary = "/home/user/compute_dist"
    bash_script = "/home/user/run_pipeline.sh"

    assert os.path.isfile(cpp_binary), f"{cpp_binary} does not exist."
    assert os.access(cpp_binary, os.X_OK), f"{cpp_binary} is not executable."

    assert os.path.isfile(bash_script), f"{bash_script} does not exist."
    assert os.access(bash_script, os.X_OK), f"{bash_script} is not executable."

def test_pipeline_execution():
    # Setup test files just in case they were modified or deleted before the test
    incoming_dir = "/home/user/incoming"
    outgoing_dir = "/home/user/outgoing"
    os.makedirs(incoming_dir, exist_ok=True)
    os.makedirs(outgoing_dir, exist_ok=True)

    batch1 = os.path.join(incoming_dir, "batch1.csv")
    batch2 = os.path.join(incoming_dir, "batch2.csv")

    with open(batch1, 'w') as f:
        f.write("kitten,sitting\nflaw,lawn\nintent,execution\n")
    with open(batch2, 'w') as f:
        f.write("rosettacode,raisethysword\ndistance,difference\nparallel,unparallel\n")

    # Run the pipeline
    bash_script = "/home/user/run_pipeline.sh"
    try:
        subprocess.run([bash_script], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        pytest.fail(f"Execution of {bash_script} failed: {e.stderr}")

    # Verify incoming is empty
    remaining_files = os.listdir(incoming_dir)
    assert len(remaining_files) == 0, f"{incoming_dir} should be empty after running the pipeline, found: {remaining_files}"

    # Verify outgoing files
    out_batch1 = os.path.join(outgoing_dir, "batch1.csv")
    out_batch2 = os.path.join(outgoing_dir, "batch2.csv")

    assert os.path.isfile(out_batch1), f"{out_batch1} was not created."
    assert os.path.isfile(out_batch2), f"{out_batch2} was not created."

    with open(out_batch1, 'r') as f:
        content1 = f.read()

    assert "kitten,sitting,3" in content1, f"Expected 'kitten,sitting,3' in {out_batch1}"
    assert "flaw,lawn,4" in content1, f"Expected 'flaw,lawn,4' in {out_batch1}"
    assert "intent,execution,5" in content1, f"Expected 'intent,execution,5' in {out_batch1}"

    with open(out_batch2, 'r') as f:
        content2 = f.read()

    assert "rosettacode,raisethysword,8" in content2, f"Expected 'rosettacode,raisethysword,8' in {out_batch2}"
    assert "distance,difference,5" in content2, f"Expected 'distance,difference,5' in {out_batch2}"
    assert "parallel,unparallel,2" in content2, f"Expected 'parallel,unparallel,2' in {out_batch2}"