# test_final_state.py

import os
import pytest

def test_final_artifacts_count():
    """Verify that exactly 50 artifacts were successfully uploaded and moved to the final directory."""
    final_dir = '/home/user/artifacts/final'
    assert os.path.isdir(final_dir), f"Final directory {final_dir} does not exist. Did you upload the files?"

    files = [f for f in os.listdir(final_dir) if os.path.isfile(os.path.join(final_dir, f))]
    assert len(files) == 50, f"Expected exactly 50 files in {final_dir}, but found {len(files)}."

def test_final_artifacts_size_threshold():
    """Verify that the total size of the artifacts is below the threshold, indicating they were stripped."""
    final_dir = '/home/user/artifacts/final'
    assert os.path.isdir(final_dir), f"Final directory {final_dir} does not exist."

    total_size = sum(
        os.path.getsize(os.path.join(final_dir, f)) 
        for f in os.listdir(final_dir) 
        if os.path.isfile(os.path.join(final_dir, f))
    )

    threshold = 800000
    assert total_size < threshold, (
        f"Total size of artifacts is {total_size} bytes, which is >= {threshold} bytes. "
        "Did you strip the debug symbols from the binaries before uploading?"
    )

def test_final_artifacts_naming_convention():
    """Verify that the artifacts follow the required naming convention."""
    final_dir = '/home/user/artifacts/final'
    assert os.path.isdir(final_dir), f"Final directory {final_dir} does not exist."

    files = [f for f in os.listdir(final_dir) if os.path.isfile(os.path.join(final_dir, f))]

    # We expect files to start with 'arch_'
    for f in files:
        assert f.startswith("arch_"), f"File {f} does not follow the naming convention 'arch_<architecture_string>_<original_filename>'."
        assert " " not in f, f"File {f} contains spaces, which should have been replaced by hyphens."

def test_services_configured_correctly():
    """Verify that the configuration files were updated properly."""
    nginx_conf = "/app/nginx.conf"
    if os.path.isfile(nginx_conf):
        with open(nginx_conf, 'r') as f:
            content = f.read()
            assert "127.0.0.1:5000" in content, "Nginx config does not point to the correct Flask port (5000)."

    env_file = "/app/.env"
    if os.path.isfile(env_file):
        with open(env_file, 'r') as f:
            content = f.read()
            assert "6379" in content, "Flask .env does not point to the correct Redis port (6379)."