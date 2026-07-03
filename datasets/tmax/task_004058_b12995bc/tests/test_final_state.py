# test_final_state.py

import os
import tarfile
import tempfile
import requests
import pytest
import math

def get_expected_filenames(start, end):
    filenames = []
    for i in range(start, end + 1):
        event_code = i % 5
        sensor_val = int(i * 3.14)
        filenames.append(f"evt{event_code}_val{sensor_val}_frm{i}.jpg")
    return filenames

def test_c_files_exist():
    assert os.path.exists("/home/user/organize.c"), "/home/user/organize.c does not exist."
    assert os.path.exists("/home/user/server.c"), "/home/user/server.c does not exist."

def test_renamed_frames_exist():
    frames_dir = "/home/user/dataset/frames"
    assert os.path.isdir(frames_dir), f"Directory {frames_dir} does not exist."

    expected_files = get_expected_filenames(1, 100)
    actual_files = os.listdir(frames_dir)

    for expected in expected_files:
        assert expected in actual_files, f"Expected renamed file {expected} not found in {frames_dir}"

def test_server_base_backup():
    try:
        response = requests.get("http://127.0.0.1:8080/backups/base", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to server for base backup: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert "application/x-tar" in response.headers.get("Content-Type", ""), "Expected Content-Type: application/x-tar"

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    try:
        with tarfile.open(tmp_path, "r") as tar:
            members = tar.getnames()
            expected_files = get_expected_filenames(1, 50)
            for expected in expected_files:
                found = any(expected in member for member in members)
                assert found, f"Expected file {expected} not found in base_backup.tar"
    except tarfile.TarError:
        pytest.fail("Response body for base backup is not a valid tar archive.")
    finally:
        os.remove(tmp_path)

def test_server_diff_backup():
    try:
        response = requests.get("http://127.0.0.1:8080/backups/diff", timeout=5)
    except requests.RequestException as e:
        pytest.fail(f"Failed to connect to server for diff backup: {e}")

    assert response.status_code == 200, f"Expected status 200, got {response.status_code}"
    assert "application/x-tar" in response.headers.get("Content-Type", ""), "Expected Content-Type: application/x-tar"

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(response.content)
        tmp_path = tmp.name

    try:
        with tarfile.open(tmp_path, "r") as tar:
            members = tar.getnames()
            expected_files = get_expected_filenames(51, 100)
            for expected in expected_files:
                found = any(expected in member for member in members)
                assert found, f"Expected file {expected} not found in diff_backup.tar"
    except tarfile.TarError:
        pytest.fail("Response body for diff backup is not a valid tar archive.")
    finally:
        os.remove(tmp_path)