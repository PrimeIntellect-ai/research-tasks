# test_final_state.py

import os
import subprocess
import tempfile
import pytest

def test_clean_project_cgar_exists():
    """Test that the final archive was created."""
    archive_path = "/home/user/clean_project.cgar"
    assert os.path.isfile(archive_path), f"Output file {archive_path} is missing."
    assert os.path.getsize(archive_path) > 0, f"Output file {archive_path} is empty."

def test_clean_project_cgar_contents():
    """Test that the archive can be decompressed and contains the correct files with correct encoding."""
    archive_path = "/home/user/clean_project.cgar"
    assert os.path.isfile(archive_path), f"Output file {archive_path} is missing."

    with tempfile.TemporaryDirectory() as tmpdir:
        # Custom decompression pipeline: rev -> base64 -d -> gzip -d -> tar -xf
        cmd = f"cat {archive_path} | rev | base64 -d | gzip -d | tar -xf - -C {tmpdir}"
        result = subprocess.run(cmd, shell=True, capture_output=True)
        assert result.returncode == 0, f"Failed to decompress clean_project.cgar. Make sure it was created with the correct pipeline (tar -> gzip -> base64 -> rev). Error: {result.stderr.decode('utf-8', errors='ignore')}"

        clean_source_dir = os.path.join(tmpdir, "clean_source")
        assert os.path.isdir(clean_source_dir), "The 'clean_source' directory was not found inside the archive. Ensure you packaged the directory itself."

        fileA = os.path.join(clean_source_dir, "fileA.txt")
        fileB = os.path.join(clean_source_dir, "fileB.txt")
        fileC = os.path.join(clean_source_dir, "fileC.txt")

        assert os.path.isfile(fileA), "fileA.txt is missing from the clean_source directory in the archive."
        assert os.path.isfile(fileB), "fileB.txt is missing from the clean_source directory in the archive."
        assert not os.path.exists(fileC), "fileC.txt was found in the archive, but it should have been deleted because it failed the MD5 checksum verification."

        # Verify UTF-8 encoding and content
        try:
            with open(fileA, "r", encoding="utf-8") as f:
                contentA = f.read().strip()
        except UnicodeDecodeError:
            pytest.fail("fileA.txt is not valid UTF-8.")

        try:
            with open(fileB, "r", encoding="utf-8") as f:
                contentB = f.read().strip()
        except UnicodeDecodeError:
            pytest.fail("fileB.txt is not valid UTF-8.")

        assert contentA == "Привет, мир! Это файл A.", "fileA.txt content is incorrect after conversion."
        assert contentB == "Тестовая строка для файла B.", "fileB.txt content is incorrect after conversion."