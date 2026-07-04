# test_final_state.py

import os
import json
import stat
import subprocess
import pytest
import glob

def test_pexpect_installed():
    """Verify pexpect 4.8.0 is installed in the virtual environment."""
    python_bin = "/home/user/venv/bin/python"
    assert os.path.isfile(python_bin), f"Virtual environment Python not found at {python_bin}"

    result = subprocess.run(
        [python_bin, "-c", "import pexpect; print(pexpect.__version__)"],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"Failed to import pexpect: {result.stderr}"
    assert result.stdout.strip() == "4.8.0", f"Expected pexpect version 4.8.0, got {result.stdout.strip()}"

def test_sanitise_users_adversarial_corpus(tmp_path):
    """Verify the sanitiser script correctly processes clean and evil corpora."""
    script_path = "/home/user/sanitise_users.py"
    assert os.path.isfile(script_path), f"Sanitiser script not found at {script_path}"

    evil_corpus_dir = "/app/tests/corpus/evil/"
    clean_corpus_dir = "/app/tests/corpus/clean/"

    evil_files = glob.glob(os.path.join(evil_corpus_dir, "*.json"))
    clean_files = glob.glob(os.path.join(clean_corpus_dir, "*.json"))

    assert len(evil_files) > 0, "No evil corpus files found."
    assert len(clean_files) > 0, "No clean corpus files found."

    evil_bypassed = []
    clean_modified = []

    # Test evil corpus
    for evil_file in evil_files:
        output_file = tmp_path / f"out_evil_{os.path.basename(evil_file)}"
        result = subprocess.run(
            ["python3", script_path, evil_file, str(output_file)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Script failed on {evil_file}: {result.stderr}"
        assert os.path.isfile(output_file), f"Output file not created for {evil_file}"

        with open(output_file, "r") as f:
            try:
                out_data = json.load(f)
            except json.JSONDecodeError:
                out_data = None

        if out_data != []:
            evil_bypassed.append(os.path.basename(evil_file))

    # Test clean corpus
    for clean_file in clean_files:
        output_file = tmp_path / f"out_clean_{os.path.basename(clean_file)}"
        result = subprocess.run(
            ["python3", script_path, clean_file, str(output_file)],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, f"Script failed on {clean_file}: {result.stderr}"
        assert os.path.isfile(output_file), f"Output file not created for {clean_file}"

        with open(clean_file, "r") as f:
            in_data = json.load(f)

        with open(output_file, "r") as f:
            try:
                out_data = json.load(f)
            except json.JSONDecodeError:
                out_data = None

        if out_data != in_data:
            clean_modified.append(os.path.basename(clean_file))

    error_msgs = []
    if evil_bypassed:
        error_msgs.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msgs.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    assert not error_msgs, " | ".join(error_msgs)

def test_cron_job_loaded():
    """Verify the cron job is correctly loaded into crontab."""
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab. Was it loaded?"

    crontab_content = result.stdout
    assert "/home/user/venv/bin/python" in crontab_content, "Crontab does not use the venv python."
    assert "/home/user/orchestrator.py" in crontab_content, "Crontab does not execute orchestrator.py."
    assert "/home/user/account_sync/output/sync.log" in crontab_content, "Crontab does not redirect output to the correct log file."

def test_directory_permissions():
    """Verify the output directory exists and has 0755 permissions."""
    target_dir = "/home/user/account_sync/output"
    assert os.path.isdir(target_dir), f"Directory does not exist: {target_dir}"

    st = os.stat(target_dir)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o755, f"Expected permissions 0755, got {oct(permissions)}"