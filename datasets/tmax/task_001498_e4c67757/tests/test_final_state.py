# test_final_state.py
import os
import json
import pytest

def test_report_json():
    report_path = "/home/user/report.json"
    assert os.path.exists(report_path), "report.json was not generated."

    with open(report_path, "r") as f:
        try:
            report = json.load(f)
        except json.JSONDecodeError:
            pytest.fail("report.json is not valid JSON.")

    expected_keys = {"skipped_members", "extracted_files", "generated_md_files"}
    assert set(report.keys()) == expected_keys, f"report.json keys mismatch. Expected {expected_keys}, got {set(report.keys())}"

    assert report["skipped_members"] == 3, f"Expected 3 skipped_members, got {report['skipped_members']}"
    assert report["extracted_files"] == 3, f"Expected 3 extracted_files, got {report['extracted_files']}"
    assert report["generated_md_files"] == 3, f"Expected 3 generated_md_files, got {report['generated_md_files']}"

def test_markdown_files():
    md_dir = "/home/user/docs_md"
    assert os.path.exists(md_dir), "docs_md directory does not exist."
    assert os.path.isdir(md_dir), "docs_md is not a directory."

    expected_files = {
        "API_Reference.md": "# API Reference\n\nThis is the API reference documentation.\n",
        "User_Guide.md": "# User Guide\n\nWelcome to the user guide.\n",
        "Release_Notes.md": "# Release Notes\n\nVersion 2.0 released.\n"
    }

    for filename, expected_content in expected_files.items():
        filepath = os.path.join(md_dir, filename)
        assert os.path.exists(filepath), f"Expected markdown file {filename} is missing."

        with open(filepath, "r") as f:
            content = f.read()

        assert content.strip() == expected_content.strip(), f"Content mismatch in {filename}.\nExpected:\n{expected_content}\nGot:\n{content}"

def test_raw_docs_extraction():
    raw_dir = "/home/user/docs_raw"
    assert os.path.exists(raw_dir), "docs_raw directory does not exist."
    assert os.path.isdir(raw_dir), "docs_raw is not a directory."

    expected_files = {"valid_json.json", "valid_csv.csv", "valid_xml.xml"}
    extracted_files = set(os.listdir(raw_dir))

    assert expected_files.issubset(extracted_files), f"Expected files {expected_files} missing from docs_raw. Found: {extracted_files}"

    # Check that malicious files were not extracted
    malicious_names = {"evil_relative.txt", "evil_absolute.txt", "evil_trick.txt", "evil.txt"}
    for mal in malicious_names:
        assert mal not in extracted_files, f"Malicious file {mal} was extracted to docs_raw!"

def test_no_tar_slip():
    # Check that malicious files did not escape to /home/user or /home
    paths_to_check = [
        "/home/user/evil_relative.txt",
        "/home/user/evil_absolute.txt",
        "/home/user/evil_trick.txt",
        "/home/evil_relative.txt",
        "/home/evil_absolute.txt",
        "/home/evil_trick.txt"
    ]

    for path in paths_to_check:
        assert not os.path.exists(path), f"Tar slip vulnerability detected! Malicious file extracted to {path}"