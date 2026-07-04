# test_final_state.py
import os

def test_extracted_docs_directory_exists():
    """Test that the incoming_docs.tar.gz was extracted to the correct directory."""
    extracted_dir = "/home/user/extracted_docs"
    assert os.path.isdir(extracted_dir), f"The directory {extracted_dir} does not exist. Did you extract the archive?"
    assert os.path.isfile(os.path.join(extracted_dir, "doc_map.ini")), "doc_map.ini is missing from the extracted directory."

def test_doc_index_md_content():
    """Test that doc_index.md exists and contains the correct formatted output."""
    index_file = "/home/user/doc_index.md"
    assert os.path.exists(index_file), f"The file {index_file} does not exist."
    assert os.path.isfile(index_file), f"{index_file} is not a regular file."

    expected_content = (
        "- docs/api/v1.txt: API Version 1\n"
        "- docs/misc/readme.txt: General Readme\n"
    )

    with open(index_file, "r") as f:
        actual_content = f.read()

    # Strip trailing whitespace/newlines from both for a fair comparison, 
    # but ensure the lines are exactly as expected.
    actual_lines = [line.strip() for line in actual_content.strip().splitlines() if line.strip()]
    expected_lines = [line.strip() for line in expected_content.strip().splitlines() if line.strip()]

    assert actual_lines == expected_lines, (
        f"The content of {index_file} is incorrect.\n"
        f"Expected:\n{chr(10).join(expected_lines)}\n\n"
        f"Got:\n{chr(10).join(actual_lines)}"
    )