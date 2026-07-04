# test_final_state.py

import os
import json
import pytest

OUTPUT_DIR = "/home/user/output"
JSON_FILE = os.path.join(OUTPUT_DIR, "analysis_results.json")
PNG_FILE = os.path.join(OUTPUT_DIR, "dominant_abundance.png")

def test_output_directory_exists():
    """Test that the output directory exists."""
    assert os.path.isdir(OUTPUT_DIR), f"The output directory {OUTPUT_DIR} does not exist."

def test_json_file_exists():
    """Test that the analysis_results.json file exists."""
    assert os.path.isfile(JSON_FILE), f"The JSON file {JSON_FILE} does not exist."

def test_png_file_exists():
    """Test that the dominant_abundance.png file exists."""
    assert os.path.isfile(PNG_FILE), f"The PNG file {PNG_FILE} does not exist."

def test_png_file_is_valid():
    """Test that the PNG file has the correct magic bytes."""
    with open(PNG_FILE, "rb") as f:
        header = f.read(8)
    # PNG magic number is \x89PNG\r\n\x1a\n
    assert header == b"\x89PNG\r\n\x1a\n", f"The file {PNG_FILE} is not a valid PNG image."

def test_json_content():
    """Test that the JSON file contains the correct analysis results."""
    with open(JSON_FILE, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"The file {JSON_FILE} does not contain valid JSON.")

    expected_keys = {
        "largest_component_size",
        "dominant_sequence",
        "abundance_integral",
        "derivative_at_t_2"
    }

    assert set(data.keys()) == expected_keys, (
        f"The JSON file {JSON_FILE} does not have the exact expected keys. "
        f"Found: {list(data.keys())}, Expected: {list(expected_keys)}"
    )

    assert data["largest_component_size"] == 3, (
        f"Expected largest_component_size to be 3, got {data['largest_component_size']}."
    )

    assert data["dominant_sequence"] == "ACGTG", (
        f"Expected dominant_sequence to be 'ACGTG', got '{data['dominant_sequence']}'."
    )

    assert isinstance(data["abundance_integral"], (int, float)), "abundance_integral must be a float."
    assert round(data["abundance_integral"], 2) == 58.50, (
        f"Expected abundance_integral to be 58.50, got {data['abundance_integral']}."
    )

    assert isinstance(data["derivative_at_t_2"], (int, float)), "derivative_at_t_2 must be a float."
    assert round(data["derivative_at_t_2"], 2) == 1.00, (
        f"Expected derivative_at_t_2 to be 1.00, got {data['derivative_at_t_2']}."
    )