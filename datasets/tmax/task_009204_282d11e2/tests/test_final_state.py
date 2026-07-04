# test_final_state.py
import os
import glob
import stat

REPORTS_DIR = "/home/user/reports"
MASTER_LOG = "/home/user/master_log.txt"
TOTAL_USAGE = "/home/user/total_usage.txt"
SCRIPT_PATH = "/home/user/aggregator.sh"

def test_no_bin_files():
    """Verify that all .bin files have been deleted from the reports directory."""
    bin_files = glob.glob(os.path.join(REPORTS_DIR, "*.bin"))
    assert len(bin_files) == 0, f"Found binary files that should have been deleted: {bin_files}"

def test_master_log_content():
    """Verify that the master log contains the extracted data in the correct format."""
    assert os.path.isfile(MASTER_LOG), f"{MASTER_LOG} does not exist."

    with open(MASTER_LOG, "r") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    expected_lines = {"ALPHA:1024", "BETA:2048", "GAMMA:512"}
    actual_lines = set(lines)

    missing = expected_lines - actual_lines
    assert not missing, f"master_log.txt is missing expected entries: {missing}"

    # We only check that the expected lines are present.
    for exp in expected_lines:
        assert exp in actual_lines, f"Expected '{exp}' in {MASTER_LOG}"

def test_total_usage_content():
    """Verify that the total usage file contains the correct sum."""
    assert os.path.isfile(TOTAL_USAGE), f"{TOTAL_USAGE} does not exist."

    with open(TOTAL_USAGE, "r") as f:
        content = f.read().strip()

    assert content == "3584", f"Expected total usage to be '3584', but got '{content}'"

def test_script_requirements():
    """Verify that the script exists, is executable, and contains required commands."""
    assert os.path.isfile(SCRIPT_PATH), f"{SCRIPT_PATH} does not exist."

    st = os.stat(SCRIPT_PATH)
    assert bool(st.st_mode & stat.S_IXUSR), f"{SCRIPT_PATH} is not executable."

    with open(SCRIPT_PATH, "r") as f:
        content = f.read()

    assert "flock" in content, "The script does not contain 'flock' for concurrent-safe aggregation."
    assert "mv" in content, "The script does not contain 'mv' for atomic summary update."