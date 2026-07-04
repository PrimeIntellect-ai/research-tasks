# test_final_state.py
import os
import hashlib
import csv
import stat
import pytest

def get_sha256(filepath):
    if not os.path.exists(filepath):
        return None
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

@pytest.fixture(scope="module")
def expected_shas():
    zip_path = "/home/user/storage_dump/folder1/hidden_zip.txt"
    tar_path = "/home/user/storage_dump/folder2/backup.dat"
    return {
        "zip": get_sha256(zip_path),
        "tar": get_sha256(tar_path)
    }

def test_inventory_report_exists_and_format(expected_shas):
    report_path = "/home/user/inventory_report.csv"
    assert os.path.exists(report_path), f"Report file {report_path} is missing."

    with open(report_path, "r", newline="") as f:
        reader = list(csv.reader(f))

    assert len(reader) > 0, "Inventory report is empty."

    header = reader[0]
    assert header == ["Original_File_Name", "Mime_Type", "Status", "SHA256"], \
        f"Incorrect CSV header. Got: {header}"

    rows = reader[1:]
    # Should be sorted by Original_File_Name
    names = [row[0] for row in rows]
    assert names == sorted(names), "CSV rows are not sorted alphabetically by Original_File_Name."

    # Check specific files
    file_records = {row[0]: row for row in rows}

    expected_files = ["backup.dat", "backup_copy.dat", "bad.zip", "hidden_zip.txt", "readme.md"]
    for ef in expected_files:
        assert ef in file_records, f"File {ef} missing from inventory report."

    # backup.dat
    assert file_records["backup.dat"][2] == "Valid", "backup.dat should be Valid"
    assert file_records["backup.dat"][3] == expected_shas["tar"], "backup.dat SHA mismatch"
    assert "tar" in file_records["backup.dat"][1], "backup.dat MIME type should contain 'tar'"

    # backup_copy.dat
    assert file_records["backup_copy.dat"][2] == "Valid", "backup_copy.dat should be Valid"
    assert file_records["backup_copy.dat"][3] == expected_shas["tar"], "backup_copy.dat SHA mismatch"

    # bad.zip
    assert file_records["bad.zip"][2] == "Corrupt", "bad.zip should be Corrupt"
    assert file_records["bad.zip"][3] == "N/A", "bad.zip SHA should be N/A"
    assert "zip" in file_records["bad.zip"][1], "bad.zip MIME type should contain 'zip'"

    # hidden_zip.txt
    assert file_records["hidden_zip.txt"][2] == "Valid", "hidden_zip.txt should be Valid"
    assert file_records["hidden_zip.txt"][3] == expected_shas["zip"], "hidden_zip.txt SHA mismatch"
    assert "zip" in file_records["hidden_zip.txt"][1], "hidden_zip.txt MIME type should contain 'zip'"

    # readme.md
    assert file_records["readme.md"][2] == "NotArchive", "readme.md should be NotArchive"
    assert file_records["readme.md"][3] == "N/A", "readme.md SHA should be N/A"

def test_clean_archives_hard_links(expected_shas):
    clean_dir = "/home/user/clean_archives"
    assert os.path.isdir(clean_dir), f"Directory {clean_dir} is missing."

    files = os.listdir(clean_dir)
    assert len(files) == 2, f"Expected exactly 2 files in {clean_dir}, got {len(files)}: {files}"

    expected_zip_name = f"{expected_shas['zip']}.zip"
    expected_tar_name = f"{expected_shas['tar']}.tar"

    assert expected_zip_name in files, f"Missing {expected_zip_name} in {clean_dir}"
    assert expected_tar_name in files, f"Missing {expected_tar_name} in {clean_dir}"

    # Check if they are hard links to the original files (same inode)
    orig_zip_stat = os.stat("/home/user/storage_dump/folder1/hidden_zip.txt")
    clean_zip_stat = os.stat(os.path.join(clean_dir, expected_zip_name))
    assert orig_zip_stat.st_ino == clean_zip_stat.st_ino, "Zip file in clean_archives is not a hard link to the original."

    orig_tar_stat = os.stat("/home/user/storage_dump/folder2/backup.dat")
    clean_tar_stat = os.stat(os.path.join(clean_dir, expected_tar_name))
    assert orig_tar_stat.st_ino == clean_tar_stat.st_ino, "Tar file in clean_archives is not a hard link to the original."

def test_archive_index_symlinks(expected_shas):
    index_dir = "/home/user/archive_index"
    assert os.path.isdir(index_dir), f"Directory {index_dir} is missing."

    expected_zip_name = f"{expected_shas['zip']}.zip"
    expected_tar_name = f"{expected_shas['tar']}.tar"

    zip_link = os.path.join(index_dir, "zip", "hidden_zip.txt")
    assert os.path.islink(zip_link), f"{zip_link} is missing or not a symlink."
    assert os.readlink(zip_link) == os.path.join("/home/user/clean_archives", expected_zip_name), \
        f"Symlink {zip_link} points to the wrong target."

    tar_link1 = os.path.join(index_dir, "tar", "backup.dat")
    assert os.path.islink(tar_link1), f"{tar_link1} is missing or not a symlink."
    assert os.readlink(tar_link1) == os.path.join("/home/user/clean_archives", expected_tar_name), \
        f"Symlink {tar_link1} points to the wrong target."

    tar_link2 = os.path.join(index_dir, "tar", "backup_copy.dat")
    assert os.path.islink(tar_link2), f"{tar_link2} is missing or not a symlink."
    assert os.readlink(tar_link2) == os.path.join("/home/user/clean_archives", expected_tar_name), \
        f"Symlink {tar_link2} points to the wrong target."