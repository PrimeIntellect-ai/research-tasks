# test_final_state.py
import os
import tarfile
import pytest

def test_published_docs_archive():
    archive_path = "/home/user/published_docs.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist. Did you run the Go program?"

    try:
        with tarfile.open(archive_path, "r:gz") as tar:
            members = tar.getnames()

            # 1. Expected files must be present
            assert "api/v1/endpoints.txt" in members, "api/v1/endpoints.txt is missing from the archive"
            assert "tutorials/getting_started.md" in members, "tutorials/getting_started.md is missing from the archive"

            # 2. Draft files must not be present
            assert "guide.md" not in members, "guide.md is marked as Draft and should not be in the archive"
            assert "api/v2/auth.md" not in members, "api/v2/auth.md is marked as Draft and should not be in the archive"
            assert "api/v2/auth.md.gz" not in members, "api/v2/auth.md.gz should not be in the archive"

            # 3. No .gz extensions should remain in the archive filenames
            for member in members:
                assert not member.endswith(".gz"), f"File {member} still has a .gz extension in the archive"

            # 4. Verify contents of the published files
            endpoints_f = tar.extractfile("api/v1/endpoints.txt")
            assert endpoints_f is not None, "Could not read api/v1/endpoints.txt from archive"
            endpoints_content = endpoints_f.read().decode("utf-8")
            assert "Status: Publish" in endpoints_content, "Missing 'Status: Publish' in api/v1/endpoints.txt"
            assert "GET /api/v1/status" in endpoints_content, "Missing expected content in api/v1/endpoints.txt"

            getting_started_f = tar.extractfile("tutorials/getting_started.md")
            assert getting_started_f is not None, "Could not read tutorials/getting_started.md from archive"
            getting_started_content = getting_started_f.read().decode("utf-8")
            assert "Status: Publish" in getting_started_content, "Missing 'Status: Publish' in tutorials/getting_started.md"

    except tarfile.ReadError:
        pytest.fail(f"{archive_path} is not a valid gzip-compressed tar archive")