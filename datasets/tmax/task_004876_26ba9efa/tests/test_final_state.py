# test_final_state.py

import os
import re
import pytest

def test_pipeline_script_exists_and_executable():
    script_path = "/home/user/pipeline.sh"
    assert os.path.isfile(script_path), f"Pipeline script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Pipeline script {script_path} is not executable."

def test_processing_data_synced():
    src_dir = "/tmp/remote_drop"
    dest_dir = "/home/user/processing_data"

    assert os.path.isdir(dest_dir), f"Destination directory {dest_dir} does not exist."

    src_files = os.listdir(src_dir)
    assert len(src_files) > 0, f"Source directory {src_dir} is empty."

    for f in src_files:
        dest_file = os.path.join(dest_dir, f)
        assert os.path.isfile(dest_file), f"File {f} was not synchronized to {dest_dir}."

def test_latest_match_log():
    log_path = "/home/user/latest_match.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        content = f.read().strip()

    assert content == "doc3.txt,0.6154", f"Expected 'doc3.txt,0.6154' in {log_path}, but got '{content}'."

def test_crontab_dump():
    dump_path = "/home/user/crontab_dump.txt"
    assert os.path.isfile(dump_path), f"Crontab dump file {dump_path} does not exist."

    with open(dump_path, "r") as f:
        lines = f.readlines()

    found_cron = False
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Check for every 15 minutes schedule: "*/15 * * * *" or "0,15,30,45 * * * *"
        # and checking if it runs /home/user/pipeline.sh
        if re.search(r'^(\*/15|0,15,30,45)\s+\*\s+\*\s+\*\s+\*', line) and "/home/user/pipeline.sh" in line:
            found_cron = True
            break

    assert found_cron, f"Could not find a valid cron job for running /home/user/pipeline.sh every 15 minutes in {dump_path}."