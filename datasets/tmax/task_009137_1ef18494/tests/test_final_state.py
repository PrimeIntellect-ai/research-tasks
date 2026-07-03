# test_final_state.py
import os
import json
import ast

def test_incoming_empty():
    incoming_dir = "/home/user/incoming"
    assert os.path.exists(incoming_dir), f"{incoming_dir} should still exist"
    files = os.listdir(incoming_dir)
    assert len(files) == 0, f"Expected {incoming_dir} to be empty, but found: {files}"

def test_repo_structure():
    expected_files = [
        "/home/user/repo/2023/10/B101.tar.gz",
        "/home/user/repo/2023/10/B102.tar.gz",
        "/home/user/repo/2023/11/B103.tar.gz",
        "/home/user/repo/2024/01/B104.tar.gz",
        "/home/user/repo/2024/02/B105.tar.gz"
    ]
    for path in expected_files:
        assert os.path.isfile(path), f"Expected artifact not found at {path}"

def test_manifest_content():
    manifest_path = "/home/user/repo/manifest.json"
    assert os.path.isfile(manifest_path), f"Manifest file missing at {manifest_path}"

    with open(manifest_path, "r") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            assert False, "manifest.json is not valid JSON"

    expected_data = [
        {"date": "2023-10-01", "build_id": "B101", "path": "/home/user/repo/2023/10/B101.tar.gz"},
        {"date": "2023-10-02", "build_id": "B102", "path": "/home/user/repo/2023/10/B102.tar.gz"},
        {"date": "2023-11-05", "build_id": "B103", "path": "/home/user/repo/2023/11/B103.tar.gz"},
        {"date": "2024-01-15", "build_id": "B104", "path": "/home/user/repo/2024/01/B104.tar.gz"},
        {"date": "2024-02-28", "build_id": "B105", "path": "/home/user/repo/2024/02/B105.tar.gz"}
    ]

    assert data == expected_data, f"Manifest content does not match expected.\nExpected: {expected_data}\nGot: {data}"

def test_atomic_write_in_code():
    script_path = "/home/user/curate.py"
    assert os.path.isfile(script_path), f"Script missing at {script_path}"

    with open(script_path, "r") as f:
        content = f.read()

    # Check for atomic replace/rename operations
    has_rename = "os.replace" in content or "os.rename" in content or "shutil.move" in content
    has_tmp = ".tmp" in content or "tmp" in content or "temp" in content

    assert has_rename and has_tmp, "Script does not appear to use an atomic write pattern (missing .tmp usage or os.replace/os.rename)."