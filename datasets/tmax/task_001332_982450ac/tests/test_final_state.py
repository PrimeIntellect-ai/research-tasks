# test_final_state.py
import os
import zipfile
import pytest

def test_clean_docs_zip_exists_and_valid():
    zip_path = "/home/user/clean_docs.zip"
    assert os.path.exists(zip_path), f"Expected {zip_path} to exist."
    assert zipfile.is_zipfile(zip_path), f"Expected {zip_path} to be a valid zip file."

def test_clean_docs_zip_contents():
    zip_path = "/home/user/clean_docs.zip"
    expected_files = {
        "set1.zip_doc1.txt": b"Welcome to OmniCorp. This is doc1.",
        "set1.zip_doc2.txt": b"OmniCorp provides great tools. OmniCorp is the best.",
        "set2.zip_docA.txt": b"Footer of OmniCorp doc."
    }

    with zipfile.ZipFile(zip_path, "r") as zf:
        actual_files = zf.namelist()
        assert set(actual_files) == set(expected_files.keys()), f"Zip contents do not match expected files. Found: {actual_files}"

        for filename, expected_content in expected_files.items():
            with zf.open(filename) as f:
                content = f.read()
                assert content == expected_content, f"Content of {filename} does not match expected output."

def test_migration_log():
    log_path = "/home/user/migration.log"
    assert os.path.exists(log_path), f"Expected {log_path} to exist."

    with open(log_path, "r", encoding="utf-8") as f:
        log_content = f.read()

    expected_line = "Migration complete. Processed 3 valid documents."
    assert expected_line in log_content, f"Expected log line '{expected_line}' not found in {log_path}."

def test_script_uses_atomic_rename():
    script_path = "/home/user/migrate_docs.py"
    assert os.path.exists(script_path), f"Expected script {script_path} to exist."

    with open(script_path, "r", encoding="utf-8") as f:
        script_content = f.read()

    has_atomic = any(func in script_content for func in ["os.replace", "os.rename", "shutil.move"])
    assert has_atomic, "Script does not appear to use an atomic rename operation (os.replace, os.rename, or shutil.move)."