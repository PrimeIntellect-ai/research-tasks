# test_final_state.py
import os
import stat

def test_doc_watcher_exists_and_executable():
    """Verify that the C++ source and compiled executable exist, and the latter is executable."""
    cpp_file = "/home/user/doc_watcher.cpp"
    exe_file = "/home/user/doc_watcher"

    assert os.path.isfile(cpp_file), f"Source file {cpp_file} does not exist."
    assert os.path.isfile(exe_file), f"Executable {exe_file} does not exist."

    st = os.stat(exe_file)
    assert bool(st.st_mode & stat.S_IXUSR), f"{exe_file} is not executable."

def test_organized_files():
    """Verify that the organized directory contains the correctly renamed files."""
    organized_dir = "/home/user/organized"
    assert os.path.isdir(organized_dir), f"{organized_dir} directory does not exist."

    expected_files = {
        "API_Setup_Alice_Smith.md",
        "Database_Config_Bob_Jones.md",
        "User_Auth_Alice_Smith.md"
    }

    actual_files = set(os.listdir(organized_dir))
    missing = expected_files - actual_files
    assert not missing, f"Expected files missing from {organized_dir}: {missing}"

def test_staging_directory_empty_of_drafts():
    """Verify that the staging directory no longer contains the original draft files."""
    staging_dir = "/home/user/staging"
    assert os.path.isdir(staging_dir), f"{staging_dir} directory does not exist."

    files = set(os.listdir(staging_dir))
    drafts = {"draft1.md", "draft2.md", "draft3.md"}
    remaining = drafts.intersection(files)
    assert not remaining, f"Draft files should have been moved from {staging_dir}, but found: {remaining}"

def test_final_listing_log():
    """Verify that final_listing.log contains the correct sorted filenames."""
    log_file = "/home/user/final_listing.log"
    assert os.path.isfile(log_file), f"{log_file} does not exist."

    with open(log_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "API_Setup_Alice_Smith.md",
        "Database_Config_Bob_Jones.md",
        "User_Auth_Alice_Smith.md"
    ]

    assert lines == expected_lines, f"Contents of {log_file} do not match expected output. Got: {lines}"