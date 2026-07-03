# test_final_state.py

import os
import stat
import subprocess
import pytest

def test_c_program_exists_and_executable():
    c_file = "/home/user/sensor_processor.c"
    exe_file = "/home/user/sensor_processor"

    assert os.path.isfile(c_file), f"C source file {c_file} is missing."
    assert os.path.isfile(exe_file), f"Executable {exe_file} is missing."
    assert os.access(exe_file, os.X_OK), f"Executable {exe_file} is not executable."

def test_sensor_processor_output():
    exe_file = "/home/user/sensor_processor"

    result = subprocess.run([exe_file], capture_output=True, text=True)
    assert result.returncode == 0, f"{exe_file} failed to execute."

    output = result.stdout.strip().split('\n')

    # We expect sensor_a.dat and sensor_b.dat in alphabetical order
    expected_lines = [
        "File: sensor_a.dat | Size: 17 | Permissions: 644",
        "File: sensor_b.dat | Size: 11 | Permissions: 600"
    ]

    for expected in expected_lines:
        assert expected in output, f"Expected line '{expected}' not found in output."

    # Check sorting
    assert output[0].startswith("File: sensor_a.dat"), "Output is not sorted alphabetically."
    assert output[1].startswith("File: sensor_b.dat"), "Output is not sorted alphabetically."

def test_git_repo_initialized():
    git_dir = "/home/user/iot_sync_repo/.git"
    assert os.path.isdir(git_dir), "Git repository not initialized in /home/user/iot_sync_repo."

def test_pre_commit_hook():
    hook_file = "/home/user/iot_sync_repo/.git/hooks/pre-commit"
    assert os.path.isfile(hook_file), f"Pre-commit hook {hook_file} does not exist."
    assert os.access(hook_file, os.X_OK), f"Pre-commit hook {hook_file} is not executable."

def test_sync_telemetry_script():
    script_file = "/home/user/sync_telemetry.sh"
    assert os.path.isfile(script_file), f"Script {script_file} does not exist."
    assert os.access(script_file, os.X_OK), f"Script {script_file} is not executable."

def test_crontab_configured():
    result = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to read crontab."

    crontab_content = result.stdout.strip()
    assert "/home/user/sync_telemetry.sh" in crontab_content, "Crontab does not contain the sync script."
    assert "*/5 * * * *" in crontab_content or "0,5,10,15,20,25,30,35,40,45,50,55 * * * *" in crontab_content, "Crontab is not scheduled for every 5 minutes."

def test_telemetry_report_permissions():
    report_file = "/home/user/iot_sync_repo/telemetry_report.txt"
    assert os.path.isfile(report_file), f"Report file {report_file} does not exist."

    st = os.stat(report_file)
    permissions = stat.S_IMODE(st.st_mode)
    assert permissions == 0o400, f"Permissions for {report_file} should be 400, got {oct(permissions)}."

def test_git_commit_message():
    repo_dir = "/home/user/iot_sync_repo"
    result = subprocess.run(["git", "-C", repo_dir, "log", "-1", "--pretty=%B"], capture_output=True, text=True)
    assert result.returncode == 0, "Failed to get git log. Is there a commit?"

    commit_message = result.stdout.strip()
    expected_string = "[IoT-Sync] Locale: en_US.UTF-8, Timezone: UTC"
    assert expected_string in commit_message, f"Commit message does not contain the required string. Got: {commit_message}"