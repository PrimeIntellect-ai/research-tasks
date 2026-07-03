# test_final_state.py

import os
import base64
import pytest

def test_backup_custom_exists():
    assert os.path.isfile("/home/user/backup.custom"), "/home/user/backup.custom does not exist"

def test_utf8_files_exist_and_content():
    expected_files = {
        "/home/user/legacy_data/docs/menu.utf8.txt": "Café et croissant\n",
        "/home/user/legacy_data/docs/sky.utf8.txt": "Über den Wolken\n",
        "/home/user/legacy_data/logs/old/sys.utf8.log": "System error: Äquator\n",
        "/home/user/legacy_data/logs/boot.utf8.log": "Booting...\n",
        "/home/user/legacy_data/financial.utf8.dat": "Data: £100\n",
    }

    for path, expected_text in expected_files.items():
        assert os.path.isfile(path), f"Converted file {path} does not exist"
        with open(path, "rb") as f:
            content = f.read()
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            pytest.fail(f"File {path} is not valid UTF-8")

        assert expected_text.strip() in text, f"Content mismatch in {path}"

def test_backup_custom_content():
    archive_path = "/home/user/backup.custom"
    assert os.path.isfile(archive_path), f"Archive {archive_path} does not exist"

    with open(archive_path, "r", encoding="utf-8") as f:
        lines = f.read().splitlines()

    expected_files = {
        "docs/menu.utf8.txt": "Café et croissant\n",
        "docs/sky.utf8.txt": "Über den Wolken\n",
        "logs/old/sys.utf8.log": "System error: Äquator\n",
        "logs/boot.utf8.log": "Booting...\n",
        "financial.utf8.dat": "Data: £100\n",
    }

    parsed_files = {}
    current_file = None
    current_content = []

    for line in lines:
        if line.startswith("===FILE:") and line.endswith("==="):
            current_file = line[8:-3]
            current_content = []
        elif line == "===EOF===":
            if current_file is not None:
                parsed_files[current_file] = "".join(current_content)
                current_file = None
        else:
            if current_file is not None:
                current_content.append(line)

    for rel_path, expected_text in expected_files.items():
        assert rel_path in parsed_files, f"File {rel_path} missing in archive"

        b64_content = parsed_files[rel_path]
        try:
            decoded_bytes = base64.b64decode(b64_content)
            decoded_text = decoded_bytes.decode("utf-8")
        except Exception as e:
            pytest.fail(f"Failed to decode base64 content for {rel_path}: {e}")

        assert expected_text.strip() in decoded_text, f"Content mismatch in archive for {rel_path}"