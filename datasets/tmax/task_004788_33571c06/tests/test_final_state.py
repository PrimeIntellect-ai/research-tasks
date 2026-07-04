# test_final_state.py
import os
import glob
import subprocess
from pathlib import Path
import pytest

def test_502_count():
    path = "/home/user/502_count.txt"
    assert os.path.exists(path), f"Expected file {path} is missing."
    with open(path, "r") as f:
        content = f.read().strip()
    assert content == "47", f"Expected count to be 47, but got '{content}'."

def test_restore_nginx():
    script = "/home/user/restore_nginx.sh"
    assert os.path.exists(script), f"Expected script {script} is missing."

    # Run the script once
    res1 = subprocess.run(["bash", script], capture_output=True, text=True)
    assert res1.returncode == 0, f"First run of restore_nginx.sh failed: {res1.stderr}"

    conf_dir = "/home/user/nginx_conf"
    assert os.path.exists(conf_dir), f"Directory {conf_dir} was not created."
    assert os.path.isdir(conf_dir), f"{conf_dir} is not a directory."

    conf_files = list(Path(conf_dir).glob("**/*.conf"))
    assert len(conf_files) > 0, "No .conf files found in the restored directory."

    for conf_file in conf_files:
        mode = os.stat(conf_file).st_mode & 0o777
        assert mode == 0o644, f"File {conf_file} has permissions {oct(mode)}, expected 0o644."

    # Run the script a second time for idempotency
    res2 = subprocess.run(["bash", script], capture_output=True, text=True)
    assert res2.returncode == 0, f"Second run of restore_nginx.sh failed (not idempotent): {res2.stderr}"

def test_manifest_filter():
    validators = glob.glob("/home/user/validator.*")
    assert validators, "No validator script found matching /home/user/validator.*"

    # Prefer an executable file if multiple exist, otherwise take the first
    validator = validators[0]
    for v in validators:
        if os.access(v, os.X_OK):
            validator = v
            break

    clean_dir = "/app/eval_corpus/clean"
    evil_dir = "/app/eval_corpus/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*"))
    evil_files = glob.glob(os.path.join(evil_dir, "*"))

    assert clean_files, f"No clean corpus files found in {clean_dir}"
    assert evil_files, f"No evil corpus files found in {evil_dir}"

    clean_failed = []
    for f in clean_files:
        res = subprocess.run([validator, f], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(f))

    evil_failed = []
    for f in evil_files:
        res = subprocess.run([validator, f], capture_output=True)
        if res.returncode == 0:
            evil_failed.append(os.path.basename(f))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_failed:
        errors.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed/accepted: {', '.join(evil_failed)}")

    if errors:
        pytest.fail(" | ".join(errors))

def test_expect_script():
    script = "/home/user/send_alert.exp"
    assert os.path.exists(script), f"Expected script {script} is missing."

    res = subprocess.run(["expect", script], capture_output=True, text=True)
    assert res.returncode == 0, f"Expect script failed to execute successfully.\nSTDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}"