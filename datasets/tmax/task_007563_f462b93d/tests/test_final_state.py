# test_final_state.py

import os
import zipfile
import pytest

def test_organize_go_exists_and_uses_flock():
    go_file = "/home/user/organize.go"
    assert os.path.exists(go_file), f"{go_file} does not exist."
    with open(go_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Flock" in content, f"{go_file} does not contain 'Flock' for file locking."

def test_final_docs_zip_exists_and_valid():
    zip_path = "/home/user/final_docs.zip"
    assert os.path.exists(zip_path), f"{zip_path} does not exist."
    assert zipfile.is_zipfile(zip_path), f"{zip_path} is not a valid zip file."

def test_zip_contents():
    zip_path = "/home/user/final_docs.zip"
    assert zipfile.is_zipfile(zip_path)

    with zipfile.ZipFile(zip_path, 'r') as zf:
        # Get all filenames in the zip, ignoring directory prefixes
        namelist = zf.namelist()
        basenames = [os.path.basename(name) for name in namelist if not name.endswith('/')]

        assert "doc_1.txt" in basenames, "doc_1.txt missing from zip archive."
        assert "doc_2.txt" in basenames, "doc_2.txt missing from zip archive."
        assert "manifest.log" in basenames, "manifest.log missing from zip archive."

        # Helper to find the exact path in the zip
        def get_zip_path(basename):
            for name in namelist:
                if os.path.basename(name) == basename:
                    return name
            return None

        # Check doc_1.txt
        doc1_path = get_zip_path("doc_1.txt")
        doc1_content = zf.read(doc1_path).decode('utf-8')
        assert "Café and Résumé" in doc1_content, "doc_1.txt content invalid or not converted to UTF-8 properly."

        # Check doc_2.txt
        doc2_path = get_zip_path("doc_2.txt")
        doc2_content = zf.read(doc2_path).decode('utf-8')
        assert "Jalapeño peppers" in doc2_content, "doc_2.txt content invalid or not converted to UTF-8 properly."

        # Check manifest.log
        manifest_path = get_zip_path("manifest.log")
        manifest_content = zf.read(manifest_path).decode('utf-8')
        assert "doc_1.txt - UTF8 Converted" in manifest_content, "manifest.log missing doc_1 entry."
        assert "doc_2.txt - UTF8 Converted" in manifest_content, "manifest.log missing doc_2 entry."