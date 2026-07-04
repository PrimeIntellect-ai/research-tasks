# test_final_state.py

import os
import subprocess
import re
import pytest

ORIG_FILE = '/app/artifact_feed.mp4'
TARGET_FILE = '/home/user/repository/releases/v2.0/main_artifact.mp4'
HARD_LINKS = [
    '/home/user/repository/stable/latest.mp4',
    '/home/user/repository/promoted/v2.mp4'
]
SYM_LINK = '/home/user/repository/experimental/beta.mp4'
MAX_SIZE = 2000000
SSIM_THRESHOLD = 0.92

def test_target_exists_and_size():
    """Check that the target file exists and respects the size constraint."""
    assert os.path.exists(TARGET_FILE), f"Target file missing at {TARGET_FILE}"
    assert os.path.isfile(TARGET_FILE), f"Target path {TARGET_FILE} is not a file"

    size = os.path.getsize(TARGET_FILE)
    assert size <= MAX_SIZE, f"Target file size {size} bytes exceeds the maximum allowed {MAX_SIZE} bytes."

def test_hard_links():
    """Check that the specified hard links exist and point to the same inode as the target."""
    assert os.path.exists(TARGET_FILE), f"Target file missing at {TARGET_FILE}"
    target_stat = os.stat(TARGET_FILE)

    for hl in HARD_LINKS:
        assert os.path.exists(hl), f"Hard link missing at {hl}"
        hl_stat = os.stat(hl)
        assert hl_stat.st_ino == target_stat.st_ino, f"File {hl} is not a hard link to {TARGET_FILE} (inode mismatch: {hl_stat.st_ino} != {target_stat.st_ino})"

def test_symlink():
    """Check that the specified symlink exists and uses the correct relative path."""
    assert os.path.islink(SYM_LINK), f"Symlink missing or not a symlink at {SYM_LINK}"

    target_read = os.readlink(SYM_LINK)
    expected_target = '../releases/v2.0/main_artifact.mp4'
    assert target_read == expected_target, f"Symlink at {SYM_LINK} points to '{target_read}', expected '{expected_target}'"

def test_ssim_metric():
    """Check that the SSIM between the original and optimized video is above the threshold."""
    assert os.path.exists(ORIG_FILE), f"Original file missing at {ORIG_FILE}"
    assert os.path.exists(TARGET_FILE), f"Target file missing at {TARGET_FILE}"

    cmd = ['ffmpeg', '-i', ORIG_FILE, '-i', TARGET_FILE, '-lavfi', 'ssim', '-f', 'null', '-']
    result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)

    match = re.search(r'All:\s*([0-9.]+)', result.stderr)
    assert match is not None, "Failed to parse SSIM output from ffmpeg."

    ssim = float(match.group(1))
    assert ssim >= SSIM_THRESHOLD, f"SSIM {ssim} is below the required threshold of {SSIM_THRESHOLD}."