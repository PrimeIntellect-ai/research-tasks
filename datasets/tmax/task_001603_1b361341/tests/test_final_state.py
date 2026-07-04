# test_final_state.py

import os
import pytest

def test_rejected_log():
    """Verify that the rejected.log file exists and contains the malicious path."""
    log_path = "/home/user/rejected.log"
    assert os.path.isfile(log_path), f"Rejected log missing at {log_path}"

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read().strip().splitlines()

    assert len(content) == 1, f"Expected exactly 1 rejected path, found {len(content)}"
    assert content[0] == "../etc/hacked.sh", f"Expected '../etc/hacked.sh' in rejected.log, got '{content[0]}'"

def test_file_a_restored_and_processed():
    """Verify file_a.txt is extracted, UTF-8, LF, and processed."""
    file_path = "/home/user/restored/file_a.txt"
    assert os.path.isfile(file_path), f"file_a.txt missing at {file_path}"

    with open(file_path, "rb") as f:
        raw_data = f.read()

    # Check for CRLF
    assert b"\r\n" not in raw_data, "file_a.txt still contains CRLF line endings"

    # Check for UTF-16LE BOM or null bytes
    assert b"\xff\xfe" not in raw_data[:2], "file_a.txt still contains UTF-16 BOM"
    assert b"\x00" not in raw_data, "file_a.txt appears to still be UTF-16 encoded (contains null bytes)"

    try:
        text = raw_data.decode("utf-8-sig") # handles optional BOM
    except UnicodeDecodeError:
        pytest.fail("file_a.txt is not valid UTF-8")

    assert "SERVER_LEGACY" not in text, "file_a.txt still contains 'SERVER_LEGACY'"
    assert "SERVER_MODERN" in text, "file_a.txt missing 'SERVER_MODERN'"
    assert "System Data" in text, "file_a.txt missing 'System Data'"

def test_file_b_restored_and_processed():
    """Verify dir/file_b.txt is extracted, UTF-8, LF, and processed."""
    file_path = "/home/user/restored/dir/file_b.txt"
    assert os.path.isfile(file_path), f"dir/file_b.txt missing at {file_path}"

    with open(file_path, "rb") as f:
        raw_data = f.read()

    # Check for CRLF
    assert b"\r\n" not in raw_data, "dir/file_b.txt still contains CRLF line endings"

    try:
        text = raw_data.decode("utf-8")
    except UnicodeDecodeError:
        pytest.fail("dir/file_b.txt is not valid UTF-8")

    assert "SERVER_LEGACY" not in text, "dir/file_b.txt still contains 'SERVER_LEGACY'"
    assert "SERVER_MODERN" in text, "dir/file_b.txt missing 'SERVER_MODERN'"
    assert "Start\nSERVER_MODERN\nEnd" in text, "dir/file_b.txt content does not match expected structure"

def test_malicious_file_not_extracted():
    """Verify that the malicious file was not extracted to the system or restored dir."""
    assert not os.path.exists("/etc/hacked.sh"), "Malicious file was extracted to /etc/hacked.sh"
    assert not os.path.exists("/home/user/restored/etc/hacked.sh"), "Malicious file was extracted to /home/user/restored/etc/hacked.sh"
    assert not os.path.exists("/home/user/etc/hacked.sh"), "Malicious file was extracted to /home/user/etc/hacked.sh"