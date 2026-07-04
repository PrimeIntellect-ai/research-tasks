# test_final_state.py
import os
import json
import subprocess
import pytest

def test_config_json():
    config_path = "/home/user/app/services/config.json"
    assert os.path.isfile(config_path), f"Config file {config_path} is missing."

    with open(config_path, "r") as f:
        try:
            config = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"Config file {config_path} is not valid JSON.")

    assert config.get("webhook_url") == "http://127.0.0.1:8080/provision", "webhook_url is not correctly configured."
    assert config.get("api_host") == "127.0.0.1", "api_host is not correctly configured."

def test_filter_py_adversarial_corpus():
    filter_script = "/home/user/app/filter.py"
    assert os.path.isfile(filter_script), f"Filter script {filter_script} is missing."

    evil_dir = "/home/user/corpora/evil/"
    clean_dir = "/home/user/corpora/clean/"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir)] if os.path.isdir(evil_dir) else []
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir)] if os.path.isdir(clean_dir) else []

    evil_bypassed = []
    for f in evil_files:
        res = subprocess.run(["python3", filter_script, f], capture_output=True)
        if res.returncode != 1:
            evil_bypassed.append(os.path.basename(f))

    clean_modified = []
    for f in clean_files:
        res = subprocess.run(["python3", filter_script, f], capture_output=True)
        if res.returncode != 0:
            clean_modified.append(os.path.basename(f))

    errors = []
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        errors.append(f"{len(clean_modified)} of {len(clean_files)} clean modified (rejected): {', '.join(clean_modified)}")

    if errors:
        pytest.fail(" | ".join(errors))

def test_create_skel_sh():
    skel_script = "/home/user/app/create_skel.sh"
    assert os.path.isfile(skel_script), f"Script {skel_script} is missing."
    assert os.access(skel_script, os.X_OK), f"Script {skel_script} is not executable."

    username = "testuser99"
    res = subprocess.run([skel_script, username], capture_output=True, text=True)
    assert res.returncode == 0, f"Script failed with exit code {res.returncode}. stderr: {res.stderr}"

    storage_dir = f"/home/user/accounts/{username}/storage/"
    shared_link = f"/home/user/accounts/{username}/shared"
    user_conf = f"/home/user/accounts/{username}/user.conf"

    assert os.path.isdir(storage_dir), "Storage directory was not created."
    assert os.path.islink(shared_link), "Shared symlink was not created."
    assert os.readlink(shared_link) == "/home/user/shared_data/", "Shared symlink points to the wrong target."

    assert os.path.isfile(user_conf), "user.conf was not created."
    with open(user_conf, "r") as f:
        assert "status=active" in f.read(), "user.conf does not contain status=active."

    # Test idempotency
    with open(user_conf, "w") as f:
        f.write("status=inactive")
    res = subprocess.run([skel_script, username], capture_output=True, text=True)
    assert res.returncode == 0, "Idempotency test failed: script returned non-zero exit code on second run."
    with open(user_conf, "r") as f:
        assert "status=inactive" in f.read(), "Idempotency test failed: user.conf was overwritten."

    # Test quota
    large_file = "/home/user/accounts/large_dummy"
    with open(large_file, "wb") as f:
        f.write(b"0" * 5000001)

    try:
        res = subprocess.run([skel_script, "testuser_quota"], capture_output=True, text=True)
        assert res.returncode == 2, f"Quota test failed: expected exit code 2, got {res.returncode}."
        assert res.stdout.strip() == "QUOTA_EXCEEDED", f"Quota test failed: expected stdout 'QUOTA_EXCEEDED', got '{res.stdout.strip()}'"
    finally:
        if os.path.exists(large_file):
            os.remove(large_file)