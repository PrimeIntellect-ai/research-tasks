# test_final_state.py

import os
import pytest

def test_tracker_source_exists():
    assert os.path.isfile("/home/user/tracker.rs"), "/home/user/tracker.rs does not exist."

def test_tracker_executable_exists():
    assert os.path.isfile("/home/user/tracker"), "/home/user/tracker executable does not exist."
    assert os.access("/home/user/tracker", os.X_OK), "/home/user/tracker is not executable."

def test_config_diff_out_exists():
    assert os.path.isfile("/home/user/config_diff.out"), "/home/user/config_diff.out does not exist."

def test_config_diff_out_contents():
    with open("/home/user/config_diff.out", "r") as f:
        content = f.read().strip()

    lines = [line.strip() for line in content.splitlines() if line.strip()]

    # Check that db.conf and cache.conf are not in the output
    assert "FILE: db.conf" not in lines, "db.conf should not be in the output as it is unchanged."
    assert "FILE: nested/cache.conf" not in lines, "nested/cache.conf should not be in the output as it is unchanged."
    assert "FILE: cache.conf" not in lines, "cache.conf should not be in the output as it is unchanged."

    # Verify app.conf
    assert "FILE: app.conf" in lines, "app.conf is missing from the output."
    app_idx = lines.index("FILE: app.conf")
    assert app_idx + 1 < len(lines), "Missing RLE content for app.conf."
    assert lines[app_idx + 1] == "5A5C", f"Incorrect RLE content for app.conf. Expected '5A5C', got '{lines[app_idx + 1]}'"

    # Verify new.conf
    assert "FILE: new.conf" in lines, "new.conf is missing from the output."
    new_idx = lines.index("FILE: new.conf")
    assert new_idx + 1 < len(lines), "Missing RLE content for new.conf."
    assert lines[new_idx + 1] == "3X3Y", f"Incorrect RLE content for new.conf. Expected '3X3Y', got '{lines[new_idx + 1]}'"

    # Ensure no extra files are reported
    file_lines = [line for line in lines if line.startswith("FILE:")]
    assert len(file_lines) == 2, f"Expected exactly 2 files in output, but found {len(file_lines)}: {file_lines}"