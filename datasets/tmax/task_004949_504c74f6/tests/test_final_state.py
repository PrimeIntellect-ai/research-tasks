# test_final_state.py

import os
import pytest

def test_go_program_exists():
    go_file = "/home/user/rename_elfs.go"
    assert os.path.exists(go_file), f"The Go program {go_file} does not exist."
    assert os.path.isfile(go_file), f"{go_file} is not a file."

def test_extracted_directory_contents():
    extracted_dir = "/home/user/extracted"
    assert os.path.exists(extracted_dir), f"The extracted directory {extracted_dir} does not exist."
    assert os.path.isdir(extracted_dir), f"{extracted_dir} is not a directory."

    files = os.listdir(extracted_dir)

    # Check notes.txt
    assert "notes.txt" in files, "notes.txt is missing from the extracted directory."

    # Check inner.zip is deleted
    assert "inner.zip" not in files, "inner.zip was not deleted from the extracted directory."

    # Find renamed ELF files
    sys_ls_renamed = [f for f in files if f.startswith("sys_ls_EM_") and f.endswith(".elf")]
    sys_cat_renamed = [f for f in files if f.startswith("sys_cat_EM_") and f.endswith(".elf")]

    assert len(sys_ls_renamed) == 1, "sys_ls was not properly renamed with its ELF architecture."
    assert len(sys_cat_renamed) == 1, "sys_cat was not properly renamed with its ELF architecture."

    # Check that the original sys_ls and sys_cat files do not exist
    assert "sys_ls" not in files, "The original sys_ls file was not renamed/removed."
    assert "sys_cat" not in files, "The original sys_cat file was not renamed/removed."