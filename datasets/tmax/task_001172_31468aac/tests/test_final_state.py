# test_final_state.py

import os
import tarfile

def test_recovered_pngs():
    recovered_dir = "/home/user/recovered_pngs"
    assert os.path.isdir(recovered_dir), f"Directory {recovered_dir} does not exist."

    files = set(os.listdir(recovered_dir))
    expected_files = {"image1.png", "image2.png"}

    assert files == expected_files, f"Expected exactly {expected_files} in {recovered_dir}, but found {files}."

    # Check magic bytes of recovered files
    for fname in expected_files:
        path = os.path.join(recovered_dir, fname)
        with open(path, "rb") as f:
            magic = f.read(8)
            assert magic == b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A", f"File {path} does not have valid PNG magic bytes."

def test_clean_csvs():
    clean_dir = "/home/user/clean_csvs"
    assert os.path.isdir(clean_dir), f"Directory {clean_dir} does not exist."

    files = set(os.listdir(clean_dir))
    expected_files = {"recent1.csv"}

    assert files == expected_files, f"Expected exactly {expected_files} in {clean_dir}, but found {files}."

    # Check encoding and content
    recent_csv = os.path.join(clean_dir, "recent1.csv")
    try:
        with open(recent_csv, "r", encoding="utf-8") as f:
            content = f.read()
            assert "René" in content, f"Expected string 'René' not found in {recent_csv}."
    except UnicodeDecodeError:
        assert False, f"File {recent_csv} is not properly UTF-8 encoded."

def test_bad_archives_log():
    log_file = "/home/user/bad_archives.log"
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist."

    with open(log_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = {
        "/home/user/research_data/bad1.tar.gz",
        "/home/user/research_data/subdir1/bad2.tar.gz"
    }

    assert set(lines) == expected_lines, f"Expected {expected_lines} in {log_file}, but found {set(lines)}."
    assert len(lines) == 2, f"Expected exactly 2 lines in {log_file}, but found {len(lines)}."

def test_no_infinite_loop_artifacts():
    # Ensure no files were copied from following the infinite loop
    # For instance, if they blindly copied, there might be deep directories
    loop_dir = "/home/user/research_data/infinite_loop"
    if os.path.islink(loop_dir):
        # We just want to make sure they didn't create duplicate files in recovered_pngs or clean_csvs
        # The exact file count checks in the previous tests already enforce this.
        pass