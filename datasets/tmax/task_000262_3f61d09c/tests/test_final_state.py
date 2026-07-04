# test_final_state.py

import os
import re
import subprocess

def test_service_dependency():
    path = "/home/user/app/account-monitor.service"
    assert os.path.exists(path), f"{path} does not exist."

    with open(path, "r") as f:
        content = f.read()

    # Extract the [Unit] section specifically to ensure the directive was added there
    unit_section_match = re.search(r'\[Unit\](.*?)(?:\[|$)', content, re.DOTALL)
    assert unit_section_match, "[Unit] section missing in service file."

    unit_section_content = unit_section_match.group(1)

    # Check for the After=storage-init.service line
    assert re.search(r'^After\s*=\s*storage-init\.service\s*$', unit_section_content, re.MULTILINE), \
        "The directive 'After=storage-init.service' was not found in the [Unit] section."

def test_auto_provision_expect():
    path = "/home/user/app/auto_provision.exp"
    assert os.path.exists(path), f"{path} does not exist."
    assert os.access(path, os.X_OK), f"{path} is not executable."

    # Run the expect script and verify it correctly automates the bash script
    result = subprocess.run([path], capture_output=True, text=True)
    assert result.returncode == 0, f"auto_provision.exp failed with return code {result.returncode}. Output: {result.stderr}"
    assert "Initialization complete." in result.stdout, \
        "auto_provision.exp did not output the expected success message. Check if PIN and Action were provided correctly."

def test_check_quota_script():
    path = "/home/user/app/check_quota.sh"
    assert os.path.exists(path), f"{path} does not exist."
    assert os.access(path, os.X_OK), f"{path} is not executable."

    users_dir = "/home/user/app/users/"
    os.makedirs(users_dir, exist_ok=True)
    log_file = "/home/user/app/quota.log"

    # Clear users dir for testing
    for f in os.listdir(users_dir):
        file_path = os.path.join(users_dir, f)
        if os.path.isfile(file_path):
            os.remove(file_path)

    # Test under quota
    small_file = os.path.join(users_dir, "smallfile")
    with open(small_file, "wb") as f:
        f.write(b"0" * 1024)  # 1 KB

    subprocess.run([path], check=True)
    assert os.path.exists(log_file), f"{log_file} was not created."
    with open(log_file, "r") as f:
        lines = f.readlines()
    assert len(lines) > 0, f"{log_file} is empty."
    assert lines[-1].strip() == "OK", f"Expected 'OK' in log for size <= 10000 bytes, got: {lines[-1].strip()}"

    # Test over quota
    large_file = os.path.join(users_dir, "largefile")
    with open(large_file, "wb") as f:
        f.write(b"0" * 15000)  # Total size > 10000 bytes

    subprocess.run([path], check=True)
    with open(log_file, "r") as f:
        lines = f.readlines()
    assert lines[-1].strip() == "QUOTA_EXCEEDED", f"Expected 'QUOTA_EXCEEDED' in log for size > 10000 bytes, got: {lines[-1].strip()}"

def test_crontab():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab. Has it been initialized?"

    found = False
    for line in result.stdout.splitlines():
        # Check for the exact schedule and script path
        if re.match(r'^\s*\*/5\s+\*\s+\*\s+\*\s+\*\s+/home/user/app/check_quota\.sh\s*$', line):
            found = True
            break

    assert found, "Crontab entry for check_quota.sh with schedule '*/5 * * * *' was not found."