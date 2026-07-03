# test_final_state.py

import os
import glob
import subprocess
import urllib.request
import urllib.error
import pytest

CLEAN_CORPUS_DIR = "/app/corpora/clean"
EVIL_CORPUS_DIR = "/app/corpora/evil"
DETECTOR_SCRIPT = "/home/user/detector.py"
UPLOAD_URL = "http://localhost:5000/upload"

def post_file(url, file_path):
    boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"

    with open(file_path, "rb") as f:
        file_data = f.read()

    filename = os.path.basename(file_path)

    body = (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"file\"; filename=\"{filename}\"\r\n"
        f"Content-Type: application/x-hdf5\r\n\r\n"
    ).encode('utf-8') + file_data + f"\r\n--{boundary}--\r\n".encode('utf-8')

    req = urllib.request.Request(url, data=body)
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')

    try:
        response = urllib.request.urlopen(req, timeout=5)
        return response.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:
        return None

def test_detector_script_exists():
    assert os.path.isfile(DETECTOR_SCRIPT), f"Detector script not found at {DETECTOR_SCRIPT}"

def test_detector_on_clean_corpus():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.h5"))
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []
    for fpath in clean_files:
        result = subprocess.run(
            ["python3", DETECTOR_SCRIPT, fpath],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if output != "CLEAN":
            failed_files.append(os.path.basename(fpath))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files modified/rejected (expected CLEAN). Offending files: {failed_files}"

def test_detector_on_evil_corpus():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.h5"))
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_files = []
    for fpath in evil_files:
        result = subprocess.run(
            ["python3", DETECTOR_SCRIPT, fpath],
            capture_output=True,
            text=True
        )
        output = result.stdout.strip()
        if output != "EVIL":
            failed_files.append(os.path.basename(fpath))

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil files bypassed (expected EVIL). Offending files: {failed_files}"

def test_api_clean_uploads():
    clean_files = glob.glob(os.path.join(CLEAN_CORPUS_DIR, "*.h5"))
    assert len(clean_files) > 0, "No clean corpus files found."

    failed_files = []
    for fpath in clean_files:
        status = post_file(UPLOAD_URL, fpath)
        if status != 200:
            failed_files.append((os.path.basename(fpath), status))

    assert not failed_files, f"{len(failed_files)} of {len(clean_files)} clean files failed to upload via API. Offending files and status codes: {failed_files}"

def test_api_evil_uploads():
    evil_files = glob.glob(os.path.join(EVIL_CORPUS_DIR, "*.h5"))
    assert len(evil_files) > 0, "No evil corpus files found."

    failed_files = []
    for fpath in evil_files:
        status = post_file(UPLOAD_URL, fpath)
        if status != 400:
            failed_files.append((os.path.basename(fpath), status))

    assert not failed_files, f"{len(failed_files)} of {len(evil_files)} evil files bypassed API validation. Offending files and status codes: {failed_files}"