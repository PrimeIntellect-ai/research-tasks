# test_final_state.py
import os

def test_unsafe_members_file():
    output_file = "/home/user/storage/unsafe_members.txt"
    assert os.path.isfile(output_file), f"Output file {output_file} is missing."

    with open(output_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected = ["logs/escape_hatch", "logs/system_passwd"]
    assert lines == expected, f"Output file contents do not match expected. Got: {lines}, Expected: {expected}"

def test_script_exists_and_uses_locking():
    script_file = "/home/user/validate_archive.py"
    assert os.path.isfile(script_file), f"Script file {script_file} is missing."

    with open(script_file, "r") as f:
        content = f.read()

    assert "fcntl" in content, "Script does not appear to import or use fcntl."
    assert "LOCK_SH" in content, "Script does not appear to use LOCK_SH for shared locking."