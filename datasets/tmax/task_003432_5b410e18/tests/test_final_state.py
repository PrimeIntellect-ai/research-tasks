# test_final_state.py
import os
import pytest

def test_final_artifact_size():
    target_file = "/app/final_artifact.pck"
    assert os.path.exists(target_file), f"Final artifact {target_file} was not generated."

    size = os.path.getsize(target_file)
    threshold = 5000000
    assert size < threshold, f"Final artifact size {size} bytes exceeds the threshold of {threshold} bytes. The packer likely included vulnerable/deprecated files or fell into a symlink loop."

def test_packer_out_log_exists():
    log_path = "/app/logs/packer_out.log"
    assert os.path.exists(log_path), f"Packer stdout log {log_path} was not created. Ensure you redirected stdout."
    assert os.path.isfile(log_path), f"{log_path} is not a file."

def test_staging_directory_exists():
    staging_dir = "/app/staging"
    assert os.path.exists(staging_dir), f"Staging directory {staging_dir} does not exist."
    assert os.path.isdir(staging_dir), f"{staging_dir} is not a directory."