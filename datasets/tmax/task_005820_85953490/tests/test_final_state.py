# test_final_state.py
import os
import subprocess

def get_extracted_service_name():
    manifest_path = "/home/user/workspace/backup_manifest.log"
    assert os.path.exists(manifest_path), f"File {manifest_path} is missing."
    with open(manifest_path, "r") as f:
        for line in f:
            if line.startswith("Requires System Service: "):
                return line.split("Requires System Service: ")[1].strip()
    return None

def test_script_exists():
    script_path = "/home/user/fix_service.py"
    assert os.path.exists(script_path), f"The script {script_path} does not exist."
    assert os.path.isfile(script_path), f"The path {script_path} is not a file."

def test_app_service_modified():
    service_name = get_extracted_service_name()
    assert service_name is not None, "Could not find expected service name in backup_manifest.log"

    app_service_path = "/home/user/workspace/app.service"
    assert os.path.exists(app_service_path), f"File {app_service_path} does not exist."

    with open(app_service_path, "r") as f:
        content = f.read()

    assert f"After={service_name}" in content, f"app.service is missing 'After={service_name}'"
    assert f"Wants={service_name}" in content, f"app.service is missing 'Wants={service_name}'"

def test_restore_status_file():
    service_name = get_extracted_service_name()
    status_path = "/home/user/workspace/restore_status.txt"
    assert os.path.exists(status_path), f"File {status_path} does not exist."

    with open(status_path, "r") as f:
        status = f.read().strip()

    # The student should have run it once, so it could be "SUCCESS: Added ..." or "SUCCESS: Already configured" if they ran it multiple times
    assert status in [f"SUCCESS: Added {service_name}", "SUCCESS: Already configured"], \
        f"restore_status.txt contains incorrect content: {status}"

def test_script_idempotency():
    service_name = get_extracted_service_name()
    script_path = "/home/user/fix_service.py"

    # Run the script a second time
    result = subprocess.run(["python3", script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Script execution failed with error: {result.stderr}"

    # Check the status file after the second run
    status_path = "/home/user/workspace/restore_status.txt"
    with open(status_path, "r") as f:
        status = f.read().strip()

    assert status == "SUCCESS: Already configured", \
        f"Expected 'SUCCESS: Already configured' in {status_path} after second run, got '{status}'"

    # Check for duplicates in app.service
    app_service_path = "/home/user/workspace/app.service"
    with open(app_service_path, "r") as f:
        content = f.read()

    after_count = content.count(f"After={service_name}")
    wants_count = content.count(f"Wants={service_name}")

    assert after_count == 1, f"Found {after_count} 'After={service_name}' lines in app.service, expected exactly 1."
    assert wants_count == 1, f"Found {wants_count} 'Wants={service_name}' lines in app.service, expected exactly 1."