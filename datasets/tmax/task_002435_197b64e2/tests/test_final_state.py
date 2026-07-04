# test_final_state.py

import os
import tarfile
import tempfile
import stat

def test_script_exists_and_executable():
    """Verify that the clean_dataset.sh script exists and is executable."""
    script_path = "/home/user/clean_dataset.sh"
    assert os.path.isfile(script_path), f"Script {script_path} does not exist."
    st = os.stat(script_path)
    assert bool(st.st_mode & stat.S_IXUSR), f"Script {script_path} is not executable."

def test_processed_archive_exists():
    """Verify that the final processed_dataset.tar.gz archive exists."""
    archive_path = "/home/user/processed_dataset.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."

def test_processed_archive_contents_and_transformations():
    """Extract the processed archive and verify its contents and the transformations."""
    archive_path = "/home/user/processed_dataset.tar.gz"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist."

    with tempfile.TemporaryDirectory() as tmpdir:
        with tarfile.open(archive_path, "r:gz") as tar:
            tar.extractall(path=tmpdir)

        # Check if chunks directory exists
        chunks_dir = None
        for root, dirs, files in os.walk(tmpdir):
            if "chunks" in dirs:
                chunks_dir = os.path.join(root, "chunks")
                break

        assert chunks_dir is not None, "Directory 'chunks' not found in the extracted archive."

        # Check the files in the chunks directory
        chunk_files = sorted(os.listdir(chunks_dir))
        expected_files = ["chunk_aa.txt", "chunk_ab.txt", "chunk_ac.txt"]

        # Filter out any non-files if necessary, but the task says *only* chunks dir and contents
        assert chunk_files == expected_files, f"Expected chunks {expected_files}, but found {chunk_files}."

        # Read contents of chunks
        all_lines = []
        for cf in expected_files:
            with open(os.path.join(chunks_dir, cf), "r") as f:
                lines = f.readlines()
                all_lines.extend(lines)

                if cf == "chunk_aa.txt":
                    assert len(lines) == 50, f"{cf} should have exactly 50 lines, found {len(lines)}."
                elif cf == "chunk_ab.txt":
                    assert len(lines) == 50, f"{cf} should have exactly 50 lines, found {len(lines)}."
                elif cf == "chunk_ac.txt":
                    assert len(lines) == 21, f"{cf} should have exactly 21 lines, found {len(lines)}."

        assert len(all_lines) == 121, f"Total lines across all chunks should be 121, found {len(all_lines)}."

        # Verify transformations
        for i, line in enumerate(all_lines):
            assert not line.startswith("ERROR"), f"Line {i+1} starts with 'ERROR': {line.strip()}"
            assert not line.startswith("DEBUG"), f"Line {i+1} starts with 'DEBUG': {line.strip()}"

            # Check for YYYY/MM/DD format (simplified check: just ensure no slashes in dates)
            # Since the original dates were 2023/XX/XX, we can check if "2023/" is present
            assert "2023/" not in line, f"Line {i+1} contains unconverted date format: {line.strip()}"
            assert "2023-" in line, f"Line {i+1} does not contain converted date format: {line.strip()}"

def test_symlinks_removed():
    """Verify that all symlinks in the extracted directory were removed."""
    extracted_dir = "/home/user/extracted"
    if os.path.isdir(extracted_dir):
        for root, dirs, files in os.walk(extracted_dir):
            for name in dirs + files:
                path = os.path.join(root, name)
                assert not os.path.islink(path), f"Symlink found at {path}, which should have been deleted."