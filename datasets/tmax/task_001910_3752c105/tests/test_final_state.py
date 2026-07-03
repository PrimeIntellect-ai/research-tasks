# test_final_state.py

import os
import json
import pytest

def test_extracted_docs_directory_exists():
    """Verify that the extracted_docs/drafts directory was created."""
    drafts_dir = "/home/user/extracted_docs/drafts"
    assert os.path.isdir(drafts_dir), f"Expected directory {drafts_dir} to exist."

def test_renamed_markdown_files():
    """Verify that the text files were properly renamed to markdown files."""
    drafts_dir = "/home/user/extracted_docs/drafts"
    assert os.path.isdir(drafts_dir), "Drafts directory missing."

    files = os.listdir(drafts_dir)

    expected_files = {
        "release_notes_v1.md",
        "api_spec_draft.md",
        "user_guide.md"
    }

    md_files = {f for f in files if f.endswith(".md")}
    txt_files = {f for f in files if f.endswith(".txt")}

    assert not txt_files, f"Found unexpected .txt files in {drafts_dir}: {txt_files}"
    assert md_files == expected_files, f"Expected markdown files {expected_files}, but found {md_files}"

def test_alice_commits_json_exists_and_valid():
    """Verify that alice_commits.json exists and contains the correct structured data."""
    json_path = "/home/user/alice_commits.json"
    assert os.path.isfile(json_path), f"Expected JSON file {json_path} to exist."

    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        pytest.fail(f"Failed to parse {json_path} as valid JSON: {e}")

    assert isinstance(data, list), "JSON output must be a list of objects."
    assert len(data) == 2, f"Expected exactly 2 commits by Alice Writer, found {len(data)}."

    # Expected data structure based on the truth log
    expected_data = [
        {
            "commit": "3c4d5e6",
            "date": "2023-10-11",
            "message": "Initial draft of API endpoints.\nFormatting fixes."
        },
        {
            "commit": "1d2e3f4",
            "date": "2023-10-14",
            "message": "Added Webhook documentation.\nFixed typos in overview.\nClarified rate limits."
        }
    ]

    for i, expected_entry in enumerate(expected_data):
        assert data[i].get("commit") == expected_entry["commit"], f"Entry {i} commit mismatch."
        assert data[i].get("date") == expected_entry["date"], f"Entry {i} date mismatch."
        assert data[i].get("message") == expected_entry["message"], f"Entry {i} message mismatch. Check indentation and newlines."