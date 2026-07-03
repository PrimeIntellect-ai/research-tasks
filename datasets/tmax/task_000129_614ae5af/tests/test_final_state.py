# test_final_state.py
import os
import subprocess
import pytest

def test_sanitizer_exists_and_executable():
    sanitizer_path = "/home/user/sanitizer"
    assert os.path.isfile(sanitizer_path), f"Sanitizer executable missing at {sanitizer_path}"
    assert os.access(sanitizer_path, os.X_OK), f"Sanitizer at {sanitizer_path} is not executable"

def test_sanitizer_clean_corpus():
    sanitizer_path = "/home/user/sanitizer"
    clean_dir = "/app/corpus/clean"
    assert os.path.isdir(clean_dir), f"Clean corpus directory missing at {clean_dir}"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    assert clean_files, "No files found in clean corpus"

    failed_files = []
    for fpath in clean_files:
        result = subprocess.run([sanitizer_path, fpath], capture_output=True)
        if result.returncode != 0:
            failed_files.append(os.path.basename(fpath))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files rejected (expected exit code 0). Offending files: {', '.join(failed_files)}"

def test_sanitizer_evil_corpus():
    sanitizer_path = "/home/user/sanitizer"
    evil_dir = "/app/corpus/evil"
    assert os.path.isdir(evil_dir), f"Evil corpus directory missing at {evil_dir}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    assert evil_files, "No files found in evil corpus"

    failed_files = []
    for fpath in evil_files:
        result = subprocess.run([sanitizer_path, fpath], capture_output=True)
        if result.returncode != 1:
            failed_files.append(os.path.basename(fpath))

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil files bypassed (expected exit code 1). Offending files: {', '.join(failed_files)}"

def test_vm_supervisor_script():
    script_path = "/home/user/vm_supervisor.sh"
    assert os.path.isfile(script_path), f"VM supervisor script missing at {script_path}"
    assert os.access(script_path, os.X_OK), f"Script at {script_path} is not executable"

def test_systemd_service_and_timer():
    service_path = os.path.expanduser("~user/.config/systemd/user/vm-restore.service")
    timer_path = os.path.expanduser("~user/.config/systemd/user/vm-restore.timer")

    assert os.path.isfile(service_path), f"Service file missing at {service_path}"

    with open(service_path, "r") as f:
        content = f.read()
    assert "ExecStart=/home/user/vm_supervisor.sh" in content, "Service file does not contain ExecStart=/home/user/vm_supervisor.sh"

    # Check if timer is active
    try:
        # Try running as user
        result = subprocess.run(["su", "-", "user", "-c", "XDG_RUNTIME_DIR=/run/user/$(id -u user) systemctl --user is-active vm-restore.timer"], capture_output=True, text=True)
        is_active = result.stdout.strip() == "active"
        if not is_active:
            # Fallback for some environments
            result2 = subprocess.run(["systemctl", "--user", "is-active", "vm-restore.timer"], capture_output=True, text=True)
            is_active = result2.stdout.strip() == "active"
        assert is_active, "vm-restore.timer is not active"
    except Exception as e:
        pytest.fail(f"Failed to check if timer is active: {e}")