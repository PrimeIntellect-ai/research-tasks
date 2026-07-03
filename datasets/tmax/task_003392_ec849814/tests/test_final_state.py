# test_final_state.py

import os
import glob
import tempfile
import tarfile
import shutil
import subprocess
import pytest

def test_rust_program_exists():
    assert os.path.isfile("/home/user/backup_tool.rs"), "Rust source file /home/user/backup_tool.rs is missing."

def test_extracted_legacy_docs():
    legacy_dir = "/home/user/extracted_legacy/legacy_docs"
    assert os.path.isdir(legacy_dir), f"Directory {legacy_dir} does not exist."

    expected_files = ["draft_api.md", "draft_intro.md", "draft_setup.md"]
    for f in expected_files:
        assert os.path.isfile(os.path.join(legacy_dir, f)), f"Expected legacy file {f} is missing in {legacy_dir}."

def test_diff_docs_directory():
    diff_docs_dir = "/home/user/diff_docs"
    assert os.path.isdir(diff_docs_dir), f"Directory {diff_docs_dir} does not exist."

    assert os.path.isfile(os.path.join(diff_docs_dir, "prod_intro.md")), "prod_intro.md is missing in diff_docs."
    assert os.path.isfile(os.path.join(diff_docs_dir, "prod_faq.md")), "prod_faq.md is missing in diff_docs."

    assert not os.path.exists(os.path.join(diff_docs_dir, "prod_api.md")), "prod_api.md should not be in diff_docs (it was unchanged)."
    assert not os.path.exists(os.path.join(diff_docs_dir, "prod_setup.md")), "prod_setup.md should not be in diff_docs (it was deleted)."

def test_final_archive_and_chunks():
    final_archive_dir = "/home/user/final_archive"
    chunks = sorted(glob.glob(os.path.join(final_archive_dir, "diff.tar.gz.chunk_*")))

    assert len(chunks) > 0, "No chunks found in /home/user/final_archive with prefix diff.tar.gz.chunk_"

    for chunk in chunks[:-1]:
        size = os.path.getsize(chunk)
        assert size == 100, f"Chunk {chunk} has size {size}, expected 100 bytes."

    # Reassemble and test
    with tempfile.TemporaryDirectory() as tmpdir:
        reassembled_tar = os.path.join(tmpdir, "diff.tar.gz")
        with open(reassembled_tar, "wb") as outfile:
            for chunk in chunks:
                with open(chunk, "rb") as infile:
                    outfile.write(infile.read())

        assert tarfile.is_tarfile(reassembled_tar), "Reassembled file is not a valid tar archive."

        with tarfile.open(reassembled_tar, "r:gz") as tar:
            tar.extractall(path=tmpdir)

        extracted_diff_docs = os.path.join(tmpdir, "diff_docs")
        assert os.path.isdir(extracted_diff_docs), "Archive did not extract to a 'diff_docs' directory."

        prod_intro = os.path.join(extracted_diff_docs, "prod_intro.md")
        prod_faq = os.path.join(extracted_diff_docs, "prod_faq.md")

        assert os.path.isfile(prod_intro), "prod_intro.md missing in reassembled archive."
        assert os.path.isfile(prod_faq), "prod_faq.md missing in reassembled archive."

        assert not os.path.exists(os.path.join(extracted_diff_docs, "prod_api.md")), "prod_api.md should not be in the archive."
        assert not os.path.exists(os.path.join(extracted_diff_docs, "prod_setup.md")), "prod_setup.md should not be in the archive."

        with open(prod_intro, "r") as f:
            content = f.read()
            assert "Updated for v2.0." in content, "prod_intro.md does not contain the updated text."

        with open(prod_faq, "r") as f:
            content = f.read()
            assert "Q: How do I start?" in content, "prod_faq.md does not contain the expected FAQ text."