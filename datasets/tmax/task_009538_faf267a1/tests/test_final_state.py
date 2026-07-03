# test_final_state.py
import os
import json
import xml.etree.ElementTree as ET
import hashlib
import pytest

PROCESSED_DIR = "/home/user/processed"
SUMMARY_FILE = "/home/user/summary.json"

def test_processed_directory_exists_and_clean():
    """Test that the processed directory exists and contains no intermediate archives."""
    assert os.path.isdir(PROCESSED_DIR), f"Directory {PROCESSED_DIR} does not exist. Did you extract the archive?"

    # Check for intermediate archives
    for root, dirs, files in os.walk(PROCESSED_DIR):
        for file in files:
            assert not file.endswith(".zip"), f"Found intermediate zip file which should have been deleted: {os.path.join(root, file)}"
            assert not file.endswith(".tar.gz"), f"Found intermediate tar.gz file which should have been deleted: {os.path.join(root, file)}"

def test_summary_json_exists_and_valid():
    """Test that the summary.json file is created and is a valid JSON array."""
    assert os.path.isfile(SUMMARY_FILE), f"Summary file {SUMMARY_FILE} does not exist."
    try:
        with open(SUMMARY_FILE, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {SUMMARY_FILE} is not a valid JSON.")

    assert isinstance(data, list), f"JSON root must be an array, got {type(data).__name__}"

def test_summary_json_content():
    """Test that the summary.json contains the correctly computed data for valid trials."""
    expected = []

    # Dynamically compute expected results from the extracted files if available
    if os.path.isdir(PROCESSED_DIR):
        for root, dirs, files in os.walk(PROCESSED_DIR):
            if {"metadata.xml", "sensors.csv", "data.bin"}.issubset(set(files)):
                tree = ET.parse(os.path.join(root, "metadata.xml"))
                xml_root = tree.getroot()
                trial_id = xml_root.find("id").text.strip()
                valid = xml_root.find("valid").text.strip().lower() == "true"

                if not valid:
                    continue

                offset = int(xml_root.find("binary_offset").text.strip())
                length = int(xml_root.find("binary_length").text.strip())

                with open(os.path.join(root, "sensors.csv"), "r") as f:
                    lines = f.read().strip().split('\n')

                values = [float(line.split(',')[1]) for line in lines[1:] if line.strip()]
                avg = round(sum(values) / len(values), 2) if values else 0.0

                with open(os.path.join(root, "data.bin"), "rb") as f:
                    f.seek(offset)
                    chunk = f.read(length)

                expected.append({
                    "trial_id": trial_id,
                    "average_reading": avg,
                    "data_hash": hashlib.sha256(chunk).hexdigest()
                })

    expected.sort(key=lambda x: x["trial_id"])

    # Fallback to absolute truth if extraction failed or was incomplete (prevents false positives)
    if len(expected) != 2:
        expected = [
            {
                "trial_id": "Alpha_01",
                "average_reading": 20.33,
                "data_hash": "10ed805175e110b48b7f8dc721e2850982df4cc10b64af5d40a8309df58bbaea"
            },
            {
                "trial_id": "Gamma_03",
                "average_reading": 100.15,
                "data_hash": "a86241c09ebc713b946ebde4aa81395b066f1b3e4fce9d34e9e4f04e12e3e579"
            }
        ]

    assert os.path.isfile(SUMMARY_FILE), f"Cannot test content, {SUMMARY_FILE} is missing."
    with open(SUMMARY_FILE, "r") as f:
        actual = json.load(f)

    assert len(actual) == len(expected), f"Expected {len(expected)} valid trials in summary, got {len(actual)}"

    for i, (exp, act) in enumerate(zip(expected, actual)):
        assert act.get("trial_id") == exp["trial_id"], f"Mismatch in trial_id at index {i}. Expected {exp['trial_id']}, got {act.get('trial_id')}"
        assert act.get("average_reading") == exp["average_reading"], f"Mismatch in average_reading for {exp['trial_id']}. Expected {exp['average_reading']}, got {act.get('average_reading')}"
        assert act.get("data_hash") == exp["data_hash"], f"Mismatch in data_hash for {exp['trial_id']}. Expected {exp['data_hash']}, got {act.get('data_hash')}"