# test_final_state.py

import os
import time
import zipfile
import io
import requests
import pytest

def test_server_generates_backup():
    url = "http://127.0.0.1:8080/generate-backup"

    # Poll until server is up or timeout
    max_retries = 15
    response = None
    for _ in range(max_retries):
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            pass
        time.sleep(1)

    assert response is not None, "Failed to connect to the server or no response received."
    assert response.status_code == 200, f"Expected HTTP 200, got {response.status_code}"

    content_type = response.headers.get('Content-Type', '')
    assert 'application/zip' in content_type or 'application/x-zip-compressed' in content_type, \
        f"Expected Content-Type application/zip, got {content_type}"

    try:
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            namelist = z.namelist()

            # Check app.conf
            assert 'app.conf' in namelist, "app.conf missing from archive"
            with z.open('app.conf') as f:
                content = f.read().decode('utf-8').strip()
                assert content == "server=nginx", f"app.conf content mismatch: {content}"

            # Check db.conf
            assert 'db.conf' in namelist, "db.conf missing from archive"
            with z.open('db.conf') as f:
                content = f.read().decode('utf-8').strip()
                assert content == "db=postgres", f"db.conf content mismatch: {content}"

            # Check header.bin
            assert 'header.bin' in namelist, "header.bin missing from archive"
            with z.open('header.bin') as f:
                header_data = f.read()
                assert len(header_data) == 24, f"Expected header.bin to be exactly 24 bytes, got {len(header_data)}"

                with open('/app/surveillance.mp4', 'rb') as vf:
                    expected_header = vf.read(24)
                assert header_data == expected_header, "header.bin content does not match the first 24 bytes of the video"

            # Check frame_30.jpg
            assert 'frame_30.jpg' in namelist, "frame_30.jpg missing from archive"
            with z.open('frame_30.jpg') as f:
                frame30_data = f.read()
                assert len(frame30_data) > 0, "frame_30.jpg is empty"
                assert frame30_data.startswith(b'\xff\xd8'), "frame_30.jpg is not a valid JPEG"

            # Check frame_60.jpg
            assert 'frame_60.jpg' in namelist, "frame_60.jpg missing from archive"
            with z.open('frame_60.jpg') as f:
                frame60_data = f.read()
                assert len(frame60_data) > 0, "frame_60.jpg is empty"
                assert frame60_data.startswith(b'\xff\xd8'), "frame_60.jpg is not a valid JPEG"

    except zipfile.BadZipFile:
        pytest.fail("Response body is not a valid ZIP archive")

def test_backup_zip_on_disk():
    backup_path = '/home/user/backup.zip'
    assert os.path.isfile(backup_path), f"{backup_path} was not created on disk"
    assert os.path.getsize(backup_path) > 0, f"{backup_path} is empty"

    try:
        with zipfile.ZipFile(backup_path) as z:
            namelist = z.namelist()
            assert 'app.conf' in namelist, "app.conf missing from disk archive"
            assert 'db.conf' in namelist, "db.conf missing from disk archive"
            assert 'header.bin' in namelist, "header.bin missing from disk archive"
            assert 'frame_30.jpg' in namelist, "frame_30.jpg missing from disk archive"
            assert 'frame_60.jpg' in namelist, "frame_60.jpg missing from disk archive"
    except zipfile.BadZipFile:
        pytest.fail(f"{backup_path} is not a valid ZIP archive")