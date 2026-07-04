# test_final_state.py
import os
import subprocess
import time
import shutil

def test_scripts_exist_and_executable():
    exp_script = "/home/user/scripts/check_health.exp"
    bash_script = "/home/user/scripts/alert_manager.sh"

    assert os.path.isfile(exp_script), f"Expect script {exp_script} does not exist."
    assert os.access(exp_script, os.X_OK), f"Expect script {exp_script} is not executable."

    assert os.path.isfile(bash_script), f"Bash script {bash_script} does not exist."
    assert os.access(bash_script, os.X_OK), f"Bash script {bash_script} is not executable."

def test_alert_manager_behavior():
    bash_script = "/home/user/scripts/alert_manager.sh"
    state_file = "/home/user/legacy_app/internal_state.dat"
    alerts_dir = "/home/user/alerts"

    # Clean up alerts directory to test behavior from scratch
    if os.path.exists(alerts_dir):
        shutil.rmtree(alerts_dir)

    # Test CRITICAL_ERROR state
    with open(state_file, "w") as f:
        f.write("CRITICAL_ERROR\n")

    # Run alert_manager.sh
    result = subprocess.run([bash_script], capture_output=True, text=True)
    assert result.returncode == 0, f"alert_manager.sh failed with exit code {result.returncode}. Stderr: {result.stderr}"

    active_dir = os.path.join(alerts_dir, "active")
    resolved_dir = os.path.join(alerts_dir, "resolved")
    symlink_path = os.path.join(active_dir, "current_alert.link")

    assert os.path.isdir(active_dir), f"Directory {active_dir} was not created."
    assert os.path.isdir(resolved_dir), f"Directory {resolved_dir} was not created."
    assert os.path.islink(symlink_path), f"Symlink {symlink_path} was not created."

    target_file = os.path.realpath(symlink_path)
    assert os.path.isfile(target_file), f"Symlink target {target_file} does not exist."
    assert target_file.startswith(active_dir), f"Symlink target {target_file} is not in {active_dir}."
    assert "incident_" in os.path.basename(target_file), f"Log file {target_file} does not match naming convention."

    with open(target_file, "r") as f:
        content = f.read().strip()
    assert content == "[STATE] CRITICAL_ERROR", f"Log file does not contain expected state string. Got: {content}"

    # Test Idempotency
    time.sleep(1) # Ensure timestamp would change if a new file was created
    subprocess.run([bash_script], check=True)

    # Check that no new files were created in active_dir (only the link and the one log)
    active_files = os.listdir(active_dir)
    assert len(active_files) == 2, f"Expected exactly 2 files in {active_dir} (link + log), but found {len(active_files)}. Idempotency failed."

    # Test HEALTHY state
    with open(state_file, "w") as f:
        f.write("HEALTHY\n")

    subprocess.run([bash_script], check=True)

    assert not os.path.exists(symlink_path), f"Symlink {symlink_path} was not deleted after recovery."

    resolved_files = os.listdir(resolved_dir)
    assert len(resolved_files) == 1, f"Expected exactly 1 file in {resolved_dir}, but found {len(resolved_files)}."

    resolved_file_path = os.path.join(resolved_dir, resolved_files[0])
    assert resolved_files[0] == os.path.basename(target_file), "Resolved file name does not match the original incident log name."

    with open(resolved_file_path, "r") as f:
        content = f.read().strip()
    assert content == "[STATE] CRITICAL_ERROR", "Resolved file content was modified."