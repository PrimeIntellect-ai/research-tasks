# test_final_state.py

import os
import subprocess
import tarfile
import tempfile
import re

def test_gcode_validator_script_exists():
    assert os.path.isfile('/home/user/gcode_validator.py'), "The script /home/user/gcode_validator.py does not exist."

def test_adversarial_corpus():
    script_path = '/home/user/gcode_validator.py'
    clean_dir = '/app/corpora/clean'
    evil_dir = '/app/corpora/evil'

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if f.endswith('.gcode')]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if f.endswith('.gcode')]

    assert len(clean_files) > 0, "Clean corpus is empty."
    assert len(evil_files) > 0, "Evil corpus is empty."

    failed_clean = []
    for cf in clean_files:
        res = subprocess.run(['python3', script_path, cf], capture_output=True)
        if res.returncode != 0:
            failed_clean.append(os.path.basename(cf))

    failed_evil = []
    for ef in evil_files:
        res = subprocess.run(['python3', script_path, ef], capture_output=True)
        if res.returncode == 0:
            failed_evil.append(os.path.basename(ef))

    error_messages = []
    if failed_clean:
        error_messages.append(f"{len(failed_clean)} of {len(clean_files)} clean modified/rejected: {', '.join(failed_clean[:5])}")
    if failed_evil:
        error_messages.append(f"{len(failed_evil)} of {len(evil_files)} evil bypassed: {', '.join(failed_evil[:5])}")

    assert not error_messages, "Adversarial corpus failed:\n" + "\n".join(error_messages)

def is_gcode_valid(filepath):
    # X_max = 150.0, Y_max = 150.0, Z_min = -12.0, S_max = 10000.
    with open(filepath, 'r') as f:
        for line in f:
            line = line.split(';')[0].upper()

            x_match = re.search(r'X\s*(-?\d+(\.\d+)?)', line)
            if x_match and float(x_match.group(1)) > 150.0: return False

            y_match = re.search(r'Y\s*(-?\d+(\.\d+)?)', line)
            if y_match and float(y_match.group(1)) > 150.0: return False

            z_match = re.search(r'Z\s*(-?\d+(\.\d+)?)', line)
            if z_match and float(z_match.group(1)) < -12.0: return False

            s_match = re.search(r'S\s*(\d+(\.\d+)?)', line)
            if s_match and float(s_match.group(1)) > 10000.0: return False

    return True

def test_valid_projects_tarball():
    tarball_path = '/home/user/valid_projects.tar.gz'
    assert os.path.isfile(tarball_path), f"{tarball_path} is missing."

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(tarball_path, 'r:gz') as tar:
            members = tar.getmembers()
            for member in members:
                assert member.isfile(), f"Archive contains non-file: {member.name}"
                assert '/' not in member.name, f"Archive is not flat, contains nested path: {member.name}"
                assert member.name.endswith('.gcode'), f"Archive contains non-gcode file: {member.name}"

            tar.extractall(path=tmpdir)

            for member in members:
                extracted_path = os.path.join(tmpdir, member.name)
                assert is_gcode_valid(extracted_path), f"File {member.name} in archive is not valid."

    # Verify all valid files from legacy_projects are present
    legacy_tarball = '/app/legacy_projects.tar.gz'
    expected_valid_files = set()
    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(legacy_tarball, 'r:gz') as tar:
            tar.extractall(path=tmpdir)
            for root, _, files in os.walk(tmpdir):
                for file in files:
                    if file.endswith('.gcode'):
                        filepath = os.path.join(root, file)
                        if is_gcode_valid(filepath):
                            expected_valid_files.add(file)

    with tarfile.open(tarball_path, 'r:gz') as tar:
        actual_files = set(m.name for m in tar.getmembers())

    missing = expected_valid_files - actual_files
    extra = actual_files - expected_valid_files

    assert not missing, f"Missing valid files in archive: {', '.join(list(missing)[:5])}"
    assert not extra, f"Extra invalid files in archive: {', '.join(list(extra)[:5])}"