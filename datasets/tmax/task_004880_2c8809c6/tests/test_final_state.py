# test_final_state.py
import os
import subprocess
import pytest

def test_symlink_target():
    link_path = "/home/user/target_list"
    expected_target = "/home/user/mail/oncall-network-team"

    assert os.path.islink(link_path), f"Expected a symbolic link at {link_path}"
    actual_target = os.readlink(link_path)
    assert actual_target == expected_target, f"Symlink {link_path} points to {actual_target}, expected {expected_target}"

def test_alert_filter_script_exists_and_executable():
    script_path = "/home/user/alert_filter.py"
    assert os.path.exists(script_path), f"Script missing at {script_path}"
    assert os.path.isfile(script_path), f"{script_path} is not a file"
    assert os.access(script_path, os.X_OK), f"Script {script_path} is not executable"

def test_alert_filter_classification():
    script_path = "/home/user/alert_filter.py"
    evil_dir = "/app/corpus/evil/"
    clean_dir = "/app/corpus/clean/"

    assert os.path.exists(script_path), f"Script missing at {script_path}"

    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]
    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]

    evil_bypassed = []
    clean_rejected = []

    for filepath in evil_files:
        result = subprocess.run(["python3", script_path, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "REJECT":
            evil_bypassed.append((os.path.basename(filepath), output))

    for filepath in clean_files:
        result = subprocess.run(["python3", script_path, filepath], capture_output=True, text=True)
        output = result.stdout.strip()
        if output != "ACCEPT":
            clean_rejected.append((os.path.basename(filepath), output))

    error_messages = []
    if evil_bypassed:
        error_messages.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed. Offending files: " + ", ".join([f[0] for f in evil_bypassed[:5]]) + ("..." if len(evil_bypassed) > 5 else ""))
    if clean_rejected:
        error_messages.append(f"{len(clean_rejected)} of {len(clean_files)} clean rejected. Offending files: " + ", ".join([f[0] for f in clean_rejected[:5]]) + ("..." if len(clean_rejected) > 5 else ""))

    assert not evil_bypassed and not clean_rejected, " | ".join(error_messages)