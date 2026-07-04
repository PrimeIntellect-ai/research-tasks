# test_final_state.py

import os
import pytest
import stat

def test_redirects_decoded():
    file_path = "/home/user/redirects_decoded.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "http://attacker.site/creds",
        "https://evil-corp.com/steal"
    ]

    assert lines == expected_lines, f"Contents of {file_path} do not match the expected sorted decoded URLs. Got: {lines}"

def test_payload_decrypted():
    file_path = "/home/user/payload_decrypted.txt"
    assert os.path.isfile(file_path), f"File {file_path} is missing."

    with open(file_path, "r") as f:
        content = f.read().strip()

    expected_content = "FLAG{0p3n_r3dir3ct_r3s0lv3d}"
    assert content == expected_content, f"Contents of {file_path} do not match the expected decrypted payload."

def test_fix_perms_script_exists():
    script_path = "/home/user/fix_perms.sh"
    assert os.path.isfile(script_path), f"Script {script_path} is missing."

def test_webroot_permissions():
    webroot = "/home/user/webroot"
    assert os.path.isdir(webroot), f"Directory {webroot} is missing."

    expected_dir_perm = 0o755
    expected_file_perm = 0o644

    for root, dirs, files in os.walk(webroot):
        # Check directory permissions
        root_stat = os.stat(root)
        root_mode = stat.S_IMODE(root_stat.st_mode)
        assert root_mode == expected_dir_perm, f"Directory {root} has incorrect permissions: {oct(root_mode)}. Expected {oct(expected_dir_perm)}."

        # Check file permissions
        for file in files:
            file_path = os.path.join(root, file)
            file_stat = os.stat(file_path)
            file_mode = stat.S_IMODE(file_stat.st_mode)
            assert file_mode == expected_file_perm, f"File {file_path} has incorrect permissions: {oct(file_mode)}. Expected {oct(expected_file_perm)}."

def test_recovered_directory_exists():
    recovered_dir = "/home/user/recovered"
    assert os.path.isdir(recovered_dir), f"Directory {recovered_dir} is missing. Did you extract the zip file?"