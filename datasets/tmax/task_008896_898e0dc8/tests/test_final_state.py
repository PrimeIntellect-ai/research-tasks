# test_final_state.py

import os
import tarfile

def test_cpp_program_exists():
    """Check if the C++ source and executable exist."""
    cpp_path = "/home/user/filter_archive.cpp"
    exe_path = "/home/user/filter_archive"

    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} does not exist."
    assert os.path.isfile(exe_path), f"Executable {exe_path} does not exist."
    assert os.access(exe_path, os.X_OK), f"File {exe_path} is not executable."

def test_safe_files_txt():
    """Check if safe_files.txt contains the correct safe paths."""
    txt_path = "/home/user/safe_files.txt"
    assert os.path.isfile(txt_path), f"File {txt_path} does not exist."

    with open(txt_path, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_safe_files = {"valid_data1.txt", "valid_data2.csv", "subdir/", "subdir/valid3.txt"}

    # Check that no malicious files are in the list
    for line in lines:
        assert not line.startswith("/"), f"Unsafe absolute path found in safe_files.txt: {line}"
        assert "../" not in line, f"Unsafe traversal path found in safe_files.txt: {line}"
        assert not line.endswith(".."), f"Unsafe traversal path found in safe_files.txt: {line}"

    # Check that expected safe files are present
    for expected in expected_safe_files:
        # tar output might not include trailing slash for directories depending on how it was created, 
        # but we check the files at least.
        if not expected.endswith("/"):
            assert expected in lines, f"Expected safe file {expected} missing from safe_files.txt."

def test_extracted_files():
    """Check if safe files were extracted and renamed correctly, and malicious files were not."""
    extracted_dir = "/home/user/extracted"
    assert os.path.isdir(extracted_dir), f"Directory {extracted_dir} does not exist."

    expected_files = [
        "clean_valid_data1.txt",
        "clean_valid_data2.csv",
        "subdir/clean_valid3.txt"
    ]

    for rel_path in expected_files:
        full_path = os.path.join(extracted_dir, rel_path)
        assert os.path.isfile(full_path), f"Expected extracted and renamed file {full_path} is missing."

    # Ensure malicious files were not extracted
    for root, dirs, files in os.walk(extracted_dir):
        for file in files:
            assert "malicious" not in file, f"Malicious file {file} found in extracted directory."

def test_backup_files():
    """Check if the backup tar and snar files exist and are valid."""
    backup_tar = "/home/user/backup1.tar"
    backup_snar = "/home/user/backup.snar"

    assert os.path.isfile(backup_tar), f"Backup archive {backup_tar} does not exist."
    assert os.path.isfile(backup_snar), f"Snapshot file {backup_snar} does not exist."

    assert tarfile.is_tarfile(backup_tar), f"{backup_tar} is not a valid tar file."

    with tarfile.open(backup_tar, "r") as tar:
        names = tar.getnames()
        # Check if the renamed files are in the backup
        # Paths in tar might be relative or absolute depending on how it was created
        found_clean_valid_data1 = any("clean_valid_data1.txt" in name for name in names)
        assert found_clean_valid_data1, f"clean_valid_data1.txt not found in backup archive {backup_tar}."