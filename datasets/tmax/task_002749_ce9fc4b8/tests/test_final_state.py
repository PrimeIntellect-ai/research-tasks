# test_final_state.py

import os
import subprocess
import glob
import json
import urllib.request
import ssl
import time

def test_finops_filter_adversarial_corpus():
    script_path = "/home/user/finops_filter.py"
    assert os.path.isfile(script_path), f"{script_path} does not exist"

    clean_dir = "/opt/verifier/clean"
    evil_dir = "/opt/verifier/evil"

    clean_files = glob.glob(os.path.join(clean_dir, "*.json"))
    evil_files = glob.glob(os.path.join(evil_dir, "*.json"))

    assert len(clean_files) > 0, "No clean corpus files found."
    assert len(evil_files) > 0, "No evil corpus files found."

    clean_failed = []
    for cf in clean_files:
        result = subprocess.run(["python3", script_path, cf], capture_output=True)
        if result.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    evil_bypassed = []
    for ef in evil_files:
        result = subprocess.run(["python3", script_path, ef], capture_output=True)
        if result.returncode == 0:
            evil_bypassed.append(os.path.basename(ef))

    errors = []
    if clean_failed:
        errors.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")
    if evil_bypassed:
        errors.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")

    assert not errors, " | ".join(errors)

def test_nginx_running_tls():
    # Check if nginx is listening on 8443
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    try:
        req = urllib.request.Request("https://localhost:8443/")
        with urllib.request.urlopen(req, context=ctx, timeout=2) as response:
            assert response.status in [200, 403, 404], f"Unexpected status code: {response.status}"
    except urllib.error.URLError as e:
        pytest.fail(f"Failed to connect to nginx on port 8443 with TLS: {e}")

def test_deploy_script():
    deploy_script = "/home/user/deploy.sh"
    assert os.path.isfile(deploy_script), f"{deploy_script} does not exist"
    assert os.access(deploy_script, os.X_OK), f"{deploy_script} is not executable"

    # Create a valid test config
    test_app_name = "test-api-service"
    valid_config = {
        "app_name": test_app_name,
        "instances": [
            {"type": "t4g.micro", "count": 1, "monthly_cost_per_unit": 10}
        ]
    }
    test_conf_path = "/tmp/test_valid_config.json"
    with open(test_conf_path, "w") as f:
        json.dump(valid_config, f)

    # Run deploy script
    result = subprocess.run(["bash", deploy_script, test_conf_path], capture_output=True)
    assert result.returncode == 0, f"Deploy script failed on valid config: {result.stderr.decode()}"

    # Check that symlink exists and points to a directory
    symlink_path = f"/home/user/www/{test_app_name}-live"
    assert os.path.islink(symlink_path), f"Symlink {symlink_path} was not created"

    target_dir = os.readlink(symlink_path)
    if not os.path.isabs(target_dir):
        target_dir = os.path.join("/home/user/www", target_dir)

    assert os.path.isdir(target_dir), f"Symlink target {target_dir} is not a directory"

    copied_config = os.path.join(target_dir, "config.json")
    assert os.path.isfile(copied_config), f"config.json not found in {target_dir}"

    # Create an invalid test config
    invalid_config = {
        "app_name": "test-evil-service",
        "instances": [
            {"type": "t4g.micro", "count": 1000, "monthly_cost_per_unit": 10}
        ]
    }
    test_evil_path = "/tmp/test_evil_config.json"
    with open(test_evil_path, "w") as f:
        json.dump(invalid_config, f)

    result_evil = subprocess.run(["bash", deploy_script, test_evil_path], capture_output=True)
    assert result_evil.returncode != 0, "Deploy script should fail on invalid config"

    evil_symlink = f"/home/user/www/test-evil-service-live"
    assert not os.path.exists(evil_symlink), f"Symlink {evil_symlink} should not exist for rejected config"