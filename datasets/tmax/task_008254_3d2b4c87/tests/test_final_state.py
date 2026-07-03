# test_final_state.py
import os
import pytest

def test_rejected_paths_log():
    log_file = "/home/user/rejected_paths.log"
    assert os.path.isfile(log_file), f"Expected log file does not exist: {log_file}"

    with open(log_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_rejections = [
        "../../../../home/user/hacked.txt",
        "/etc/passwd_fake"
    ]

    for expected in expected_rejections:
        assert expected in lines, f"Log file is missing rejected path: {expected}"

    assert len(lines) == len(expected_rejections), f"Log file contains unexpected entries. Expected exactly {len(expected_rejections)} rejected paths."

def test_zip_slip_prevented():
    hacked_file = "/home/user/hacked.txt"
    fake_passwd = "/etc/passwd_fake"

    assert not os.path.exists(hacked_file), f"Zip slip vulnerability was not prevented! Malicious file found at: {hacked_file}"
    assert not os.path.exists(fake_passwd), f"Zip slip vulnerability was not prevented! Malicious file found at: {fake_passwd}"

def test_hard_links_and_extraction():
    links_dir = "/home/user/cpp_links"
    extract_dir = "/home/user/safe_extract"

    expected_links = {
        "main.cpp": (os.path.join(extract_dir, "src/main.cpp"), b'int main() { return 0; }'),
        "utils.cpp": (os.path.join(extract_dir, "src/utils.cpp"), b'void test() {}'),
        "legit.cpp": (os.path.join(extract_dir, "src/legit.cpp"), b'int legit() {}')
    }

    for link_name, (original_path, expected_content) in expected_links.items():
        link_path = os.path.join(links_dir, link_name)

        # Check that the extracted file exists
        assert os.path.isfile(original_path), f"Expected extracted file missing: {original_path}"

        # Check that the hard link exists
        assert os.path.isfile(link_path), f"Expected hard link missing: {link_path}"

        # Verify it is actually a hard link (same inode and device)
        stat_original = os.stat(original_path)
        stat_link = os.stat(link_path)
        assert stat_original.st_ino == stat_link.st_ino and stat_original.st_dev == stat_link.st_dev, \
            f"File {link_path} is not a hard link to {original_path}"

        # Verify RLE decompression worked correctly
        with open(link_path, "rb") as f:
            content = f.read()
        assert content == expected_content, f"Content mismatch in {link_path}. RLE decompression may be flawed."

def test_ignored_files_not_extracted():
    # ignore.parc did not have u+x permissions, so it should not have been extracted
    secret_link = "/home/user/cpp_links/secret.cpp"
    secret_original = "/home/user/safe_extract/src/secret.cpp"

    assert not os.path.exists(secret_link), f"File from non-executable archive was incorrectly processed: {secret_link}"
    assert not os.path.exists(secret_original), f"File from non-executable archive was incorrectly extracted: {secret_original}"