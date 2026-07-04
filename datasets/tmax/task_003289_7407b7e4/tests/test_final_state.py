# test_final_state.py

import os
import struct
import tarfile
import zipfile
import json
import requests
from io import BytesIO

def create_test_artifact(path: str):
    # 1. Create a fake ELF file
    elf_magic = b"\x7FELF\x01\x01\x01\x00"
    root_elf_data = elf_magic + b"root_elf_data"

    # 2. Create a nested zip containing another fake ELF file
    nested_elf_data = elf_magic + b"nested_elf_data"
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        zf.writestr("nested_elf", nested_elf_data)
    zip_data = zip_buffer.getvalue()

    # 3. Create a real text file
    txt_data = b"Hello world, this is a text file."

    # Package into payload.tar.gz
    tar_buffer = BytesIO()
    with tarfile.open(fileobj=tar_buffer, mode="w:gz") as tar:
        # root_elf
        info = tarfile.TarInfo(name="root_elf")
        info.size = len(root_elf_data)
        tar.addfile(info, BytesIO(root_elf_data))

        # text file
        info = tarfile.TarInfo(name="readme.txt")
        info.size = len(txt_data)
        tar.addfile(info, BytesIO(txt_data))

        # nested zip
        info = tarfile.TarInfo(name="archive.zip")
        info.size = len(zip_data)
        tar.addfile(info, BytesIO(zip_data))

    tar_gz_data = tar_buffer.getvalue()

    # Construct .artf
    magic = b"ARTF"
    payload_size = struct.pack("<I", len(tar_gz_data))

    artf_data = magic + payload_size + tar_gz_data

    with open(path, "wb") as f:
        f.write(artf_data)

def test_curate_endpoint_success():
    artifact_path = "/tmp/verifier_test.artf"
    create_test_artifact(artifact_path)

    url = "http://127.0.0.1:8888/curate"
    params = {
        "artifact": artifact_path,
        "token": "omega cipher nine"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.RequestException as e:
        assert False, f"Failed to connect to the service on port 8888: {e}"

    assert response.status_code == 200, f"Expected HTTP 200 OK, got {response.status_code}. Response: {response.text}"

    try:
        data = response.json()
    except ValueError:
        assert False, f"Response is not valid JSON: {response.text}"

    assert isinstance(data, list), "Expected a JSON array of filenames."

    expected_files = {"root_elf", "nested_elf"}
    actual_files = set(data)

    assert expected_files.issubset(actual_files) or actual_files == expected_files, \
        f"Expected JSON array to contain {expected_files}, but got {actual_files}"

def test_curate_endpoint_invalid_token():
    artifact_path = "/tmp/verifier_test.artf"
    if not os.path.exists(artifact_path):
        create_test_artifact(artifact_path)

    url = "http://127.0.0.1:8888/curate"
    params = {
        "artifact": artifact_path,
        "token": "wrong token"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.RequestException as e:
        assert False, f"Failed to connect to the service on port 8888: {e}"

    assert response.status_code == 401, f"Expected HTTP 401 Unauthorized for invalid token, got {response.status_code}"

def test_curate_endpoint_invalid_artifact():
    url = "http://127.0.0.1:8888/curate"
    params = {
        "artifact": "/tmp/non_existent_file.artf",
        "token": "omega cipher nine"
    }

    try:
        response = requests.get(url, params=params, timeout=5)
    except requests.RequestException as e:
        assert False, f"Failed to connect to the service on port 8888: {e}"

    assert response.status_code == 400, f"Expected HTTP 400 Bad Request for invalid artifact, got {response.status_code}"