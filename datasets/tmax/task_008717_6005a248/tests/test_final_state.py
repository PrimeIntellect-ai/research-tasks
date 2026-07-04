# test_final_state.py

import os
import time
import subprocess
import pytest

def test_daemon_running():
    """Check if doc_daemon is running."""
    try:
        output = subprocess.check_output(["pgrep", "-f", "doc_daemon"]).decode("utf-8")
        assert output.strip(), "doc_daemon is not running in the background."
    except subprocess.CalledProcessError:
        pytest.fail("doc_daemon process not found.")

def test_daemon_processing():
    """Create a test file and verify the daemon processes it correctly."""
    watch_dir = "/home/user/doc_watch"
    processed_dir = "/home/user/doc_processed"
    test_file = os.path.join(watch_dir, "secret_manual.txt")

    # Create test file
    lines = [f"Line {i}\n" for i in range(1, 9)]
    with open(test_file, "w") as f:
        f.writelines(lines)

    # Wait for daemon to process
    time.sleep(3)

    # Check original file deleted
    assert not os.path.exists(test_file), f"Original file {test_file} was not deleted by the daemon."

    # Check output directory exists
    out_dir = os.path.join(processed_dir, "secret_manual")
    assert os.path.isdir(out_dir), f"Output directory {out_dir} was not created."

    # Check part_1.md
    part1 = os.path.join(out_dir, "part_1.md")
    assert os.path.exists(part1), f"{part1} does not exist."
    with open(part1, "r") as f:
        content = f.read().splitlines()
    assert len(content) == 3, f"part_1.md should have 3 lines, got {len(content)}."
    assert content == ["Line 1", "Line 2", "Line 3"], "part_1.md content is incorrect."

    # Check part_2.md
    part2 = os.path.join(out_dir, "part_2.md")
    assert os.path.exists(part2), f"{part2} does not exist."
    with open(part2, "r") as f:
        content = f.read().splitlines()
    assert len(content) == 3, f"part_2.md should have 3 lines, got {len(content)}."
    assert content == ["Line 4", "Line 5", "Line 6"], "part_2.md content is incorrect."

    # Check part_3.md
    part3 = os.path.join(out_dir, "part_3.md")
    assert os.path.exists(part3), f"{part3} does not exist."
    with open(part3, "r") as f:
        content = f.read().splitlines()
    assert len(content) == 2, f"part_3.md should have 2 lines, got {len(content)}."
    assert content == ["Line 7", "Line 8"], "part_3.md content is incorrect."

    # Check index.md
    index_file = os.path.join(out_dir, "index.md")
    assert os.path.exists(index_file), f"{index_file} does not exist."
    with open(index_file, "r") as f:
        index_content = f.read().strip()

    expected_index = f"{part1}\n{part2}\n{part3}"
    assert index_content == expected_index, f"index.md content is incorrect. Expected:\n{expected_index}\nGot:\n{index_content}"