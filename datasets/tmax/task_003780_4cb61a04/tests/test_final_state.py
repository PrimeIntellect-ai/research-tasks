# test_final_state.py
import os
import re

def test_extracted_files_exist():
    expected_files = ["doc1.txt", "doc2.txt", "doc3.txt"]
    for f in expected_files:
        path = os.path.join("/home/user/extracted_zips", f)
        assert os.path.isfile(path), f"Extracted file missing: {path}"

def test_doc_map_conf():
    conf_path = "/home/user/doc_map.conf"
    assert os.path.isfile(conf_path), f"Configuration file missing: {conf_path}"

    with open(conf_path, "r") as f:
        content = f.read()

    expected_mappings = [
        "/home/user/extracted_zips/doc1.txt=/home/user/final_docs/doc1.txt",
        "/home/user/extracted_zips/doc2.txt=/home/user/final_docs/doc2.txt",
        "/home/user/extracted_zips/doc3.txt=/home/user/final_docs/doc3.txt"
    ]

    for mapping in expected_mappings:
        assert mapping in content, f"Expected mapping '{mapping}' not found in {conf_path}"

def test_transformer_c_code():
    c_path = "/home/user/transformer.c"
    assert os.path.isfile(c_path), f"C program missing: {c_path}"

    with open(c_path, "r") as f:
        content = f.read()

    assert "mmap" in content, "C program does not use 'mmap'"
    assert "rename" in content, "C program does not use 'rename'"

def test_final_docs_content():
    expected_contents = {
        "doc1.txt": "Title: API v1\nStatus: [FINAL]\nThis is the [FINAL] documentation for API v1.\n",
        "doc2.txt": "Title: Architecture\nThis architecture document is currently a [FINAL].\n",
        "doc3.txt": "[FINAL] Release Notes\nNo major changes.\n"
    }

    for filename, expected_text in expected_contents.items():
        path = os.path.join("/home/user/final_docs", filename)
        assert os.path.isfile(path), f"Final document missing: {path}"

        with open(path, "r") as f:
            content = f.read()

        # Check that [DRAFT] is replaced with [FINAL]
        assert "[DRAFT]" not in content, f"Found '[DRAFT]' in {path}, should be replaced."
        assert "[FINAL]" in content, f"Expected '[FINAL]' not found in {path}."

        # Optional: check exact content match, stripping trailing newlines for safety
        assert content.strip() == expected_text.strip(), f"Content mismatch in {path}"