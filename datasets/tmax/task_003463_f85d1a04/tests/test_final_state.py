# test_final_state.py
import os
import sys
import stat
import subprocess
import pytest
import importlib.util

def test_pipeline_script():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Missing script at {script_path}"

    # Check if executable
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable"

    # Run the script and check output
    result = subprocess.run([script_path], capture_output=True, text=True)
    assert "Pipeline running" in result.stdout, f"Script output did not contain 'Pipeline running'. Output: {result.stdout}"

def test_cron_job():
    # Check crontab for user
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    # The output should contain * * * * * /home/user/pipeline.sh
    assert result.returncode == 0, "Failed to list crontab"
    lines = result.stdout.strip().split('\n')
    found = False
    for line in lines:
        if line.startswith('#'):
            continue
        if "/home/user/pipeline.sh" in line and line.startswith("* * * * *"):
            found = True
            break
    assert found, f"Cron job for /home/user/pipeline.sh running every minute not found. Crontab: {result.stdout}"

def test_validator_corpus():
    validator_path = "/home/user/validator.py"
    assert os.path.isfile(validator_path), f"Missing validator module at {validator_path}"

    # Import the module
    spec = importlib.util.spec_from_file_location("validator", validator_path)
    validator = importlib.util.module_from_spec(spec)
    sys.modules["validator"] = validator
    try:
        spec.loader.exec_module(validator)
    except Exception as e:
        pytest.fail(f"Failed to import {validator_path}: {e}")

    assert hasattr(validator, "process_and_validate"), f"Function process_and_validate not found in {validator_path}"

    process_and_validate = validator.process_and_validate

    evil_dir = "/app/corpora/evil"
    clean_dir = "/app/corpora/clean"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_failures = []
    for f in evil_files:
        try:
            result = process_and_validate(f)
            if result is not False:
                evil_failures.append(os.path.basename(f))
        except Exception as e:
            # If it crashes on evil, we might consider it rejected, but typically it should return False
            evil_failures.append(f"{os.path.basename(f)} (crashed: {e})")

    clean_failures = []
    for f in clean_files:
        try:
            result = process_and_validate(f)
            if result is not True:
                clean_failures.append(os.path.basename(f))
        except Exception as e:
            clean_failures.append(f"{os.path.basename(f)} (crashed: {e})")

    error_msgs = []
    if evil_failures:
        error_msgs.append(f"{len(evil_failures)} of {len(evil_files)} evil bypassed: {', '.join(evil_failures)}")
    if clean_failures:
        error_msgs.append(f"{len(clean_failures)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failures)}")

    if error_msgs:
        pytest.fail(" | ".join(error_msgs))