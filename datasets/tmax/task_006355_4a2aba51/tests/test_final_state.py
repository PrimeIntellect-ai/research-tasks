# test_final_state.py

import os
import json
import tarfile
import pytest

def test_log_file_contents():
    """Test that the pipeline.log exists and contains the required log messages."""
    log_path = "/home/user/pipeline.log"
    assert os.path.isfile(log_path), f"Log file {log_path} does not exist."

    with open(log_path, "r") as f:
        log_content = f.read()

    expected_logs = [
        "Processing language en",
        "Exported 3 context groups for en",
        "Processing language es",
        "Imputed 2 missing keys for es",
        "Exported 3 context groups for es",
        "Processing language fr",
        "Imputed 4 missing keys for fr",
        "Exported 3 context groups for fr",
    ]

    for expected in expected_logs:
        assert expected in log_content, f"Expected log message '{expected}' not found in {log_path}."

def test_tarball_exists_and_valid():
    """Test that the tarball was created, transferred, and contains expected files."""
    tar_path = "/tmp/remote_l10n_dest/l10n_release.tar.gz"
    assert os.path.isfile(tar_path), f"Tarball {tar_path} does not exist."

    assert tarfile.is_tarfile(tar_path), f"File {tar_path} is not a valid tar file."

    with tarfile.open(tar_path, "r:gz") as tar:
        names = tar.getnames()
        # Check that it contains es/home.json or something similar
        # Depending on how it was archived, it might include the parent directory or just the contents.
        # We'll look for 'home.json' within an 'es' directory.
        found_es_home = any(name.endswith("es/home.json") for name in names)
        assert found_es_home, f"Tarball does not contain 'es/home.json'. Contents: {names}"

def test_processed_es_home_json():
    """Test the contents of the processed es/home.json file."""
    file_path = "/home/user/processed_l10n/es/home.json"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        data = json.load(f)

    expected_data = [
        {"id": "msg_error", "text": "Ocurrió un error."},
        {"id": "msg_welcome", "text": "[TBD] Welcome to our app!"}
    ]

    assert data == expected_data, f"Contents of {file_path} do not match expected data."

    # Check formatting (2-space indent)
    with open(file_path, "r") as f:
        content = f.read()
        assert "{\n  " in content or "{\n    " in content, f"File {file_path} does not appear to use 2-space indentation."

def test_processed_fr_nav_json():
    """Test the contents of the processed fr/nav.json file."""
    file_path = "/home/user/processed_l10n/fr/nav.json"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        data = json.load(f)

    expected_data = [
        {"id": "nav_profile", "text": "[TBD] Profile"}
    ]

    assert data == expected_data, f"Contents of {file_path} do not match expected data."

def test_processed_es_ui_json():
    """Test the contents of the processed es/ui.json file to ensure glossary imputation worked."""
    file_path = "/home/user/processed_l10n/es/ui.json"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        data = json.load(f)

    expected_data = [
        {"id": "btn_cancel", "text": "Cancelar"},
        {"id": "btn_ok", "text": "Aceptar"}
    ]

    assert data == expected_data, f"Contents of {file_path} do not match expected data."

def test_processed_fr_ui_json():
    """Test the contents of the processed fr/ui.json file."""
    file_path = "/home/user/processed_l10n/fr/ui.json"
    assert os.path.isfile(file_path), f"File {file_path} does not exist."

    with open(file_path, "r") as f:
        data = json.load(f)

    expected_data = [
        {"id": "btn_cancel", "text": "Annuler"},
        {"id": "btn_ok", "text": "D'accord"}
    ]

    assert data == expected_data, f"Contents of {file_path} do not match expected data."