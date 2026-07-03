# test_final_state.py
import os
import json
import zipfile

def test_raw_docs_extracted():
    assert os.path.exists("/home/user/raw_docs"), "/home/user/raw_docs directory does not exist. Extraction failed."
    assert os.path.isdir("/home/user/raw_docs"), "/home/user/raw_docs is not a directory."

def test_manifest_json():
    manifest_path = "/home/user/manifest.json"
    assert os.path.exists(manifest_path), f"Missing {manifest_path}"

    with open(manifest_path, "r", encoding="utf-8") as f:
        try:
            manifest = json.load(f)
        except json.JSONDecodeError:
            assert False, "manifest.json is not valid JSON."

    assert isinstance(manifest, list), "Manifest must be a JSON array."

    # Check sorting
    new_paths = [item.get("new_path", "") for item in manifest]
    assert new_paths == sorted(new_paths), "Manifest array is not sorted alphabetically by new_path."

    # Check expected files
    expected_files = {
        "/home/user/compiled_docs/api_reference/api_v1_endpoints.md": False,
        "/home/user/compiled_docs/archive/legacy_notes.txt": True,
        "/home/user/compiled_docs/installation/Setup_guide.md": False,
        "/home/user/compiled_docs/security/AUTH_flow.txt": False,
        "/home/user/compiled_docs/uncategorized/random_thoughts.txt": True
    }

    actual_files = {item.get("new_path"): item.get("was_converted") for item in manifest}

    for path, was_converted in expected_files.items():
        assert path in actual_files, f"Missing expected file in manifest: {path}"
        assert actual_files[path] == was_converted, f"Expected was_converted={was_converted} for {path}, got {actual_files[path]}"

def test_compiled_docs_content_and_encoding():
    compiled_dir = "/home/user/compiled_docs"
    assert os.path.exists(compiled_dir), f"{compiled_dir} does not exist."

    expected_paths = [
        "/home/user/compiled_docs/api_reference/api_v1_endpoints.md",
        "/home/user/compiled_docs/archive/legacy_notes.txt",
        "/home/user/compiled_docs/installation/Setup_guide.md",
        "/home/user/compiled_docs/security/AUTH_flow.txt",
        "/home/user/compiled_docs/uncategorized/random_thoughts.txt"
    ]

    for path in expected_paths:
        assert os.path.exists(path), f"Expected file missing in compiled_docs: {path}"

        # Check encoding by reading as utf-8
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            # Ensure no null bytes from UTF-16
            assert "\x00" not in content, f"File {path} appears to still be UTF-16 encoded (contains null bytes)."
        except UnicodeDecodeError:
            assert False, f"File {path} is not valid UTF-8."

def test_final_docs_zip():
    zip_path = "/home/user/final_docs.zip"
    assert os.path.exists(zip_path), f"Missing {zip_path}"
    assert zipfile.is_zipfile(zip_path), f"{zip_path} is not a valid zip file."

    with zipfile.ZipFile(zip_path, "r") as z:
        namelist = z.namelist()

        # Check if compiled_docs is in the zip
        compiled_docs_files = [n for n in namelist if "compiled_docs/" in n]
        assert len(compiled_docs_files) > 0, "Zip archive does not contain compiled_docs directory."

        # Ensure all expected files are in the zip
        expected_suffixes = [
            "compiled_docs/api_reference/api_v1_endpoints.md",
            "compiled_docs/archive/legacy_notes.txt",
            "compiled_docs/installation/Setup_guide.md",
            "compiled_docs/security/AUTH_flow.txt",
            "compiled_docs/uncategorized/random_thoughts.txt"
        ]

        for suffix in expected_suffixes:
            found = any(n.endswith(suffix) for n in namelist)
            assert found, f"Expected file ending with {suffix} not found in zip archive."