# test_final_state.py

import os

def test_extracted_docs_content():
    doc1_path = '/home/user/extracted_docs/API_101_v1.txt'
    doc2_path = '/home/user/extracted_docs/Tutorial_202_v3.txt'

    assert os.path.isfile(doc1_path), f"Expected extracted document {doc1_path} is missing."
    assert os.path.isfile(doc2_path), f"Expected extracted document {doc2_path} is missing."

    with open(doc1_path, 'r') as f:
        content1 = f.read().strip()
    assert content1 == "This is the API documentation.", f"Content of {doc1_path} is incorrect. Got: {content1}"

    with open(doc2_path, 'r') as f:
        content2 = f.read().strip()
    assert content2 == "This is the Tutorial documentation.", f"Content of {doc2_path} is incorrect. Got: {content2}"

def test_no_extra_docs_extracted():
    extract_dir = '/home/user/extracted_docs'
    assert os.path.isdir(extract_dir), f"Extraction directory {extract_dir} does not exist."

    files = os.listdir(extract_dir)
    # Only the two expected files should be present
    assert len(files) == 2, f"Expected exactly 2 files in {extract_dir}, but found {len(files)}: {files}"

def test_summary_txt_content():
    summary_path = '/home/user/summary.txt'
    assert os.path.isfile(summary_path), f"Summary log file {summary_path} is missing."

    with open(summary_path, 'r') as f:
        lines = [line.strip() for line in f.read().strip().split('\n') if line.strip()]

    expected_lines = [
        "Extracted DocID 101 of Category API at Version 1",
        "Extracted DocID 202 of Category Tutorial at Version 3"
    ]

    assert lines == expected_lines, f"Content of {summary_path} does not match expected output. Got: {lines}"