# test_final_state.py
import os
import subprocess
import glob
import stat

def test_sanitizer_evil_corpus():
    sanitizer_path = "/home/user/sanitizer"
    assert os.path.exists(sanitizer_path), "Sanitizer binary not found at /home/user/sanitizer"
    assert os.access(sanitizer_path, os.X_OK), "Sanitizer is not executable"

    evil_files = glob.glob("/app/corpus/evil/*")
    assert len(evil_files) > 0, "No evil corpus files found"

    bypassed_files = []
    for filepath in evil_files:
        with open(filepath, 'r') as f:
            input_data = f.read()

        result = subprocess.run([sanitizer_path], input=input_data, text=True, capture_output=True)

        # Evil files should produce NO output (all lines rejected)
        if result.stdout.strip() != "":
            bypassed_files.append(os.path.basename(filepath))

    if bypassed_files:
        assert False, f"{len(bypassed_files)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_files)}"

def test_sanitizer_clean_corpus():
    sanitizer_path = "/home/user/sanitizer"
    assert os.path.exists(sanitizer_path), "Sanitizer binary not found at /home/user/sanitizer"
    assert os.access(sanitizer_path, os.X_OK), "Sanitizer is not executable"

    clean_files = glob.glob("/app/corpus/clean/*")
    assert len(clean_files) > 0, "No clean corpus files found"

    modified_files = []
    for filepath in clean_files:
        with open(filepath, 'r') as f:
            input_data = f.read()

        result = subprocess.run([sanitizer_path], input=input_data, text=True, capture_output=True)

        # Clean files should be preserved exactly
        if result.stdout != input_data:
            modified_files.append(os.path.basename(filepath))

    if modified_files:
        assert False, f"{len(modified_files)} of {len(clean_files)} clean modified: {', '.join(modified_files)}"

def test_permissions_and_security():
    alerts_dir = "/home/user/alerts"
    assert os.path.exists(alerts_dir), f"Directory {alerts_dir} does not exist"
    assert os.path.isdir(alerts_dir), f"{alerts_dir} is not a directory"

    dir_stat = os.stat(alerts_dir)
    assert stat.S_IMODE(dir_stat.st_mode) == 0o700, f"Permissions for {alerts_dir} are not 0700"

    log_file = "/home/user/alerts/sanitized_ssh.log"
    if os.path.exists(log_file):
        file_stat = os.stat(log_file)
        assert stat.S_IMODE(file_stat.st_mode) == 0o600, f"Permissions for {log_file} are not 0600"

def test_logrotate_conf():
    conf_path = "/home/user/logrotate.conf"
    assert os.path.exists(conf_path), f"Logrotate conf not found at {conf_path}"

    with open(conf_path, 'r') as f:
        content = f.read()

    assert "daily" in content, "Logrotate conf missing 'daily'"
    assert "rotate 7" in content, "Logrotate conf missing 'rotate 7'"
    assert "compress" in content, "Logrotate conf missing 'compress'"
    assert "0600" in content or "600" in content, "Logrotate conf missing '0600' permission recreation"