# test_final_state.py
import os
import tarfile
import pytest

def test_bad_links_logged_and_removed():
    log_file = "/home/user/bad_links.txt"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist."

    with open(log_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_bad_links = [
        "/home/user/project_root/dirA/link_to_B",
        "/home/user/project_root/dirB/link_to_A",
        "/home/user/project_root/docs/broken_link"
    ]

    assert lines == sorted(expected_bad_links), f"Contents of {log_file} are incorrect or not sorted properly."

    for link in expected_bad_links:
        assert not os.path.exists(link) and not os.path.islink(link), f"Problematic symlink {link} was not deleted."

def test_configs_redacted():
    conf_files = [
        "/home/user/project_root/configs/db.conf",
        "/home/user/project_root/configs/api.conf"
    ]

    for conf in conf_files:
        assert os.path.isfile(conf), f"Config file {conf} is missing."
        with open(conf, "r") as f:
            lines = f.readlines()

        password_found = False
        for line in lines:
            if line.startswith("PASSWORD="):
                assert line.strip() == "PASSWORD=REDACTED", f"Password not redacted correctly in {conf}."
                password_found = True

        assert password_found, f"No PASSWORD= line found in {conf}."

def test_skipped_symlinks_logged():
    log_file = "/home/user/skipped_symlinks.log"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist."

    with open(log_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_skipped = [
        "/home/user/project_root/dirA/readme_link"
    ]

    assert lines == sorted(expected_skipped), f"Contents of {log_file} are incorrect."

def test_safe_archive_created_and_contents():
    archive_file = "/home/user/safe_archive.tar.gz"
    assert os.path.isfile(archive_file), f"Archive {archive_file} does not exist."

    expected_files = {
        "dirA/fileA.txt",
        "dirB/fileB.txt",
        "configs/db.conf",
        "configs/api.conf",
        "docs/readme.txt"
    }

    found_files = set()
    with tarfile.open(archive_file, "r:gz") as tar:
        for member in tar.getmembers():
            if member.isfile():
                # Allow paths to be prefixed with project_root/ or just relative
                name = member.name
                if name.startswith("project_root/"):
                    name = name[len("project_root/"):]
                elif name.startswith("/home/user/project_root/"):
                    name = name[len("/home/user/project_root/"):]
                elif name.startswith("./"):
                    name = name[2:]
                found_files.add(name)

    for f in expected_files:
        assert f in found_files, f"Expected file {f} is missing from the tar archive."

    # Ensure no bad links are in the tar
    bad_names = {"dirA/link_to_B", "dirB/link_to_A", "docs/broken_link"}
    for b in bad_names:
        assert b not in found_files, f"Problematic link {b} was included in the archive."

def test_backup_script_fixed():
    script = "/home/user/backup_script.py"
    assert os.path.isfile(script), f"Backup script {script} is missing."

    with open(script, "r") as f:
        content = f.read()

    assert "followlinks=True" not in content, "Backup script still contains 'followlinks=True'."