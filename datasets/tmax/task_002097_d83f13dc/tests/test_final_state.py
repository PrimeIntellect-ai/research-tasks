# test_final_state.py

import os
import json
import zipfile
import pytest

def test_elf_binaries_moved():
    binaries_dir = "/home/user/workspace/binaries"
    extracted_dir = "/home/user/workspace/extracted"

    # Expected binaries
    ls_bin = os.path.join(binaries_dir, "ls_bin")
    pwd_bin = os.path.join(binaries_dir, "pwd_bin")

    assert os.path.exists(ls_bin), "ls_bin was not moved to binaries directory."
    assert os.path.exists(pwd_bin), "pwd_bin was not moved to binaries directory."

    # Check they are ELF by reading magic bytes
    for bin_file in [ls_bin, pwd_bin]:
        with open(bin_file, "rb") as f:
            magic = f.read(4)
            assert magic == b"\x7fELF", f"{bin_file} is not an ELF binary."

    # Check they are removed from extracted
    assert not os.path.exists(os.path.join(extracted_dir, "ls_bin")), "ls_bin was not removed from extracted directory."
    assert not os.path.exists(os.path.join(extracted_dir, "subdir", "pwd_bin")), "pwd_bin was not removed from extracted directory."

def test_csv_encoding_converted():
    csv_file = "/home/user/workspace/extracted/subdir/data.csv"
    assert os.path.exists(csv_file), f"{csv_file} is missing."

    with open(csv_file, "rb") as f:
        content = f.read()

    try:
        decoded = content.decode("utf-8")
    except UnicodeDecodeError:
        pytest.fail("CSV file is not valid UTF-8.")

    # Check that it contains the expected characters (Café, Résumé)
    assert "Café" in decoded, "Expected string 'Café' not found in UTF-8 decoded CSV."
    assert "Résumé" in decoded, "Expected string 'Résumé' not found in UTF-8 decoded CSV."

def test_version_extracted():
    version_file = "/home/user/workspace/version.txt"
    assert os.path.exists(version_file), "version.txt was not created."

    with open(version_file, "r", encoding="utf-8") as f:
        version = f.read().strip()

    assert version == "2.9.4-beta", f"Expected version '2.9.4-beta', got '{version}'."

def test_zip_archive_created():
    zip_path = "/home/user/workspace/cleaned_project.zip"
    assert os.path.exists(zip_path), "cleaned_project.zip was not created."
    assert zipfile.is_zipfile(zip_path), "cleaned_project.zip is not a valid zip archive."

    with zipfile.ZipFile(zip_path, "r") as z:
        namelist = z.namelist()

        # Check expected files are in the zip
        assert "metadata.json" in namelist, "metadata.json missing from zip."
        assert "readme.txt" in namelist, "readme.txt missing from zip."
        assert "subdir/data.csv" in namelist, "subdir/data.csv missing from zip."

        # Check ELF binaries are NOT in the zip
        assert "ls_bin" not in namelist, "ls_bin should not be in the zip."
        assert "subdir/pwd_bin" not in namelist, "pwd_bin should not be in the zip."