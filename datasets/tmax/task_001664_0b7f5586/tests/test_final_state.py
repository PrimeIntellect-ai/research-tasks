# test_final_state.py

import os
import time
import subprocess
import shutil
import pytest

DEPLOY_SCRIPT = "/home/user/deploy.py"
APP_SOURCE = "/home/user/app_source"
RELEASES_DIR = "/home/user/releases"

def create_dummy_file(size_kb):
    os.makedirs(APP_SOURCE, exist_ok=True)
    file_path = os.path.join(APP_SOURCE, "file1.bin")
    with open(file_path, "wb") as f:
        f.write(b"\0" * (size_kb * 1024))

def run_deploy(version):
    result = subprocess.run(
        ["python3", DEPLOY_SCRIPT, version],
        capture_output=True,
        text=True
    )
    assert result.returncode == 0, f"deploy.py failed for {version}:\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

def get_existing_releases():
    if not os.path.exists(RELEASES_DIR):
        return []
    items = os.listdir(RELEASES_DIR)
    return [item for item in items if item != "current" and os.path.isdir(os.path.join(RELEASES_DIR, item))]

def test_deploy_script_exists_and_executable():
    assert os.path.exists(DEPLOY_SCRIPT), f"Script {DEPLOY_SCRIPT} does not exist."
    assert os.access(DEPLOY_SCRIPT, os.X_OK), f"Script {DEPLOY_SCRIPT} is not executable."

def test_deployment_simulation():
    # Clean up releases dir for test
    if os.path.exists(RELEASES_DIR):
        shutil.rmtree(RELEASES_DIR)
    os.makedirs(RELEASES_DIR, exist_ok=True)

    # Step 1: 80KB file, deploy v1
    create_dummy_file(80)
    run_deploy("v1")
    assert "v1" in get_existing_releases(), "v1 was not deployed correctly."

    # Step 2: deploy v2
    time.sleep(1.1)
    run_deploy("v2")
    releases = get_existing_releases()
    assert "v1" in releases and "v2" in releases, "v1 and v2 should exist."

    # Step 3: deploy v3, should delete v1 (80*3 = 240 > 200)
    time.sleep(1.1)
    run_deploy("v3")
    releases = get_existing_releases()
    assert "v1" not in releases, "v1 should have been deleted to enforce quota."
    assert "v2" in releases and "v3" in releases, "v2 and v3 should exist."

    # Step 4: 250KB file, deploy v4
    create_dummy_file(250)
    time.sleep(1.1)
    run_deploy("v4")
    releases = get_existing_releases()
    assert "v2" not in releases, "v2 should have been deleted."
    assert "v3" not in releases, "v3 should have been deleted."
    assert "v4" in releases, "v4 must exist as it is the current release."

    # Check symlink
    current_link = os.path.join(RELEASES_DIR, "current")
    assert os.path.islink(current_link), "'current' must be a symlink."
    target = os.readlink(current_link)
    assert os.path.basename(os.path.normpath(target)) == "v4", "'current' symlink does not point to v4."