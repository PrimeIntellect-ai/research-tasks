# test_final_state.py

import os
import json
import subprocess
import time
import pytest

def test_pipeline_execution_and_directories():
    pipeline_script = "/home/user/pipeline.sh"
    assert os.path.isfile(pipeline_script), f"{pipeline_script} does not exist."
    assert os.access(pipeline_script, os.X_OK), f"{pipeline_script} is not executable."

    # Run the pipeline script
    result = subprocess.run([pipeline_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed with exit code {result.returncode}.\nSTDOUT: {result.stdout}\nSTDERR: {result.stderr}"

    # Verify directories
    for d in ["/home/user/deployments", "/home/user/state", "/home/user/backups"]:
        assert os.path.isdir(d), f"Directory {d} was not created."

def test_backup_creation():
    backup_tarball = "/home/user/backups/state_backup.tar.gz"
    assert os.path.isfile(backup_tarball), f"Backup tarball {backup_tarball} does not exist."

    # Verify it's a valid tarball
    result = subprocess.run(["tar", "-tzf", backup_tarball], capture_output=True)
    assert result.returncode == 0, f"Backup file {backup_tarball} is not a valid compressed tarball."

def test_deployment_scripts():
    manifests_dir = "/home/user/manifests"
    deployments_dir = "/home/user/deployments"

    for filename in os.listdir(manifests_dir):
        if not filename.endswith(".json"):
            continue

        with open(os.path.join(manifests_dir, filename), 'r') as f:
            manifest = json.load(f)

        vm_name = manifest["metadata"]["name"]
        memory = manifest["spec"]["memory"]
        qemu_image = manifest["spec"]["qemu_image"]
        vnc_port = manifest["spec"]["vnc_port"]

        script_path = os.path.join(deployments_dir, f"launch_{vm_name}.sh")
        assert os.path.isfile(script_path), f"Deployment script {script_path} does not exist."
        assert os.access(script_path, os.X_OK), f"Deployment script {script_path} is not executable."

        with open(script_path, 'r') as f:
            lines = f.read().strip().split('\n')

        assert len(lines) >= 2, f"Script {script_path} does not have exactly two lines."
        assert lines[0] == "#!/bin/bash", f"Script {script_path} does not start with #!/bin/bash."
        expected_cmd = f"qemu-system-x86_64 -m {memory} -hda {qemu_image} -vnc 127.0.0.1:{vnc_port} -daemonize"
        assert lines[1] == expected_cmd, f"Script {script_path} command line does not match expected."

def test_state_files():
    manifests_dir = "/home/user/manifests"
    state_dir = "/home/user/state"

    for filename in os.listdir(manifests_dir):
        if not filename.endswith(".json"):
            continue

        with open(os.path.join(manifests_dir, filename), 'r') as f:
            manifest = json.load(f)

        vm_name = manifest["metadata"]["name"]
        vnc_port = manifest["spec"]["vnc_port"]

        state_path = os.path.join(state_dir, f"{vm_name}.json")
        assert os.path.isfile(state_path), f"State file {state_path} does not exist."

        with open(state_path, 'r') as f:
            try:
                state_data = json.load(f)
            except json.JSONDecodeError:
                pytest.fail(f"State file {state_path} is not valid JSON.")

        assert state_data.get("status") == "deployed", f"State file {state_path} status is incorrect."
        assert state_data.get("name") == vm_name, f"State file {state_path} name is incorrect."
        assert state_data.get("port") == vnc_port, f"State file {state_path} port is incorrect."

def test_pipeline_log():
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"Pipeline log {log_path} does not exist."

    with open(log_path, 'r') as f:
        content = f.read()

    assert "PIPELINE SUCCESS" in content, f"Pipeline log {log_path} does not contain 'PIPELINE SUCCESS'."

def test_idempotency():
    pipeline_script = "/home/user/pipeline.sh"
    web_manifest = "/home/user/manifests/web.json"
    web_state = "/home/user/state/web-server.json"
    db_state = "/home/user/state/db-server.json"

    assert os.path.isfile(web_manifest), f"Manifest {web_manifest} missing."
    assert os.path.isfile(web_state), f"State file {web_state} missing."
    assert os.path.isfile(db_state), f"State file {db_state} missing."

    # Sleep to ensure mtime differences
    time.sleep(2)

    # Record mtime of db state
    db_state_mtime_before = os.path.getmtime(db_state)

    # Modify web manifest to trigger update
    os.utime(web_manifest, None)

    # Run pipeline again
    result = subprocess.run([pipeline_script], capture_output=True, text=True)
    assert result.returncode == 0, f"Pipeline script failed during idempotency test."

    # Check if web state was updated
    web_state_mtime = os.path.getmtime(web_state)
    web_manifest_mtime = os.path.getmtime(web_manifest)
    assert web_state_mtime >= web_manifest_mtime, "Web state file was not updated after manifest modification."

    # Check if db state was NOT updated
    db_state_mtime_after = os.path.getmtime(db_state)
    assert db_state_mtime_before == db_state_mtime_after, "DB state file was updated even though its manifest was not modified (idempotency failed)."