# test_final_state.py

import os
import json
import tarfile
import tempfile
import pytest

def test_metadata_json_content():
    metadata_path = "/home/user/metadata.json"
    assert os.path.isfile(metadata_path), f"File not found: {metadata_path}"

    with open(metadata_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            pytest.fail(f"File {metadata_path} is not valid JSON.")

    assert isinstance(data, list), f"{metadata_path} must contain a JSON array."

    expected_items = [
        {"file": "doc_sys.txt", "author": "Jean Dupont", "date": "2018-05-12"},
        {"file": "doc_net.txt", "author": "Marie Curie", "date": "2019-11-23"}
    ]

    assert len(data) == len(expected_items), f"Expected {len(expected_items)} items in {metadata_path}, got {len(data)}."

    # Order does not matter, so we can check if each expected item is in the data
    for item in expected_items:
        assert item in data, f"Expected metadata item {item} not found in {metadata_path}."

def test_final_archive_contents():
    archive_path = "/home/user/final_docs.tar.gz"
    assert os.path.isfile(archive_path), f"File not found: {archive_path}"
    assert tarfile.is_tarfile(archive_path), f"File {archive_path} is not a valid tar archive."

    with tarfile.open(archive_path, 'r:gz') as tar:
        names = tar.getnames()

        # Ensure no .csv or .tar.gz files are in the archive
        for name in names:
            assert not name.endswith('.csv'), f"Found CSV file in final archive: {name}"
            assert not name.endswith('.tar.gz'), f"Found tar.gz file in final archive: {name}"

        # Ensure metadata.json is in the archive
        metadata_found = any(os.path.basename(name) == 'metadata.json' for name in names)
        assert metadata_found, "metadata.json is missing from the final archive."

        # Find the text files
        doc_sys_members = [m for m in tar.getmembers() if os.path.basename(m.name) == 'doc_sys.txt']
        doc_net_members = [m for m in tar.getmembers() if os.path.basename(m.name) == 'doc_net.txt']

        assert doc_sys_members, "doc_sys.txt is missing from the final archive."
        assert doc_net_members, "doc_net.txt is missing from the final archive."

        # Check UTF-8 encoding and content
        with tar.extractfile(doc_sys_members[0]) as f:
            content = f.read()
            try:
                text = content.decode('utf-8')
                assert text == "Leçon un: L'intégration des systèmes.", "Content of doc_sys.txt does not match expected UTF-8 text."
            except UnicodeDecodeError:
                pytest.fail("doc_sys.txt in the final archive is not valid UTF-8.")

        with tar.extractfile(doc_net_members[0]) as f:
            content = f.read()
            try:
                text = content.decode('utf-8')
                assert text == "Leçon deux: Les réseaux et la sécurité.", "Content of doc_net.txt does not match expected UTF-8 text."
            except UnicodeDecodeError:
                pytest.fail("doc_net.txt in the final archive is not valid UTF-8.")