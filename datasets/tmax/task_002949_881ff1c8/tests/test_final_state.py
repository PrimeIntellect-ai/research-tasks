# test_final_state.py
import os
import tarfile
import pytest

def test_manifest_utf8_exists_and_encoding():
    manifest_path = "/home/user/artifacts/manifest_utf8.log"
    assert os.path.isfile(manifest_path), f"Manifest file {manifest_path} does not exist."

    try:
        with open(manifest_path, "rb") as f:
            content = f.read()
            decoded_content = content.decode("utf-8")
    except UnicodeDecodeError:
        pytest.fail(f"{manifest_path} is not valid UTF-8 encoded.")

    expected_strings = [
        "[Artifact]",
        "Temp-Name: bin_A192.tar.gz",
        "Real-Name: auth-service-1.0.tar.gz",
        "Temp-Name: bin_B834.tar.gz",
        "Real-Name: payment-gateway-2.1.tar.gz",
        "Temp-Name: bin_C771.tar.gz",
        "Real-Name: ui-components-3.4.tar.gz"
    ]
    for s in expected_strings:
        assert s in decoded_content, f"Expected string '{s}' not found in decoded UTF-8 manifest."

def test_renamed_archives_exist():
    expected_files = [
        "auth-service-1.0.tar.gz",
        "payment-gateway-2.1.tar.gz",
        "ui-components-3.4.tar.gz"
    ]
    for f in expected_files:
        path = os.path.join("/home/user/artifacts", f)
        assert os.path.isfile(path), f"Renamed archive {path} does not exist. Renaming might have failed."

def test_curated_artifacts_tar():
    tar_path = "/home/user/curated_artifacts.tar"
    assert os.path.isfile(tar_path), f"Tar archive {tar_path} does not exist."

    expected_files = {
        "auth-service-1.0.tar.gz",
        "payment-gateway-2.1.tar.gz",
        "ui-components-3.4.tar.gz"
    }

    try:
        with tarfile.open(tar_path, "r") as tar:
            members = tar.getnames()
    except tarfile.ReadError:
        pytest.fail(f"File {tar_path} is not a valid tar archive.")

    assert set(members) == expected_files, f"Tar archive contents {members} do not exactly match expected files {expected_files} at the root."

def test_final_list_txt():
    list_path = "/home/user/final_list.txt"
    assert os.path.isfile(list_path), f"List file {list_path} does not exist."

    with open(list_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    expected_lines = [
        "auth-service-1.0.tar.gz",
        "payment-gateway-2.1.tar.gz",
        "ui-components-3.4.tar.gz"
    ]

    assert lines == expected_lines, f"Contents of {list_path} do not match the expected sorted list of artifacts."