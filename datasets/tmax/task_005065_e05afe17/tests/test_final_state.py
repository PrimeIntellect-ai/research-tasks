# test_final_state.py
import os
import subprocess
import glob
import json
import pytest

def test_filter_executable_exists():
    assert os.path.isfile('/home/user/filter'), "The C++ filter binary is missing at /home/user/filter."
    assert os.access('/home/user/filter', os.X_OK), "The C++ filter binary is not executable."

def test_adversarial_corpus():
    clean_dir = "/app/corpus/clean"
    evil_dir = "/app/corpus/evil"
    filter_bin = "/home/user/filter"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    for f in clean_files:
        res = subprocess.run([filter_bin, f], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(f))

    evil_failed = []
    for f in evil_files:
        res = subprocess.run([filter_bin, f], capture_output=True)
        if res.returncode == 0:
            evil_failed.append(os.path.basename(f))

    error_msgs = []
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")

    assert not error_msgs, "Adversarial corpus verification failed: " + " | ".join(error_msgs)

def test_pipeline_script():
    pipeline_script = "/home/user/pipeline.sh"
    assert os.path.isfile(pipeline_script), f"{pipeline_script} is missing."

    # Run the pipeline script to ensure it works
    res = subprocess.run(["bash", pipeline_script], capture_output=True)
    assert res.returncode == 0, f"pipeline.sh failed with exit code {res.returncode}. stderr: {res.stderr.decode()}"

    approved_dir = "/home/user/approved_deployments"
    assert os.path.isdir(approved_dir), f"{approved_dir} was not created."

    # Verify symlinks
    raw_files = glob.glob("/app/corpus/raw/*.json")
    valid_raw_files = []
    for f in raw_files:
        with open(f, 'r') as fp:
            try:
                data = json.load(fp)
                if "CostCenter=FinOps" in data.get("tags", []):
                    valid_raw_files.append(f)
            except Exception:
                pass

    symlinks = glob.glob(os.path.join(approved_dir, "*.json"))
    assert len(symlinks) == len(valid_raw_files), f"Expected {len(valid_raw_files)} symlinks, found {len(symlinks)}."

    for sl in symlinks:
        assert os.path.islink(sl), f"{sl} is not a symbolic link."
        target = os.readlink(sl)
        assert os.path.isabs(target) or os.path.exists(os.path.join(approved_dir, target)), f"Broken symlink {sl}"

def test_expect_script():
    expect_script = "/home/user/auto_deploy.exp"
    assert os.path.isfile(expect_script), f"{expect_script} is missing."

    # Run the expect script
    res = subprocess.run(["expect", expect_script], capture_output=True)
    assert res.returncode == 0, f"auto_deploy.exp failed with exit code {res.returncode}. Output: {res.stdout.decode()} {res.stderr.decode()}"