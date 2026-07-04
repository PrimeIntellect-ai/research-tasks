# test_final_state.py

import os
import json
import base64
import tarfile
import tempfile
import pytest

def test_backup_json_files():
    backup_dir = "/home/user/backup"

    network_json_path = os.path.join(backup_dir, "backup_network.json")
    ui_json_path = os.path.join(backup_dir, "backup_ui.json")

    assert os.path.isfile(network_json_path), f"File {network_json_path} does not exist."
    assert os.path.isfile(ui_json_path), f"File {ui_json_path} does not exist."

    with open(network_json_path, "r") as f:
        try:
            network_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{network_json_path} is not valid JSON.")

    assert network_data.get("ip") == "192.168.1.100", f"Incorrect 'ip' in {network_json_path}."
    assert network_data.get("port") == "8080", f"Incorrect 'port' in {network_json_path}."
    assert network_data.get("protocol") == "tcp", f"Incorrect 'protocol' in {network_json_path}."

    with open(ui_json_path, "r") as f:
        try:
            ui_data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"{ui_json_path} is not valid JSON.")

    assert ui_data.get("theme") == "dark", f"Incorrect 'theme' in {ui_json_path}."
    assert ui_data.get("resolution") == "1920x1080", f"Incorrect 'resolution' in {ui_json_path}."

def test_archive_b64():
    archive_path = "/home/user/archive.b64"
    assert os.path.isfile(archive_path), f"File {archive_path} does not exist."

    with open(archive_path, "r") as f:
        b64_content = f.read().strip()

    try:
        tar_gz_data = base64.b64decode(b64_content)
    except Exception as e:
        pytest.fail(f"Failed to base64 decode {archive_path}: {e}")

    with tempfile.NamedTemporaryFile(delete=False) as tmp_tar:
        tmp_tar.write(tar_gz_data)
        tmp_tar_path = tmp_tar.name

    try:
        assert tarfile.is_tarfile(tmp_tar_path), "Decoded data is not a valid tar file."

        with tarfile.open(tmp_tar_path, "r:gz") as tar:
            names = tar.getnames()

            # Ensure no parent directories are included like 'backup/backup_network.json'
            # Expected files are just 'backup_network.json' and 'backup_ui.json'
            # Or they might be './backup_network.json'
            basenames = [os.path.basename(name) for name in names]

            assert "backup_network.json" in basenames, "backup_network.json not found in the tarball."
            assert "backup_ui.json" in basenames, "backup_ui.json not found in the tarball."

            # Ensure it's not nested inside a backup directory
            for name in names:
                assert "backup/" not in name, f"Tarball contains parent directory path: {name}"

            # Extract and check content
            with tempfile.TemporaryDirectory() as extract_dir:
                tar.extractall(path=extract_dir)

                # Find the extracted files
                extracted_network = None
                extracted_ui = None
                for root, dirs, files in os.walk(extract_dir):
                    if "backup_network.json" in files:
                        extracted_network = os.path.join(root, "backup_network.json")
                    if "backup_ui.json" in files:
                        extracted_ui = os.path.join(root, "backup_ui.json")

                assert extracted_network is not None, "Could not locate backup_network.json after extraction."
                assert extracted_ui is not None, "Could not locate backup_ui.json after extraction."

                with open(extracted_network, "r") as f:
                    net_data = json.load(f)
                    assert net_data.get("ip") == "192.168.1.100", "Extracted backup_network.json has incorrect content."

                with open(extracted_ui, "r") as f:
                    ui_data = json.load(f)
                    assert ui_data.get("theme") == "dark", "Extracted backup_ui.json has incorrect content."

    finally:
        os.remove(tmp_tar_path)