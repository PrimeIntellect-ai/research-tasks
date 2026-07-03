# test_final_state.py

import os
import tarfile
import pytest

TAR_PATH = "/home/user/backups/history.tar"

def test_history_tar_exists():
    """Check that the history.tar file exists."""
    assert os.path.isfile(TAR_PATH), f"Backup archive {TAR_PATH} does not exist."

def test_history_tar_valid_and_contains_diffs():
    """Check that history.tar is a valid tar file and contains the expected diffs."""
    assert tarfile.is_tarfile(TAR_PATH), f"{TAR_PATH} is not a valid tar archive."

    with tarfile.open(TAR_PATH, "r") as tar:
        names = tar.getnames()

    network_diffs = [n for n in names if "network.ini" in n and n.endswith(".diff")]
    assert len(network_diffs) >= 2, f"Expected at least 2 diff files for network.ini, found {len(network_diffs)}: {network_diffs}"

def test_diff_contents():
    """Extract the diffs and verify their contents are correct and in UTF-8."""
    with tarfile.open(TAR_PATH, "r") as tar:
        names = tar.getnames()
        network_diffs = [n for n in names if "network.ini" in n and n.endswith(".diff")]

        # Sort to get them in chronological order based on timestamp in filename
        network_diffs.sort()

        # Read the first two diffs
        try:
            diff1 = tar.extractfile(network_diffs[0]).read().decode('utf-8')
        except UnicodeDecodeError:
            pytest.fail("First diff is not valid UTF-8.")

        try:
            diff2 = tar.extractfile(network_diffs[1]).read().decode('utf-8')
        except UnicodeDecodeError:
            pytest.fail("Second diff is not valid UTF-8.")

    # Verify first diff (creation)
    assert "+server=192.168.1.1" in diff1, "First diff is missing the addition of 'server=192.168.1.1'."
    assert "+port=8080" in diff1, "First diff is missing the addition of 'port=8080'."

    # Verify second diff (modification)
    assert "+enable_ssl=true" in diff2, "Second diff is missing the addition of 'enable_ssl=true'."
    assert "server=192.168.1.1" in diff2, "Second diff is missing the context line 'server=192.168.1.1'."
    assert "port=8080" in diff2, "Second diff is missing the context line 'port=8080'."