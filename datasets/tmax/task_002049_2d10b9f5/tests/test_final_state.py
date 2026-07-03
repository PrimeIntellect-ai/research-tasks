# test_final_state.py

import os
import uuid
import urllib.request
import urllib.error
import pytest

def post_multipart(url, file_path, field_name="file"):
    boundary = uuid.uuid4().hex
    with open(file_path, 'rb') as f:
        file_content = f.read()

    filename = os.path.basename(file_path)

    body = (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"{field_name}\"; filename=\"{filename}\"\r\n"
        f"Content-Type: text/csv\r\n\r\n"
    ).encode('utf-8') + file_content + f"\r\n--{boundary}--\r\n".encode('utf-8')

    req = urllib.request.Request(url, data=body)
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')

    try:
        with urllib.request.urlopen(req) as response:
            return response.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return 0

def test_detector_exists():
    detector_path = "/home/user/app/detector.py"
    assert os.path.isfile(detector_path), f"Detector script {detector_path} is missing."

def test_clean_corpus():
    clean_dir = "/home/user/data/clean/"
    assert os.path.isdir(clean_dir), f"Clean corpus directory {clean_dir} is missing."

    files = [f for f in os.listdir(clean_dir) if f.endswith('.csv')]
    assert len(files) > 0, "No clean corpus files found."

    failed_files = []
    for f in files:
        path = os.path.join(clean_dir, f)
        status = post_multipart("http://127.0.0.1:8080/upload", path)
        if status != 200:
            failed_files.append(f)

    assert not failed_files, f"{len(failed_files)} of {len(files)} clean modified/rejected: {failed_files}"

def test_evil_corpus():
    evil_dir = "/home/user/data/evil/"
    assert os.path.isdir(evil_dir), f"Evil corpus directory {evil_dir} is missing."

    files = [f for f in os.listdir(evil_dir) if f.endswith('.csv')]
    assert len(files) > 0, "No evil corpus files found."

    failed_files = []
    for f in files:
        path = os.path.join(evil_dir, f)
        status = post_multipart("http://127.0.0.1:8080/upload", path)
        if status != 400:
            failed_files.append(f)

    assert not failed_files, f"{len(failed_files)} of {len(files)} evil bypassed: {failed_files}"