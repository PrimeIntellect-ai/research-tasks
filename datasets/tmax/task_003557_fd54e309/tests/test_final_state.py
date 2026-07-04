# test_final_state.py
import os
import pytest

def test_tmp_file_removed():
    """Test that the temporary file was atomically renamed and does not exist."""
    assert not os.path.exists("/home/user/critical_summary.tmp"), "/home/user/critical_summary.tmp should not exist."

def test_critical_summary_exists():
    """Test that the final output file exists."""
    assert os.path.isfile("/home/user/critical_summary.txt"), "/home/user/critical_summary.txt must exist."

def test_critical_summary_content():
    """Test that critical_summary.txt contains exactly the critical records."""
    block_node1 = """[CRITICAL] 2023-10-01 10:10:00
Disk space critically low on /dev/sda1
Immediate action required.
Dumping core state..."""

    block_node2 = """[CRITICAL] 2023-10-01 09:30:00
RAID array degraded!
Drive 3 failed.
Please replace drive 3 and rebuild."""

    with open("/home/user/critical_summary.txt", "r") as f:
        content = f.read().strip()

    # The order depends on directory iteration, so check both possible orderings
    option1 = f"{block_node1}\n{block_node2}"
    option2 = f"{block_node2}\n{block_node1}"

    assert content == option1 or content == option2, "The content of /home/user/critical_summary.txt does not match the expected extracted records."

def test_logs_directory_empty_of_logs():
    """Test that no .log files remain in the logs directory."""
    if os.path.isdir("/home/user/logs"):
        log_files = [f for f in os.listdir("/home/user/logs") if f.endswith(".log")]
        assert len(log_files) == 0, f"Found .log files left in /home/user/logs: {log_files}"

def test_archive_directory_contains_archived_files():
    """Test that the log files were moved and renamed correctly to the archive directory."""
    assert os.path.isfile("/home/user/archive/node1.archived"), "/home/user/archive/node1.archived does not exist."
    assert os.path.isfile("/home/user/archive/node2.archived"), "/home/user/archive/node2.archived does not exist."

def test_no_info_or_warn_in_summary():
    """Ensure no [INFO] or [WARN] tags leaked into the output."""
    with open("/home/user/critical_summary.txt", "r") as f:
        content = f.read()
    assert "[INFO]" not in content, "[INFO] tag found in critical_summary.txt"
    assert "[WARN]" not in content, "[WARN] tag found in critical_summary.txt"