# test_final_state.py

import os
import subprocess
import tempfile
import glob

def test_scripts_exist():
    """Verify that the required scripts exist."""
    assert os.path.isfile('/home/user/filter.py'), "/home/user/filter.py does not exist."
    assert os.path.isfile('/home/user/run_pipeline.sh'), "/home/user/run_pipeline.sh does not exist."

def test_cron_job_installed():
    """Verify that the correct cron job is installed for the user."""
    try:
        # Check crontab for 'user'
        result = subprocess.run(['crontab', '-l', '-u', 'user'], capture_output=True, text=True, check=True)
        crontab_content = result.stdout
    except subprocess.CalledProcessError:
        # Fallback to checking root if the user was root or no user crontab exists
        try:
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True, check=True)
            crontab_content = result.stdout
        except subprocess.CalledProcessError:
            crontab_content = ""

    assert crontab_content.strip() != "", "No crontab found."

    # Look for the schedule and the script
    # The schedule from the image is */10 * * * *
    found_cron = False
    for line in crontab_content.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if '*/10 * * * *' in line and '/home/user/run_pipeline.sh' in line:
            found_cron = True
            break

    assert found_cron, "The required cron job '*/10 * * * * /home/user/run_pipeline.sh' was not found in the crontab."

def test_filter_clean_corpus():
    """Verify that the filter preserves 100% of the clean corpus."""
    clean_dir = '/app/corpora/clean'
    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} is missing."

    clean_files = glob.glob(os.path.join(clean_dir, '*'))
    assert len(clean_files) > 0, "No files found in clean corpus."

    modified_files = []

    for input_file in clean_files:
        with tempfile.NamedTemporaryFile(delete=False) as temp_out:
            output_file = temp_out.name

        try:
            subprocess.run(
                ['python3', '/home/user/filter.py', input_file, output_file],
                check=True,
                capture_output=True
            )

            with open(input_file, 'r', encoding='utf-8') as f:
                expected_lines = f.readlines()
            with open(output_file, 'r', encoding='utf-8') as f:
                actual_lines = f.readlines()

            if expected_lines != actual_lines:
                modified_files.append(os.path.basename(input_file))
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)

    assert not modified_files, f"{len(modified_files)} of {len(clean_files)} clean files modified: {', '.join(modified_files)}"

def test_filter_evil_corpus():
    """Verify that the filter drops 100% of the evil corpus."""
    evil_dir = '/app/corpora/evil'
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} is missing."

    evil_files = glob.glob(os.path.join(evil_dir, '*'))
    assert len(evil_files) > 0, "No files found in evil corpus."

    bypassed_files = []

    for input_file in evil_files:
        with tempfile.NamedTemporaryFile(delete=False) as temp_out:
            output_file = temp_out.name

        try:
            subprocess.run(
                ['python3', '/home/user/filter.py', input_file, output_file],
                check=True,
                capture_output=True
            )

            with open(output_file, 'r', encoding='utf-8') as f:
                actual_lines = f.readlines()

            if len(actual_lines) > 0:
                bypassed_files.append(os.path.basename(input_file))
        finally:
            if os.path.exists(output_file):
                os.remove(output_file)

    assert not bypassed_files, f"{len(bypassed_files)} of {len(evil_files)} evil files bypassed: {', '.join(bypassed_files)}"