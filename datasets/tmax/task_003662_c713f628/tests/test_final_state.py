# test_final_state.py
import os
import subprocess
import pytest
import json
import re

def test_adversarial_corpus():
    validator = "/home/user/verify_telemetry.sh"
    assert os.path.isfile(validator), f"{validator} does not exist"
    assert os.access(validator, os.X_OK), f"{validator} is not executable"

    clean_dir = "/app/corpus/clean/"
    evil_dir = "/app/corpus/evil/"

    clean_files = [f for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [f for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failed = []
    for f in clean_files:
        path = os.path.join(clean_dir, f)
        res = subprocess.run(["bash", validator, path], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(f)

    evil_bypassed = []
    for f in evil_files:
        path = os.path.join(evil_dir, f)
        res = subprocess.run(["bash", validator, path], capture_output=True)
        if res.returncode == 0:
            evil_bypassed.append(f)

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean rejected: {', '.join(clean_failed)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    assert not errors, "Adversarial corpus failed:\n" + "\n".join(errors)

def test_deployment_state():
    deploy_script = "/home/user/deploy.sh"
    assert os.path.isfile(deploy_script), f"{deploy_script} does not exist"
    assert os.access(deploy_script, os.X_OK), f"{deploy_script} is not executable"

    deploy_id = "8675309"
    deploy_dir = f"/home/user/deployments/{deploy_id}"
    symlink = "/home/user/current_telemetry"

    assert os.path.isdir(deploy_dir), f"Deployment directory {deploy_dir} does not exist. Did the deploy script run properly with the decoded ID?"

    assert os.path.islink(symlink), f"{symlink} is not a symlink"
    target = os.readlink(symlink)
    abs_target = os.path.normpath(os.path.join(os.path.dirname(symlink), target))
    assert abs_target == deploy_dir, f"Symlink points to {abs_target}, expected {deploy_dir}"

    incoming_dir = "/app/incoming/"
    expected_files = []

    for f in os.listdir(incoming_dir):
        path = os.path.join(incoming_dir, f)
        if not os.path.isfile(path) or not f.endswith('.json'):
            continue

        try:
            with open(path, 'r') as fp:
                data = json.load(fp)

            if 'device_id' not in data or 'temperature' not in data:
                continue

            device_id = data['device_id']
            if not isinstance(device_id, str) or not re.match(r'^[A-Za-z0-9\-]+$', device_id):
                continue

            temp = data['temperature']
            if not isinstance(temp, (int, float)) or isinstance(temp, bool):
                continue

            if not (-50 <= temp <= 150):
                continue

            expected_files.append(f)
        except Exception:
            continue

    deployed_files = [f for f in os.listdir(deploy_dir) if os.path.isfile(os.path.join(deploy_dir, f))]

    missing = set(expected_files) - set(deployed_files)
    extra = set(deployed_files) - set(expected_files)

    assert not missing, f"Missing valid files in deployment directory: {missing}"
    assert not extra, f"Extra (invalid) files copied to deployment directory: {extra}"