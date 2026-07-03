# test_final_state.py

import os
import gzip

def test_drafts_directory_empty_or_missing():
    drafts_dir = '/home/user/drafts'
    if os.path.exists(drafts_dir):
        assert os.path.isdir(drafts_dir), f"{drafts_dir} exists but is not a directory."
        files = os.listdir(drafts_dir)
        assert len(files) == 0, f"Expected {drafts_dir} to be empty, but found: {files}"

def test_final_docs_contains_renamed_files():
    final_docs_dir = '/home/user/final_docs'
    assert os.path.isdir(final_docs_dir), f"Directory {final_docs_dir} does not exist."

    expected_files = {
        "api_reference_v2.txt.gz",
        "user_guide_2023.txt.gz",
        "troubleshooting_network.txt.gz",
        "architecture_overview.txt.gz",
        "getting_started_intro.txt.gz"
    }

    actual_files = set(os.listdir(final_docs_dir))
    assert actual_files == expected_files, f"Expected files {expected_files} in {final_docs_dir}, but got {actual_files}"

    # Verify they are valid gzip files
    for filename in actual_files:
        filepath = os.path.join(final_docs_dir, filename)
        try:
            with gzip.open(filepath, 'rt') as f:
                f.readline()
        except Exception as e:
            assert False, f"File {filepath} is not a valid gzip file: {e}"

def test_rename_log_content():
    log_file = '/home/user/rename.log'
    assert os.path.isfile(log_file), f"Log file {log_file} does not exist."

    expected_log = (
        "draft_001.txt.gz -> api_reference_v2.txt.gz\n"
        "draft_002.txt.gz -> user_guide_2023.txt.gz\n"
        "draft_003.txt.gz -> troubleshooting_network.txt.gz\n"
        "draft_004.txt.gz -> architecture_overview.txt.gz\n"
        "draft_005.txt.gz -> getting_started_intro.txt.gz"
    )

    with open(log_file, 'r') as f:
        actual_log = f.read().strip()

    assert actual_log == expected_log.strip(), f"Content of {log_file} does not match expected output.\nExpected:\n{expected_log}\nGot:\n{actual_log}"