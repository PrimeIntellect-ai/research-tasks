# test_final_state.py
import os

def test_success_elf_exists():
    """Check if the exploit successfully created /home/user/success.elf"""
    file_path = "/home/user/success.elf"
    assert os.path.exists(file_path), f"The file {file_path} does not exist. The exploit may have failed or not been executed."
    assert os.path.isfile(file_path), f"{file_path} is not a regular file."

def test_success_elf_magic_bytes():
    """Check if /home/user/success.elf starts with the correct ELF magic bytes"""
    file_path = "/home/user/success.elf"
    assert os.path.exists(file_path), f"The file {file_path} does not exist."

    with open(file_path, "rb") as f:
        header = f.read(4)

    assert header == b"\x7fELF", f"The file {file_path} does not start with the correct ELF magic bytes (\\x7fELF). Found: {header!r}"

def test_audit_script_exists():
    """Check if the user created the audit_upload.py script as requested"""
    script_path = "/home/user/audit_upload.py"
    assert os.path.exists(script_path), f"The script {script_path} was not created."
    assert os.path.isfile(script_path), f"{script_path} is not a regular file."