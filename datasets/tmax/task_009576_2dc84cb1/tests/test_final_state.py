# test_final_state.py

import os
import tarfile
import pytest

ARTIFACTS_DIR = "/home/user/artifacts"
BACKUP_ARCHIVE = "/home/user/artifacts_backup.tar.gz"

def test_loop_symlink_removed():
    loop_link = os.path.join(ARTIFACTS_DIR, "v3", "loop_link")
    assert not os.path.exists(loop_link) and not os.path.islink(loop_link), (
        f"The circular symlink {loop_link} should have been deleted."
    )

def test_valid_symlink_intact():
    latest_link = os.path.join(ARTIFACTS_DIR, "latest")
    assert os.path.islink(latest_link), f"The valid symlink {latest_link} should still exist."
    target = os.readlink(latest_link)
    expected_target = os.path.join(ARTIFACTS_DIR, "v3")
    # Tar might have preserved relative or absolute symlinks, but the file system one should be intact as is
    # Wait, the prompt says "Leave all other valid symlinks intact."
    assert target == expected_target or target == "v3", (
        f"The symlink {latest_link} should point to {expected_target} or 'v3'."
    )

def test_deduplication_hardlinks():
    v1_bin = os.path.join(ARTIFACTS_DIR, "v1", "app.bin")
    v2_bin = os.path.join(ARTIFACTS_DIR, "v2", "app.bin")
    v3_bin = os.path.join(ARTIFACTS_DIR, "v3", "app.bin")

    assert os.path.isfile(v1_bin), f"File {v1_bin} is missing."
    assert os.path.isfile(v2_bin), f"File {v2_bin} is missing."
    assert os.path.isfile(v3_bin), f"File {v3_bin} is missing."

    stat1 = os.stat(v1_bin)
    stat2 = os.stat(v2_bin)
    stat3 = os.stat(v3_bin)

    assert stat1.st_ino == stat2.st_ino, (
        f"{v1_bin} and {v2_bin} should be hardlinked (same inode) because they are identical."
    )

    assert stat1.st_ino != stat3.st_ino, (
        f"{v3_bin} should NOT be hardlinked to {v1_bin} because they have different contents."
    )

def test_backup_archive_exists_and_valid():
    assert os.path.isfile(BACKUP_ARCHIVE), f"Backup archive {BACKUP_ARCHIVE} does not exist."
    assert tarfile.is_tarfile(BACKUP_ARCHIVE), f"{BACKUP_ARCHIVE} is not a valid tar archive."

    with tarfile.open(BACKUP_ARCHIVE, "r:gz") as tar:
        names = tar.getnames()

        # Check for presence of required files, allowing for different prefix paths (e.g., artifacts/v1/app.bin or home/user/artifacts/v1/app.bin)
        def contains_path(ending):
            return any(name.endswith(ending) for name in names)

        assert contains_path("v1/app.bin"), f"Archive is missing v1/app.bin."
        assert contains_path("v2/app.bin"), f"Archive is missing v2/app.bin."
        assert contains_path("v3/app.bin"), f"Archive is missing v3/app.bin."
        assert contains_path("latest"), f"Archive is missing 'latest' symlink."
        assert not contains_path("v3/loop_link"), f"Archive should NOT contain the loop_link."