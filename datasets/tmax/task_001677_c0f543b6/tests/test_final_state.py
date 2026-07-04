# test_final_state.py
import os
import difflib
import pytest

def test_vulnerability_prevented():
    """Verify that the directory traversal vulnerability was fixed."""
    # If the vulnerability was not fixed, these files might exist based on the paths in the archive
    assert not os.path.exists("/home/user/evil.txt"), "Vulnerability not fixed: ../evil.txt was extracted to /home/user/evil.txt"
    assert not os.path.exists("/absolute_evil.txt"), "Vulnerability not fixed: /absolute_evil.txt was extracted"

    # Also check they are not inside the extracted directory literally
    assert not os.path.exists("/home/user/extracted/evil.txt"), "Malicious file evil.txt was extracted"
    assert not os.path.exists("/home/user/extracted/absolute_evil.txt"), "Malicious file absolute_evil.txt was extracted"

def test_safe_files_extracted():
    """Verify that safe files were properly extracted."""
    assert os.path.exists("/home/user/extracted/draft.txt"), "Safe file draft.txt was not extracted to /home/user/extracted/"
    assert os.path.exists("/home/user/extracted/safe_image.bin"), "Safe file safe_image.bin was not extracted to /home/user/extracted/"

def test_final_doc_metric():
    """Verify the final document content using the specified similarity metric."""
    final_doc_path = "/home/user/final_doc.txt"
    assert os.path.exists(final_doc_path), f"Final document not found at {final_doc_path}"

    expected = (
        "Documentation Draft v1.2\n"
        "Notes:\n"
        "the system architecture requires three redundant databases\n"
        "End of notes.\n"
    )

    with open(final_doc_path, 'r', encoding='utf-8') as f:
        actual = f.read()

    ratio = difflib.SequenceMatcher(None, expected.strip(), actual.strip()).ratio()
    assert ratio >= 0.90, f"Similarity Ratio {ratio:.4f} is below threshold 0.90. Actual content:\n{actual}"