# test_final_state.py

import os
import tarfile
import pytest

WORKSPACE_DIR = "/home/user/workspace"
LOG_FILE = os.path.join(WORKSPACE_DIR, "extraction_log.txt")
TAR_FILE = os.path.join(WORKSPACE_DIR, "clean_docs.tar.gz")
EXTRACTED_DOCS_DIR = os.path.join(WORKSPACE_DIR, "extracted_docs")

def test_extraction_log_exists_and_accurate():
    assert os.path.isfile(LOG_FILE), f"Log file missing at {LOG_FILE}"

    with open(LOG_FILE, "r") as f:
        log_content = f.read()

    assert "SKIPPED: ../secret_config.txt" in log_content, "Log did not correctly record the skipped malicious file."
    assert "EXTRACTED: docs/intro.txt" in log_content, "Log did not record extraction of docs/intro.txt."
    assert "EXTRACTED: docs/setup.txt" in log_content, "Log did not record extraction of docs/setup.txt."

def test_clean_docs_tar_exists_and_valid():
    assert os.path.isfile(TAR_FILE), f"Output tarball missing at {TAR_FILE}"
    assert tarfile.is_tarfile(TAR_FILE), f"File {TAR_FILE} is not a valid tar archive."

def test_clean_docs_tar_structure():
    with tarfile.open(TAR_FILE, "r:gz") as tf:
        names = tf.getnames()

        # Check for expected converted files
        assert any(n.endswith("docs/intro.md") for n in names), "docs/intro.md missing from the output tar archive."
        assert any(n.endswith("docs/setup.md") for n in names), "docs/setup.md missing from the output tar archive."

        # Ensure malicious file is NOT present
        assert not any("secret_config" in n for n in names), "Malicious file was incorrectly included in the output tar archive."

        # Ensure no .txt files are present in the tar
        assert not any(n.endswith(".txt") for n in names), "Legacy .txt files were incorrectly included in the output tar archive."

def test_clean_docs_tar_content_conversion():
    with tarfile.open(TAR_FILE, "r:gz") as tf:
        intro_member = None
        for m in tf.getmembers():
            if m.name.endswith("docs/intro.md"):
                intro_member = m
                break

        assert intro_member is not None, "Could not find docs/intro.md to check content."

        f = tf.extractfile(intro_member)
        assert f is not None, "Failed to read docs/intro.md from tar archive."

        content = f.read().decode('utf-8')
        assert "# Introduction" in content, "Legacy header '[HEADER]' was not properly converted to markdown '# '."
        assert "**very**" in content, "Legacy bolding '[B]...[/B]' was not properly converted to '**...**'."
        assert "[HEADER]" not in content, "Legacy header tag still present."
        assert "[B]" not in content and "[/B]" not in content, "Legacy bold tags still present."

def test_extracted_docs_cleanup():
    if os.path.isdir(EXTRACTED_DOCS_DIR):
        for root, dirs, files in os.walk(EXTRACTED_DOCS_DIR):
            for file in files:
                assert not file.endswith(".txt"), f"Legacy text file {file} was not deleted from {root} after conversion."