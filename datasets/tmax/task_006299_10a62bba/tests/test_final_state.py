# test_final_state.py
import json
import os

def test_json_file_exists_and_valid():
    json_path = "/home/user/public_docs.json"
    assert os.path.exists(json_path), f"{json_path} does not exist."

    with open(json_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, f"{json_path} is not valid JSON."

    assert isinstance(data, list), "JSON root should be a list."
    assert len(data) == 2, f"Expected exactly 2 public records, got {len(data)}."

    # Check first record
    assert data[0].get("author") == "Alice Smith", "First record author is incorrect."
    assert data[0].get("date") == "2023-01-01", "First record date is incorrect."
    assert "public" in data[0].get("tags", []), "First record missing 'public' tag."
    assert data[0].get("content") == "This is the public API documentation.\nIt has multiple lines.", "First record content mismatch."

    # Check second record
    assert data[1].get("author") == "Charlie Brown", "Second record author is incorrect."
    assert data[1].get("date") == "2023-01-03", "Second record date is incorrect."
    assert "public" in data[1].get("tags", []), "Second record missing 'public' tag."
    assert data[1].get("content") == "How to setup the project.\n\nStep 1: Install.\nStep 2: Run.", "Second record content mismatch."

def test_rle_file_exists_and_matches_json():
    rle_path = "/home/user/public_docs.rle"
    json_path = "/home/user/public_docs.json"

    assert os.path.exists(rle_path), f"{rle_path} does not exist."
    assert os.path.exists(json_path), f"{json_path} does not exist."

    with open(rle_path, "rb") as f:
        rle_bytes = f.read()

    assert len(rle_bytes) > 0, f"{rle_path} is empty."
    assert len(rle_bytes) % 2 == 0, f"{rle_path} has an odd number of bytes, invalid RLE format."

    decoded = ""
    for i in range(0, len(rle_bytes), 2):
        count = rle_bytes[i]
        char = chr(rle_bytes[i+1])
        decoded += char * count

    with open(json_path, "r") as f:
        expected_json_str = f.read()

    assert decoded == expected_json_str, "Decoded RLE content does not exactly match the contents of public_docs.json."