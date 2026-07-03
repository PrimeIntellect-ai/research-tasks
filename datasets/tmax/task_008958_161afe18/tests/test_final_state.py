# test_final_state.py

import os
import zipfile
import tarfile
import tempfile
import shutil

def test_elf_list_file():
    log_file = "/home/user/elf_list.txt"
    assert os.path.exists(log_file), f"Log file {log_file} does not exist."
    with open(log_file, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_binaries = sorted(["app_bin", "echo_tool.dat", "ls_exe"])
    assert lines == expected_binaries, f"Expected {expected_binaries} in {log_file}, but got {lines}."

def test_binaries_archive_zip():
    zip_path = "/home/user/binaries_archive.zip"
    assert os.path.exists(zip_path), f"Zip archive {zip_path} does not exist."
    assert zipfile.is_zipfile(zip_path), f"File {zip_path} is not a valid zip archive."

    with zipfile.ZipFile(zip_path, "r") as z:
        namelist = z.namelist()
        # Verify files are at the root
        basenames = [os.path.basename(n) for n in namelist if not n.endswith('/')]
        expected_binaries = {"app_bin", "echo_tool.dat", "ls_exe"}
        assert expected_binaries.issubset(set(basenames)), f"Zip archive is missing some expected binaries. Found: {basenames}"

        # Ensure no full paths
        for n in namelist:
            if n in expected_binaries:
                assert "/" not in n, f"File {n} should be at the root of the zip archive, not in a subdirectory."

def test_workspace_clean_tarball():
    tar_path = "/home/user/workspace_clean.tar.bz2"
    assert os.path.exists(tar_path), f"Tarball {tar_path} does not exist."
    assert tarfile.is_tarfile(tar_path), f"File {tar_path} is not a valid tar archive."

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(tar_path, "r:bz2") as t:
            t.extractall(path=tmpdir)

        # Check that logs.txt exists and logs.txt.gz does not
        # The tarball might include the 'workspace' directory or just its contents.
        # Let's find logs.txt recursively.
        logs_txt_found = False
        logs_txt_gz_found = False
        old_macro_found = False
        new_macro_found = False
        elf_found = False

        for root, dirs, files in os.walk(tmpdir):
            for file in files:
                filepath = os.path.join(root, file)
                if file == "logs.txt":
                    logs_txt_found = True
                if file == "logs.txt.gz":
                    logs_txt_gz_found = True

                # Check for macros
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        if "OLD_MACRO_XYZ()" in content:
                            old_macro_found = True
                        if "NEW_MACRO_ABC()" in content:
                            new_macro_found = True
                except UnicodeDecodeError:
                    # Might be a binary file, check if it's an ELF
                    with open(filepath, "rb") as f:
                        header = f.read(4)
                        if header == b"\x7fELF":
                            elf_found = True

        assert logs_txt_found, "logs.txt was not found in the extracted tarball (should have been decompressed)."
        assert not logs_txt_gz_found, "logs.txt.gz should have been decompressed and removed."
        assert not old_macro_found, "Found OLD_MACRO_XYZ() in the workspace tarball. It should have been replaced."
        assert new_macro_found, "Did not find NEW_MACRO_ABC() in the workspace tarball."
        assert not elf_found, "Found an ELF binary in the workspace tarball. They should have been moved."

def test_workspace_no_elfs_and_macros_replaced():
    workspace_path = "/home/user/workspace"
    if not os.path.exists(workspace_path):
        return # Might have been cleaned up, but if it exists, check it.

    for root, dirs, files in os.walk(workspace_path):
        for file in files:
            filepath = os.path.join(root, file)
            # Check if it's an ELF
            with open(filepath, "rb") as f:
                header = f.read(4)
                assert header != b"\x7fELF", f"Found ELF binary {filepath} still in workspace."

            # Check text files for macro replacement
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    assert "OLD_MACRO_XYZ()" not in content, f"File {filepath} still contains OLD_MACRO_XYZ()."
            except UnicodeDecodeError:
                pass

def test_binaries_directory_contains_elfs():
    binaries_path = "/home/user/binaries"
    assert os.path.exists(binaries_path), f"Directory {binaries_path} does not exist."

    found_files = set(os.listdir(binaries_path))
    expected_files = {"app_bin", "echo_tool.dat", "ls_exe"}
    assert expected_files.issubset(found_files), f"Expected {expected_files} in {binaries_path}, got {found_files}."

    for file in expected_files:
        filepath = os.path.join(binaries_path, file)
        with open(filepath, "rb") as f:
            header = f.read(4)
            assert header == b"\x7fELF", f"File {filepath} is not an ELF binary."