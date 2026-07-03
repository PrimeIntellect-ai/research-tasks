# test_final_state.py
import os
import zipfile

def test_release_docs_zip_exists():
    assert os.path.isfile("/home/user/release_docs.zip"), "Failed: /home/user/release_docs.zip does not exist"

def test_release_docs_zip_contents():
    zip_path = "/home/user/release_docs.zip"
    assert os.path.isfile(zip_path), "Failed: /home/user/release_docs.zip does not exist"

    with zipfile.ZipFile(zip_path, 'r') as z:
        file_list = z.namelist()

    # Exclude directory entries if any exist, though there shouldn't be any
    files_only = [f for f in file_list if not f.endswith('/')]

    expected_files = {
        "api_v1.0_endpoints.md",
        "core_v3.2_engine.md",
        "frontend_v1.5_buttons.md"
    }

    actual_files = set(files_only)

    # Check for missing expected files
    missing = expected_files - actual_files
    assert not missing, f"Failed: Missing expected files in zip: {missing}"

    # Check for unexpected files (e.g., draft or deprecated files)
    unexpected = actual_files - expected_files
    assert not unexpected, f"Failed: Zip contains unexpected files: {unexpected}"

    # Check that paths are flattened (no slashes in filenames)
    for f in actual_files:
        assert "/" not in f and "\\" not in f, f"Failed: Zip file contains directory paths '{f}'. Should be flattened."

def test_organizer_cpp_exists():
    cpp_path = "/home/user/organizer.cpp"
    assert os.path.isfile(cpp_path), f"Failed: C++ source file {cpp_path} does not exist"

def test_docs_workspace_exists():
    workspace_path = "/home/user/docs_workspace"
    assert os.path.isdir(workspace_path), f"Failed: Extracted directory {workspace_path} does not exist"