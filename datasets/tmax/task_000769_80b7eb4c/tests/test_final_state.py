# test_final_state.py

import os
import json
import zipfile
import re
import pytest

def test_docs_cleaned_exists_and_watermarks_removed():
    cleaned_dir = "/home/user/docs_cleaned"
    assert os.path.isdir(cleaned_dir), f"Directory {cleaned_dir} does not exist"

    expected_files = ["docA.md", "docB.md"]
    for f in expected_files:
        filepath = os.path.join(cleaned_dir, f)
        assert os.path.isfile(filepath), f"File {filepath} is missing"

        with open(filepath, "r") as file:
            content = file.read()
            # Check that watermarks are removed
            assert not re.search(r'\[DRAFT_WATERMARK_[0-9]+\]', content), f"Watermark found in {filepath}"

def test_extractor_go_exists():
    go_file = "/home/user/extractor.go"
    assert os.path.isfile(go_file), f"Go program {go_file} does not exist"

def test_compiled_config_json():
    json_file = "/home/user/compiled_config.json"
    assert os.path.isfile(json_file), f"JSON file {json_file} does not exist"

    with open(json_file, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{json_file} is not valid JSON")

    expected_data = {
        "endpoint": "https://api.example.com/v1",
        "timeout": "30s",
        "retry_count": "5",
        "backoff_multiplier": "1.5"
    }

    # Convert all values to strings for robust comparison
    stringified_data = {k: str(v).strip() for k, v in data.items()}

    for key, value in expected_data.items():
        assert key in stringified_data, f"Key '{key}' missing from compiled JSON"
        assert stringified_data[key] == value, f"Value for '{key}' is incorrect. Expected '{value}', got '{stringified_data[key]}'"

def test_final_docs_zip():
    zip_path = "/home/user/final_docs.zip"
    assert os.path.isfile(zip_path), f"Zip file {zip_path} does not exist"

    with zipfile.ZipFile(zip_path, 'r') as zf:
        namelist = zf.namelist()

        expected_files = {"docA.md", "docB.md", "compiled_config.json"}
        actual_files = set(namelist)

        assert expected_files.issubset(actual_files), f"Zip file is missing expected files. Found: {actual_files}"

        # Ensure no parent directories are included (files should be at the root)
        for f in actual_files:
            assert "/" not in f and "\\" not in f, f"File {f} is not at the root of the zip archive"

        # Also verify watermarks are not in the zipped markdown files
        for md_file in ["docA.md", "docB.md"]:
            if md_file in actual_files:
                with zf.open(md_file) as f:
                    content = f.read().decode('utf-8')
                    assert not re.search(r'\[DRAFT_WATERMARK_[0-9]+\]', content), f"Watermark found in zipped {md_file}"