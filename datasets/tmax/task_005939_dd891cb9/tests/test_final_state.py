# test_final_state.py

import os
import json

def test_final_docs_directory_exists():
    assert os.path.exists("/home/user/final_docs"), "Directory /home/user/final_docs/ does not exist."
    assert os.path.isdir("/home/user/final_docs"), "/home/user/final_docs/ is not a directory."

def test_expected_files_exist():
    expected_files = [
        "engineering_api_auth.md",
        "engineering_api_endpoints.md",
        "sales_pitch_contacts.md",
        "sales_pitch_deck.md"
    ]
    for filename in expected_files:
        filepath = os.path.join("/home/user/final_docs", filename)
        assert os.path.exists(filepath), f"Expected file {filepath} is missing."
        assert os.path.isfile(filepath), f"{filepath} is not a file."

def test_converted_file_contents():
    endpoints_path = "/home/user/final_docs/engineering_api_endpoints.md"
    deck_path = "/home/user/final_docs/sales_pitch_deck.md"

    with open(endpoints_path, "r") as f:
        endpoints_content = f.read()
    assert endpoints_content.startswith("# Original File: endpoints.txt\n\n"), f"File {endpoints_path} does not have the correct header."
    assert "GET /users\nPOST /users" in endpoints_content, f"File {endpoints_path} does not contain the original content."

    with open(deck_path, "r") as f:
        deck_content = f.read()
    assert deck_content.startswith("# Original File: deck.txt\n\n"), f"File {deck_path} does not have the correct header."
    assert "Slide 1: Intro\nSlide 2: Synergy" in deck_content, f"File {deck_path} does not contain the original content."

def test_manifest_json():
    manifest_path = "/home/user/manifest.json"
    assert os.path.exists(manifest_path), f"Manifest file {manifest_path} is missing."

    with open(manifest_path, "r") as f:
        try:
            manifest_data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"Manifest file {manifest_path} is not valid JSON."

    expected_list = [
        "/home/user/final_docs/engineering_api_auth.md",
        "/home/user/final_docs/engineering_api_endpoints.md",
        "/home/user/final_docs/sales_pitch_contacts.md",
        "/home/user/final_docs/sales_pitch_deck.md"
    ]

    assert isinstance(manifest_data, list), "Manifest JSON is not a list."
    assert manifest_data == expected_list, "Manifest JSON does not contain the expected sorted list of absolute paths."

def test_extracted_directory_cleanup():
    extracted_dir = "/home/user/extracted"
    assert os.path.exists(extracted_dir), f"Directory {extracted_dir} does not exist."

    for root, dirs, files in os.walk(extracted_dir):
        for file in files:
            assert not file.endswith(".zip"), f"Found zip file {file} in {root}."
            assert not file.endswith(".tar.gz"), f"Found tar.gz file {file} in {root}."
            assert not file.endswith(".txt"), f"Found txt file {file} in {root}."
            assert not file.endswith(".md"), f"Found md file {file} in {root}."