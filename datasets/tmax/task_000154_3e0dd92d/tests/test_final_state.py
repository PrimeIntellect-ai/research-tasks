# test_final_state.py
import os
import subprocess
import pwd
import stat
import pytest

def test_stage1_outage_seconds():
    outage_file = "/home/user/outage_seconds.txt"
    assert os.path.exists(outage_file), f"File {outage_file} does not exist. Stage 1 incomplete."

    with open(outage_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = ["12", "13", "14", "15", "42", "43", "44", "45", "46", "47"]
    assert lines == expected_lines, f"Expected timestamps {expected_lines}, but got {lines}. Video analysis incorrect."

def test_stage2_socket_permissions():
    sock_path = "/run/api-backend/api.sock"
    assert os.path.exists(sock_path), f"Socket {sock_path} does not exist. Backend service may not be running."

    st = os.stat(sock_path)

    try:
        www_data_uid = pwd.getpwnam("www-data").pw_uid
        www_data_gid = pwd.getpwnam("www-data").pw_gid
    except KeyError:
        pytest.fail("User www-data does not exist on the system.")

    can_read = False
    can_write = False

    if st.st_uid == www_data_uid:
        can_read = bool(st.st_mode & stat.S_IRUSR)
        can_write = bool(st.st_mode & stat.S_IWUSR)
    elif st.st_gid == www_data_gid:
        can_read = bool(st.st_mode & stat.S_IRGRP)
        can_write = bool(st.st_mode & stat.S_IWGRP)
    else:
        can_read = bool(st.st_mode & stat.S_IROTH)
        can_write = bool(st.st_mode & stat.S_IWOTH)

    assert can_read and can_write, f"www-data does not have rw permissions on {sock_path}. Nginx will still return 502."

def test_stage3_sanitizer_adversarial_corpus():
    sanitizer_path = "/home/user/sanitizer"
    assert os.path.exists(sanitizer_path), f"Sanitizer binary {sanitizer_path} does not exist."
    assert os.access(sanitizer_path, os.X_OK), f"Sanitizer {sanitizer_path} is not executable."

    evil_dir = "/app/corpora/evil/"
    clean_dir = "/app/corpora/clean/"

    assert os.path.isdir(evil_dir), f"Evil corpus missing at {evil_dir}"
    assert os.path.isdir(clean_dir), f"Clean corpus missing at {clean_dir}"

    evil_files = os.listdir(evil_dir)
    clean_files = os.listdir(clean_dir)

    evil_bypassed = []
    clean_modified = []

    for filename in evil_files:
        filepath = os.path.join(evil_dir, filename)
        with open(filepath, "rb") as f:
            result = subprocess.run([sanitizer_path], stdin=f)
            if result.returncode != 1:
                evil_bypassed.append(filename)

    for filename in clean_files:
        filepath = os.path.join(clean_dir, filename)
        with open(filepath, "rb") as f:
            result = subprocess.run([sanitizer_path], stdin=f)
            if result.returncode != 0:
                clean_modified.append(filename)

    error_msg = []
    if evil_bypassed:
        error_msg.append(f"{len(evil_bypassed)} of {len(evil_files)} evil bypassed: {', '.join(evil_bypassed)}")
    if clean_modified:
        error_msg.append(f"{len(clean_modified)} of {len(clean_files)} clean modified: {', '.join(clean_modified)}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))