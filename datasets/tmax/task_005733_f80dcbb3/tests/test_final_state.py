# test_final_state.py
import os
import json
import subprocess

def test_phase1_backup_profile():
    profile_path = "/home/user/.backup_profile"
    assert os.path.isfile(profile_path), f"File {profile_path} does not exist."

    with open(profile_path, "r") as f:
        content = f.read()

    expected_exports = [
        "export BACKUP_SOURCE=/home/user/data",
        "export BACKUP_DEST=/home/user/backups/data",
        "export BACKUP_RETENTION_DAYS=14"
    ]

    for exp in expected_exports:
        assert exp in content, f"Missing or incorrect export in {profile_path}: expected '{exp}'"

def test_phase2_custom_fstab():
    fstab_path = "/home/user/custom_fstab"
    assert os.path.isfile(fstab_path), f"File {fstab_path} does not exist."

    with open(fstab_path, "r") as f:
        lines = f.readlines()

    found = False
    for line in lines:
        fields = line.strip().split()
        if len(fields) == 6:
            if fields == ['/home/user/data', '/home/user/backups/data', 'none', 'bind', '0', '0']:
                found = True
                break

    assert found, f"Correct fstab entry not found in {fstab_path}. Expected: '/home/user/data /home/user/backups/data none bind 0 0'"

def test_phase3_interactive_automation():
    json_path = "/home/user/backup_configured.json"
    assert os.path.isfile(json_path), f"File {json_path} does not exist. Did auto_provision.py run successfully?"

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"File {json_path} does not contain valid JSON."

    expected_data = {
        "src": "/home/user/data",
        "dst": "/home/user/backups/data",
        "retention": "14"
    }

    assert data == expected_data, f"JSON content in {json_path} does not match expected output. Got {data}"

def test_phase4_scheduled_task():
    try:
        output = subprocess.check_output(["crontab", "-l"], stderr=subprocess.STDOUT, text=True)
    except subprocess.CalledProcessError:
        assert False, "Failed to read crontab. Is it configured?"

    expected_cron = "30 2 * * * /home/user/bin/run_backup.sh"

    found = False
    for line in output.splitlines():
        # normalize whitespace
        if " ".join(line.strip().split()) == expected_cron:
            found = True
            break

    assert found, f"Cron entry '{expected_cron}' not found in crontab."