# test_final_state.py

import os
import json
import glob
import subprocess
import tempfile
import pytest

def test_multipart_zip_exists():
    """Check that the multi-part zip files exist."""
    zip_path = "/home/user/archive_out/error_logs.zip"
    z01_path = "/home/user/archive_out/error_logs.z01"

    assert os.path.exists(zip_path), f"Expected multi-part zip file not found at {zip_path}"
    assert os.path.exists(z01_path), f"Expected multi-part split file not found at {z01_path}"

def test_zip_contents_and_json_format():
    """Reassemble the multi-part zip, extract, and verify the JSON files."""
    zip_path = "/home/user/archive_out/error_logs.zip"
    assert os.path.exists(zip_path), "Base zip file missing, cannot proceed with extraction."

    with tempfile.TemporaryDirectory() as tmpdir:
        single_zip = os.path.join(tmpdir, "single.zip")

        # Reassemble the multi-part zip using the zip command
        result = subprocess.run(
            ["zip", "-s", "0", zip_path, "--out", single_zip],
            cwd="/home/user/archive_out",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        assert result.returncode == 0, f"Failed to reassemble multi-part zip: {result.stderr.decode()}"

        # Extract the reassembled zip
        extract_dir = os.path.join(tmpdir, "extracted")
        os.makedirs(extract_dir)
        result = subprocess.run(
            ["unzip", single_zip, "-d", extract_dir],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        assert result.returncode == 0, f"Failed to extract reassembled zip: {result.stderr.decode()}"

        # Find all JSON files
        json_files = glob.glob(os.path.join(extract_dir, "**", "*_errors.json"), recursive=True)
        assert len(json_files) == 6, f"Expected exactly 6 JSON files, but found {len(json_files)}."

        # Verify JSON content
        expected_keys = {"timestamp", "level", "module", "message"}
        for jf in json_files:
            with open(jf, "r") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    pytest.fail(f"File {jf} contains invalid JSON.")

                assert isinstance(data, list), f"JSON root in {jf} must be an array."

                for i, item in enumerate(data):
                    assert isinstance(item, dict), f"Item at index {i} in {jf} is not an object."
                    assert set(item.keys()) == expected_keys, f"Incorrect keys in item {i} of {jf}. Expected {expected_keys}, got {set(item.keys())}."
                    assert item["level"] == "ERROR", f"Non-ERROR level found in item {i} of {jf}: {item['level']}"