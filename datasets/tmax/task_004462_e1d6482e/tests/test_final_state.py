# test_final_state.py

import os
import json
import pytest

def test_symlink_loops_intact():
    symlinks = {
        "/home/user/printing_dataset/batch_A/loop_dir": "/home/user/printing_dataset/batch_A",
        "/home/user/printing_dataset/batch_B/nested/root_loop": "/home/user/printing_dataset"
    }
    for link, target in symlinks.items():
        assert os.path.islink(link), f"Symlink missing or altered: {link}"
        assert os.readlink(link) == target, f"Symlink {link} points to wrong target"

def test_files_renamed_correctly():
    expected_renamed = [
        "/home/user/printing_dataset/batch_A/cube_12.4mm.gcode",
        "/home/user/printing_dataset/batch_A/sphere_55.0mm.gcode",
        "/home/user/printing_dataset/batch_B/cylinder_98.12mm.gcode",
    ]
    for f in expected_renamed:
        assert os.path.isfile(f), f"Expected renamed file missing: {f}"

    unexpected_originals = [
        "/home/user/printing_dataset/batch_A/cube.gcode",
        "/home/user/printing_dataset/batch_A/sphere.gcode",
        "/home/user/printing_dataset/batch_B/cylinder.gcode",
    ]
    for f in unexpected_originals:
        assert not os.path.exists(f), f"Original file should have been renamed but still exists: {f}"

def test_pyramid_unchanged():
    pyramid_path = "/home/user/printing_dataset/batch_B/nested/pyramid.gcode"
    assert os.path.isfile(pyramid_path), f"File without metadata should be unchanged: {pyramid_path}"

def test_json_summary():
    json_path = "/home/user/printing_summary.json"
    assert os.path.isfile(json_path), f"JSON summary missing: {json_path}"

    with open(json_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {json_path} is not valid JSON")

    expected_data = {
        "/home/user/printing_dataset/batch_A/cube_12.4mm.gcode": 12.4,
        "/home/user/printing_dataset/batch_A/sphere_55.0mm.gcode": 55.0,
        "/home/user/printing_dataset/batch_B/cylinder_98.12mm.gcode": 98.12
    }

    assert data == expected_data, f"JSON summary content is incorrect. Expected {expected_data}, got {data}"

def test_tmp_file_not_present():
    tmp_path = "/home/user/printing_summary.json.tmp"
    assert not os.path.exists(tmp_path), f"Temporary file {tmp_path} should not be present"