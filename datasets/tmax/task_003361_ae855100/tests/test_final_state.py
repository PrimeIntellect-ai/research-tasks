# test_final_state.py
import os
import hashlib

def test_extract_go_exists():
    assert os.path.isfile("/home/user/extract.go"), "The Go source file /home/user/extract.go is missing."

def test_safe_extract_directory_exists():
    assert os.path.isdir("/home/user/safe_extract"), "The /home/user/safe_extract/ directory does not exist."

def test_extracted_files_content():
    expected_files = {
        "shadow": b"fake_shadow_data\n",
        "important.txt": b"hello world\n",
        "normal_file.dat": b"normal data\n"
    }

    for filename, expected_content in expected_files.items():
        filepath = os.path.join("/home/user/safe_extract", filename)
        assert os.path.isfile(filepath), f"The extracted file {filepath} is missing."

        with open(filepath, "rb") as f:
            content = f.read()
            assert content == expected_content, f"Content of {filepath} does not match expected data."

def test_manifest_file_content():
    manifest_path = "/home/user/manifest.txt"
    assert os.path.isfile(manifest_path), f"The manifest file {manifest_path} is missing."

    expected_manifest = (
        "a591a6d40bf420404a011733cfb7b190d62c65bf0bcda32b57b277d9ad9f146e  important.txt\n"
        "86bc6a686d0669b32e03ab52d8ccabfb7c3d4ee133bd55abf9b90c109720b0b8  normal_file.dat\n"
        "2ed8e1b1d9ed35bc0ec4948a47ff0f16f5c814b3dc0ceba4ea0d1df643c7bfe9  shadow\n"
    )

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest_content = f.read()

    assert manifest_content.strip() == expected_manifest.strip(), "The manifest file contents do not match the expected output or are not correctly sorted."