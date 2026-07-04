# test_final_state.py

import os
import json
import csv
import pytest

def test_registry_json_updated():
    registry_path = '/home/user/project_root/config/registry.json'
    assert os.path.isfile(registry_path), f"File {registry_path} is missing."

    with open(registry_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{registry_path} is not valid JSON.")

    assert "components" in data, "Key 'components' missing in registry.json"
    components = data["components"]

    # Check removed components
    assert "Network" not in components, "'Network' component was not removed from registry.json."
    assert "PhysicsEngine" not in components, "'PhysicsEngine' component was not removed from registry.json."

    # Check remaining components
    assert components.get("Logger") == "logger.cpp", "'Logger' component is missing or incorrect in registry.json."
    assert components.get("Database") == "db.cpp", "'Database' component is missing or incorrect in registry.json."
    assert components.get("Renderer") == "render.cpp", "'Renderer' component is missing or incorrect in registry.json."

def test_license_headers_updated():
    files_to_check = [
        '/home/user/project_root/src/core/logger.cpp',
        '/home/user/project_root/src/backend/db.cpp',
        '/home/user/project_root/src/frontend/render.cpp'
    ]

    for path in files_to_check:
        assert os.path.isfile(path), f"File {path} is missing."
        with open(path, 'r') as f:
            content = f.read()

        assert "/* LICENSE_UPDATED_2024 */" in content, f"License header not updated correctly in {path}."
        assert "/* TODO: UPDATE_LICENSE */" not in content, f"Old license header still present in {path}."

def test_final_manifest_csv():
    manifest_path = '/home/user/workspace/final_manifest.csv'
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} is missing. Did you run the C++ program and redirect its output?"

    expected_rows = [
        ['Component', 'Filename', 'AbsolutePath'],
        ['Database', 'db.cpp', '/home/user/project_root/src/backend/db.cpp'],
        ['Logger', 'logger.cpp', '/home/user/project_root/src/core/logger.cpp'],
        ['Renderer', 'render.cpp', '/home/user/project_root/src/frontend/render.cpp']
    ]

    actual_rows = []
    with open(manifest_path, 'r', newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # Ignore empty lines if any
                actual_rows.append(row)

    assert len(actual_rows) > 0, f"Manifest file {manifest_path} is empty."
    assert actual_rows[0] == expected_rows[0], f"CSV header is incorrect. Expected {expected_rows[0]}, got {actual_rows[0]}"

    # Ensure rows are sorted by Component name
    assert actual_rows == expected_rows, f"CSV content does not match expected output or is not sorted correctly. Expected:\n{expected_rows}\nGot:\n{actual_rows}"

def test_cpp_program_exists():
    cpp_path = '/home/user/workspace/build_manifest.cpp'
    assert os.path.isfile(cpp_path), f"C++ source file {cpp_path} is missing."