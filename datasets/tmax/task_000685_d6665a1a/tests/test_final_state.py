# test_final_state.py

import os
import pytest

def test_rotation_summary_exists():
    """Verify that the rotation_summary.txt file was created."""
    assert os.path.exists("/home/user/rotation_summary.txt"), (
        "The file /home/user/rotation_summary.txt does not exist. "
        "Make sure you created it in the correct location."
    )

def test_rotation_summary_content():
    """Verify that the rotation_summary.txt file has the correct content."""
    expected_lines = [
        "legacy_admin_token_xyz789",
        "rotated_successfully_abc123",
        "secure-rotation-endpoint.local"
    ]

    with open("/home/user/rotation_summary.txt", "r") as f:
        content = f.read().strip().splitlines()

    assert len(content) >= 3, "The rotation_summary.txt file must contain exactly three lines."

    assert content[0].strip() == expected_lines[0], (
        f"Line 1 is incorrect. Expected '{expected_lines[0]}', but got '{content[0].strip()}'."
    )

    assert content[1].strip() == expected_lines[1], (
        f"Line 2 is incorrect. Expected '{expected_lines[1]}', but got '{content[1].strip()}'."
    )

    assert content[2].strip() == expected_lines[2], (
        f"Line 3 is incorrect. Expected '{expected_lines[2]}', but got '{content[2].strip()}'."
    )

    assert len(content) == 3, "The rotation_summary.txt file should contain exactly three lines, but it has more."