# test_final_state.py

import os
import sys
import tarfile
import tempfile
import subprocess
import re
import pytest

# Add /home/user to sys.path to import archiver.py
sys.path.insert(0, "/home/user")

def test_archiver_evil_corpus():
    try:
        from archiver import sanitize_and_archive
    except ImportError:
        pytest.fail("Could not import archiver.py. Ensure it exists at /home/user/archiver.py and has the correct function.")

    evil_dir = "/home/user/corpora/evil"
    if not os.path.isdir(evil_dir):
        pytest.fail(f"Evil corpus directory missing: {evil_dir}")

    evil_files = os.listdir(evil_dir)
    bypassed_files = []

    for filename in evil_files:
        input_path = os.path.join(evil_dir, filename)
        with tempfile.TemporaryDirectory() as tmpdir:
            output_archive = os.path.join(tmpdir, f"{filename}.tar.gz")

            try:
                result = sanitize_and_archive(input_path, output_archive)
            except Exception as e:
                # If it crashes on evil input, we consider it failing to gracefully reject/sanitize
                bypassed_files.append(f"{filename} (crashed: {e})")
                continue

            if result is False:
                # Rejected properly (e.g. binary file)
                continue

            if result is True:
                # Need to verify it was sanitized
                if not os.path.isfile(output_archive):
                    bypassed_files.append(f"{filename} (returned True but no archive created)")
                    continue

                # Extract and check contents
                try:
                    with tarfile.open(output_archive, "r:gz") as tar:
                        members = tar.getmembers()
                        if not members:
                            bypassed_files.append(f"{filename} (empty archive)")
                            continue
                        extracted_file = tar.extractfile(members[0])
                        if not extracted_file:
                            bypassed_files.append(f"{filename} (could not read extracted file)")
                            continue
                        content = extracted_file.read().decode('utf-8', errors='replace')

                        # Check for raw CCs (16 digits, with or without dashes)
                        # A simple regex for CCs: \b(?:\d[ -]*?){15}\d\b
                        cc_pattern = re.compile(r'\b(?:\d[ -]*?){15}\d\b')
                        if cc_pattern.search(content):
                            bypassed_files.append(f"{filename} (unsanitized CC found)")
                            continue

                        # Check for RSA private key
                        if "-----BEGIN RSA PRIVATE KEY-----" in content:
                            bypassed_files.append(f"{filename} (unsanitized RSA key found)")
                            continue
                except Exception as e:
                    bypassed_files.append(f"{filename} (error extracting/verifying archive: {e})")
            else:
                bypassed_files.append(f"{filename} (returned non-boolean)")

    if bypassed_files:
        pytest.fail(f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: " + ", ".join(bypassed_files))


def test_archiver_clean_corpus():
    try:
        from archiver import sanitize_and_archive
    except ImportError:
        pytest.fail("Could not import archiver.py.")

    clean_dir = "/home/user/corpora/clean"
    if not os.path.isdir(clean_dir):
        pytest.fail(f"Clean corpus directory missing: {clean_dir}")

    clean_files = os.listdir(clean_dir)
    modified_files = []

    for filename in clean_files:
        input_path = os.path.join(clean_dir, filename)
        with open(input_path, 'r', encoding='utf-8') as f:
            original_content = f.read()

        with tempfile.TemporaryDirectory() as tmpdir:
            output_archive = os.path.join(tmpdir, f"{filename}.tar.gz")

            try:
                result = sanitize_and_archive(input_path, output_archive)
            except Exception as e:
                modified_files.append(f"{filename} (crashed: {e})")
                continue

            if result is not True:
                modified_files.append(f"{filename} (returned False or rejected)")
                continue

            if not os.path.isfile(output_archive):
                modified_files.append(f"{filename} (returned True but no archive created)")
                continue

            try:
                with tarfile.open(output_archive, "r:gz") as tar:
                    members = tar.getmembers()
                    if not members:
                        modified_files.append(f"{filename} (empty archive)")
                        continue
                    extracted_file = tar.extractfile(members[0])
                    if not extracted_file:
                        modified_files.append(f"{filename} (could not read extracted file)")
                        continue
                    content = extracted_file.read().decode('utf-8', errors='replace')

                    if content != original_content:
                        modified_files.append(f"{filename} (content modified)")
            except Exception as e:
                modified_files.append(f"{filename} (error extracting archive: {e})")

    if modified_files:
        pytest.fail(f"{len(modified_files)} of {len(clean_files)} clean modified or rejected: " + ", ".join(modified_files))

def test_config_ini():
    config_path = "/home/user/app/config.ini"
    assert os.path.isfile(config_path), "config.ini missing"
    with open(config_path, "r") as f:
        content = f.read()

    # Check if archiver_cmd points to python /home/user/archiver.py --input %I --output %O
    # or similar
    assert "python /home/user/archiver.py" in content, "config.ini does not point to python /home/user/archiver.py"

def test_start_pipeline_script_exists():
    script_path = "/home/user/start_pipeline.sh"
    assert os.path.isfile(script_path), "start_pipeline.sh is missing"
    assert os.access(script_path, os.X_OK) or os.stat(script_path).st_mode & 0o111, "start_pipeline.sh is not executable"