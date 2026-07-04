# test_final_state.py

import os
import gzip
import pytest

def test_deduplication_hard_links():
    """Check that identical files in raw_artifacts have been hard-linked."""
    raw_dir = "/home/user/raw_artifacts"

    # Group files by their intended content type
    file_a_prefix = "file_A_"
    file_b_prefix = "file_B_"
    doc_d_prefix = "doc_D_"

    inodes_a = set()
    inodes_b = set()
    inodes_d = set()

    for f in os.listdir(raw_dir):
        path = os.path.join(raw_dir, f)
        if not os.path.isfile(path) or os.path.islink(path):
            continue

        inode = os.stat(path).st_ino
        if f.startswith(file_a_prefix):
            inodes_a.add(inode)
        elif f.startswith(file_b_prefix):
            inodes_b.add(inode)
        elif f.startswith(doc_d_prefix):
            inodes_d.add(inode)

    # Each group should have exactly 1 unique inode if fully deduplicated
    assert len(inodes_a) == 1, f"Expected 1 unique inode for file_A_*, found {len(inodes_a)}. Hard linking incomplete."
    assert len(inodes_b) == 1, f"Expected 1 unique inode for file_B_*, found {len(inodes_b)}. Hard linking incomplete."
    assert len(inodes_d) == 1, f"Expected 1 unique inode for doc_D_*, found {len(inodes_d)}. Hard linking incomplete."

def test_metadata_compression():
    """Check that .meta.txt files are compressed to .meta.gz and originals removed."""
    raw_dir = "/home/user/raw_artifacts"

    meta_txt_files = [f for f in os.listdir(raw_dir) if f.endswith(".meta.txt")]
    assert len(meta_txt_files) == 0, f"Found uncompressed .meta.txt files: {meta_txt_files}. They should be removed."

    meta_gz_files = [f for f in os.listdir(raw_dir) if f.endswith(".meta.gz")]
    assert len(meta_gz_files) > 0, "No .meta.gz files found in raw_artifacts."

    inodes_c = set()
    for f in meta_gz_files:
        path = os.path.join(raw_dir, f)
        inodes_c.add(os.stat(path).st_ino)
        # Verify it's a valid gzip file
        try:
            with gzip.open(path, 'rb') as gz:
                gz.read(10)
        except Exception as e:
            pytest.fail(f"File {f} is not a valid gzip file: {e}")

    assert len(inodes_c) == 1, f"Expected 1 unique inode for meta_C_*.meta.gz, found {len(inodes_c)}. Hard linking incomplete."

def test_staging_directory_structure_and_symlinks():
    """Check that curated directory has correct structure and symlinks."""
    curated_dir = "/home/user/curated"

    for subdir in ["binaries", "docs", "metadata"]:
        path = os.path.join(curated_dir, subdir)
        assert os.path.isdir(path), f"Directory {path} is missing."

    binaries_dir = os.path.join(curated_dir, "binaries")
    docs_dir = os.path.join(curated_dir, "docs")
    metadata_dir = os.path.join(curated_dir, "metadata")

    # Check binaries
    for f in os.listdir(binaries_dir):
        path = os.path.join(binaries_dir, f)
        assert os.path.islink(path), f"{path} is not a symlink."
        assert f.endswith(".bin"), f"Found non-binary file {f} in binaries directory."

    # Check docs
    for f in os.listdir(docs_dir):
        path = os.path.join(docs_dir, f)
        assert os.path.islink(path), f"{path} is not a symlink."
        assert f.endswith(".doc"), f"Found non-doc file {f} in docs directory."

    # Check metadata
    for f in os.listdir(metadata_dir):
        path = os.path.join(metadata_dir, f)
        assert os.path.islink(path), f"{path} is not a symlink."
        assert f.endswith(".meta.gz"), f"Found non-meta.gz file {f} in metadata directory."

def test_final_archive_size_metric():
    """Check that the final archive size is within the threshold."""
    archive_path = "/home/user/final_archive.pack"

    assert os.path.isfile(archive_path), f"Final archive {archive_path} is missing."

    size = os.path.getsize(archive_path)
    threshold = 1800000

    assert size <= threshold, f"Archive size is {size} bytes, which exceeds the threshold of {threshold} bytes."