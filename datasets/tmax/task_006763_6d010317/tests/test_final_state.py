# test_final_state.py

import os
import json
import pytest

def test_shortest_path_json_exists_and_correct():
    filepath = "/home/user/shortest_path.json"

    assert os.path.isfile(filepath), f"File not found: {filepath}. Ensure your script generated the output file."

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError:
        pytest.fail(f"File {filepath} does not contain valid JSON.")

    expected_path = [
        "Warehouse_Alpha",
        "Hub_Beta",
        "Hub_Gamma",
        "Hub_Delta",
        "Store_Omega"
    ]
    expected_distance = 60

    assert "path" in data, f"Key 'path' is missing in the JSON output."
    assert "total_distance" in data, f"Key 'total_distance' is missing in the JSON output."

    assert data["path"] == expected_path, (
        f"The computed path is incorrect.\n"
        f"Expected: {expected_path}\n"
        f"Got: {data['path']}"
    )

    assert data["total_distance"] == expected_distance, (
        f"The computed total_distance is incorrect.\n"
        f"Expected: {expected_distance}\n"
        f"Got: {data['total_distance']}"
    )