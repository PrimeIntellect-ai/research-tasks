# test_final_state.py
import os
import subprocess
import shutil

def test_disk_monitor_script():
    script_path = '/home/user/disk_monitor.py'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable."

    data_dir = '/home/user/data'
    os.makedirs(data_dir, exist_ok=True)

    test_file = os.path.join(data_dir, 'test_file')

    # Test under quota (500MB)
    with open(test_file, 'wb') as f:
        f.truncate(500 * 1024 * 1024)

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 0, f"Expected exit code 0 for under quota, got {result.returncode}"
    assert result.stdout.strip() == "OK", f"Expected output 'OK' for under quota, got '{result.stdout.strip()}'"

    # Test over quota (513MB)
    with open(test_file, 'wb') as f:
        f.truncate(513 * 1024 * 1024)

    result = subprocess.run([script_path], capture_output=True, text=True)
    assert result.returncode == 1, f"Expected exit code 1 for over quota, got {result.returncode}"
    assert result.stdout.strip() == "QUOTA_EXCEEDED", f"Expected output 'QUOTA_EXCEEDED' for over quota, got '{result.stdout.strip()}'"

    # Cleanup
    os.remove(test_file)

def test_systemd_service():
    service_path = '/home/user/.config/systemd/user/disk-monitor.service'
    assert os.path.isfile(service_path), f"Service file {service_path} does not exist."

    with open(service_path, 'r') as f:
        content = f.read()

    assert "ExecStart=/home/user/disk_monitor.py" in content, "Service file missing correct ExecStart directive."
    assert "Restart=on-failure" in content, "Service file missing correct Restart directive."

def test_ssh_filter_corpus():
    script_path = '/home/user/ssh_filter.py'
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."

    clean_dir = '/app/corpus/clean'
    evil_dir = '/app/corpus/evil'

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    clean_failed = []
    evil_failed = []

    for cf in clean_files:
        res = subprocess.run(['python3', script_path, cf], capture_output=True)
        if res.returncode != 0:
            clean_failed.append(os.path.basename(cf))

    for ef in evil_files:
        res = subprocess.run(['python3', script_path, ef], capture_output=True)
        if res.returncode != 1:
            evil_failed.append(os.path.basename(ef))

    error_msgs = []
    if evil_failed:
        error_msgs.append(f"{len(evil_failed)} of {len(evil_files)} evil bypassed: {', '.join(evil_failed)}")
    if clean_failed:
        error_msgs.append(f"{len(clean_failed)} of {len(clean_files)} clean modified/rejected: {', '.join(clean_failed)}")

    assert not error_msgs, " | ".join(error_msgs)