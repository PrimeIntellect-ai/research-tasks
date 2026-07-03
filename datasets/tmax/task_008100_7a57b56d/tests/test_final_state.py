# test_final_state.py
import os
import zipfile

def test_extracted_files_renamed_and_edited():
    extracted_dir = "/home/user/extracted_docs/legacy_docs"

    file1 = os.path.join(extracted_dir, "intro_guide.md")
    assert os.path.exists(file1), f"Expected file missing: {file1}"
    with open(file1, "r") as f:
        content = f.read()
        assert "Welcome to **[Deprecated Version]**." in content, f"Macro replacement failed in {file1}"

    file2 = os.path.join(extracted_dir, "api", "rest_spec.md")
    assert os.path.exists(file2), f"Expected file missing: {file2}"
    with open(file2, "r") as f:
        content = f.read()
        assert "API details for **[Deprecated Version]** here." in content, f"Macro replacement failed in {file2}"

    file3 = os.path.join(extracted_dir, "guides", "setup.md")
    assert os.path.exists(file3), f"Expected file missing: {file3}"
    with open(file3, "r") as f:
        content = f.read()
        assert "No macros here." in content, f"Unexpected content in {file3}"

def test_symlinks_deleted():
    extracted_dir = "/home/user/extracted_docs/legacy_docs"

    symlink1 = os.path.join(extracted_dir, "infinite_loop")
    assert not os.path.exists(symlink1) and not os.path.islink(symlink1), f"Symlink {symlink1} was not deleted"

    symlink2 = os.path.join(extracted_dir, "api", "recursive_guides")
    assert not os.path.exists(symlink2) and not os.path.islink(symlink2), f"Symlink {symlink2} was not deleted"

def test_clean_docs_zip():
    zip_path = "/home/user/clean_docs.zip"
    assert os.path.exists(zip_path), f"Zip file missing: {zip_path}"
    assert zipfile.is_zipfile(zip_path), f"File {zip_path} is not a valid zip archive"

    with zipfile.ZipFile(zip_path, 'r') as z:
        names = z.namelist()
        basenames = [os.path.basename(n) for n in names if not n.endswith('/')]

        assert "intro_guide.md" in basenames, "intro_guide.md missing from zip archive"
        assert "rest_spec.md" in basenames, "rest_spec.md missing from zip archive"
        assert "setup.md" in basenames, "setup.md missing from zip archive"

        assert "infinite_loop" not in basenames, "Symlink 'infinite_loop' should not be in zip archive"
        assert "recursive_guides" not in basenames, "Symlink 'recursive_guides' should not be in zip archive"

def test_cleanup_report():
    report_path = "/home/user/cleanup_report.txt"
    assert os.path.exists(report_path), f"Report file missing: {report_path}"

    with open(report_path, "r") as f:
        content = f.read().strip()
        assert content == "3", f"Expected report to contain exactly '3', got '{content}'"