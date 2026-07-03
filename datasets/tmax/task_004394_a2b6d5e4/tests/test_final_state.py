# test_final_state.py
import os
import glob
import pytest

def test_utf8_conversion():
    utf8_file = "/home/user/docs_utf8.json"
    assert os.path.exists(utf8_file), f"Converted file {utf8_file} does not exist."
    assert os.path.isfile(utf8_file), f"Path {utf8_file} is not a file."

    try:
        with open(utf8_file, "r", encoding="utf-8") as f:
            content = f.read()
            # The original file had 'Caf\xe9' in Windows-1252, which is 'Café' in UTF-8
            assert "Café" in content, f"Expected 'Café' not found in {utf8_file}. Conversion might be incorrect."
    except UnicodeDecodeError:
        pytest.fail(f"File {utf8_file} is not a valid UTF-8 encoded file.")

def test_symlink_validity_metric():
    tags_dir = "/home/user/dist/tags"
    assert os.path.exists(tags_dir), f"Tags directory {tags_dir} does not exist. Did you run the pipeline?"

    symlinks = glob.glob(f"{tags_dir}/**/*.md", recursive=True)

    assert len(symlinks) > 0, f"No symlinks found in {tags_dir}. The pipeline might have failed to generate output."

    valid_count = sum(1 for link in symlinks if os.path.exists(os.path.realpath(link)))
    score = (valid_count / len(symlinks)) * 100.0

    assert score >= 100.0, f"Symlink Validity Score is {score}%, expected >= 100.0%. Some symlinks are broken."