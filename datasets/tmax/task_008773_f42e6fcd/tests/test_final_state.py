# test_final_state.py

import os
import json
import struct
import pytest

INVENTORY_PATH = "/home/user/inventory.json"
BASE_DIR = "/home/user/project_dump"

def decompress_if_needed(data: bytes) -> bytes:
    """Decompress CRLE data if the magic header is present."""
    if data.startswith(b"CRLE"):
        decompressed = bytearray()
        i = 4
        while i + 1 < len(data):
            count = data[i]
            byte = data[i+1:i+2]
            decompressed.extend(byte * count)
            i += 2
        return bytes(decompressed)
    return data

def process_file(path: str) -> dict:
    """Extract metadata from a file according to the specifications."""
    with open(path, "rb") as f:
        data = f.read()

    data = decompress_if_needed(data)

    if data.startswith(b"\x7fELF"):
        if len(data) >= 0x18 + 8:
            val = struct.unpack_from("<Q", data, 0x18)[0]
            return {"type": "ELF", "metric": hex(val)}
    elif data.startswith(b"\x37\x7f\x06\x82") or data.startswith(b"\x37\x7f\x06\x83"):
        if len(data) >= 0x08 + 4:
            val = struct.unpack_from(">I", data, 0x08)[0]
            return {"type": "WAL", "metric": val}
    elif data.startswith(b"; FLAVOR:Marlin"):
        text = data.decode("utf-8", errors="ignore")
        count = sum(1 for line in text.splitlines() if line.startswith("G1 "))
        return {"type": "GCode", "metric": count}

    return None

def get_expected_inventory(base_dir: str) -> dict:
    """Dynamically compute the expected inventory from the actual files."""
    inventory = {}
    for root, _, files in os.walk(base_dir):
        for f in files:
            path = os.path.join(root, f)
            res = process_file(path)
            if res is not None:
                inventory[path] = res
    return inventory

def test_inventory_file_exists():
    assert os.path.isfile(INVENTORY_PATH), f"The output file {INVENTORY_PATH} was not created."

def test_inventory_file_is_valid_json():
    assert os.path.isfile(INVENTORY_PATH), "Inventory file missing."
    with open(INVENTORY_PATH, "r") as f:
        try:
            json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"The file {INVENTORY_PATH} does not contain valid JSON: {e}")

def test_inventory_contents_match():
    assert os.path.isfile(INVENTORY_PATH), "Inventory file missing."

    with open(INVENTORY_PATH, "r") as f:
        actual_inventory = json.load(f)

    expected_inventory = get_expected_inventory(BASE_DIR)

    assert isinstance(actual_inventory, dict), "The top-level JSON structure must be an object (dictionary)."

    # Check that all expected keys are present and values match
    for path, expected_data in expected_inventory.items():
        assert path in actual_inventory, f"Missing entry for file: {path}"
        actual_data = actual_inventory[path]
        assert actual_data.get("type") == expected_data["type"], f"Incorrect type for {path}. Expected {expected_data['type']}, got {actual_data.get('type')}"
        assert actual_data.get("metric") == expected_data["metric"], f"Incorrect metric for {path}. Expected {expected_data['metric']}, got {actual_data.get('metric')}"

    # Check for any extra unexpected keys
    extra_keys = set(actual_inventory.keys()) - set(expected_inventory.keys())
    assert not extra_keys, f"Found unexpected entries in the inventory: {extra_keys}"