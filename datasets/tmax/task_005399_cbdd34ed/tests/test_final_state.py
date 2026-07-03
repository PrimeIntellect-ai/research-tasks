# test_final_state.py
import os
import json
import pytest

def test_quarantined_files():
    quarantine_dir = "/home/user/quarantine"
    expected_quarantined = ["docB.tar", "docD.tar"]

    for filename in expected_quarantined:
        filepath = os.path.join(quarantine_dir, filename)
        assert os.path.isfile(filepath), f"Malicious archive {filename} was not moved to quarantine at {filepath}."

def test_extracted_docs_docA():
    docA_dir = "/home/user/extracted_docs/docA"
    assert os.path.isdir(docA_dir), f"Directory {docA_dir} does not exist."

    toc_path = os.path.join(docA_dir, "toc.csv")
    assert os.path.isfile(toc_path), f"File {toc_path} does not exist."

    chapter_path = os.path.join(docA_dir, "chapter1.md")
    assert os.path.isfile(chapter_path), f"File {chapter_path} does not exist."

    with open(chapter_path, "r") as f:
        content = f.read()

    assert "DRAFT" not in content, f"Found 'DRAFT' in {chapter_path}, text replacement failed."
    assert "FINAL" in content, f"Expected 'FINAL' in {chapter_path}, but it was not found."

def test_extracted_docs_docC():
    docC_dir = "/home/user/extracted_docs/docC"
    assert os.path.isdir(docC_dir), f"Directory {docC_dir} does not exist."

    toc_path = os.path.join(docC_dir, "toc.csv")
    assert os.path.isfile(toc_path), f"File {toc_path} does not exist."

    chapter_path = os.path.join(docC_dir, "chapter2.md")
    assert os.path.isfile(chapter_path), f"File {chapter_path} does not exist."

    with open(chapter_path, "r") as f:
        content = f.read()

    assert "DRAFT" not in content, f"Found 'DRAFT' in {chapter_path}, text replacement failed."
    assert "FINAL" in content, f"Expected 'FINAL' in {chapter_path}, but it was not found."

def test_processing_summary_json():
    summary_path = "/home/user/processing_summary.json"
    assert os.path.isfile(summary_path), f"Summary log {summary_path} does not exist."

    with open(summary_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {summary_path} is not valid JSON.")

    assert "processed" in data, "Key 'processed' missing in JSON summary."
    assert "quarantined" in data, "Key 'quarantined' missing in JSON summary."

    expected_processed = ["docA.tar", "docC.tar"]
    expected_quarantined = ["docB.tar", "docD.tar"]

    assert sorted(data["processed"]) == sorted(expected_processed), \
        f"Processed list in JSON {data['processed']} does not match expected {expected_processed}."

    assert sorted(data["quarantined"]) == sorted(expected_quarantined), \
        f"Quarantined list in JSON {data['quarantined']} does not match expected {expected_quarantined}."