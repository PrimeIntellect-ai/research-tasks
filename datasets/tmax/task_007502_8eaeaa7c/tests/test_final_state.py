# test_final_state.py

import os
import pytest

def test_safe_backup_exists():
    """Verify that /home/user/safe_backup.txt exists."""
    assert os.path.isfile("/home/user/safe_backup.txt"), "/home/user/safe_backup.txt was not generated."

def test_safe_backup_contents():
    """Verify the contents of /home/user/safe_backup.txt."""
    with open("/home/user/safe_backup.txt", "rb") as f:
        content_bytes = f.read()

    # Must be valid UTF-8
    try:
        content_str = content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        pytest.fail("/home/user/safe_backup.txt does not contain valid UTF-8.")

    # Check included files
    assert "--- report1.log ---" in content_str, "report1.log was not included in the backup."
    assert "--- report2.log ---" in content_str, "report2.log was not included in the backup."

    # Check excluded files
    assert "tiny.log" not in content_str, "tiny.log should not be included (size < 50 bytes)."
    assert "ignore.txt" not in content_str, "ignore.txt should not be included (wrong extension)."

    # Check specific UTF-8 conversions
    assert "©" in content_str, "ISO-8859-1 '\\xA9' was not correctly converted to UTF-8 '©'."
    assert "æ" in content_str, "ISO-8859-1 '\\xE6' was not correctly converted to UTF-8 'æ'."

def test_c_source_exists_and_contents():
    """Verify that /home/user/archive_tool.c exists and contains required function calls."""
    source_file = "/home/user/archive_tool.c"
    assert os.path.isfile(source_file), f"{source_file} does not exist."

    with open(source_file, "r", encoding="utf-8", errors="ignore") as f:
        source_code = f.read()

    assert "flock" in source_code, f"{source_file} does not contain 'flock'."
    assert "iconv_open" in source_code, f"{source_file} does not contain 'iconv_open'."