# test_final_state.py

import os
import urllib.request
import urllib.error
import pytest

def post_file(url, file_path):
    boundary = "----BoundaryTest123456789"
    with open(file_path, "rb") as f:
        file_content = f.read()

    filename = os.path.basename(file_path)
    body = (
        f"--{boundary}\r\n"
        f"Content-Disposition: form-data; name=\"file\"; filename=\"{filename}\"\r\n"
        f"Content-Type: text/csv\r\n\r\n".encode('utf-8') +
        file_content +
        f"\r\n--{boundary}--\r\n".encode('utf-8')
    )

    req = urllib.request.Request(url, data=body)
    req.add_header('Content-Type', f'multipart/form-data; boundary={boundary}')

    try:
        response = urllib.request.urlopen(req, timeout=5)
        return response.getcode()
    except urllib.error.HTTPError as e:
        return e.code
    except urllib.error.URLError:
        return 0

def test_adversarial_corpus():
    clean_dir = '/app/corpus/clean/'
    evil_dir = '/app/corpus/evil/'
    url = 'http://127.0.0.1:8080/upload'

    assert os.path.isdir(clean_dir), f"{clean_dir} does not exist"
    assert os.path.isdir(evil_dir), f"{evil_dir} does not exist"

    clean_files = [os.path.join(clean_dir, f) for f in os.listdir(clean_dir) if os.path.isfile(os.path.join(clean_dir, f))]
    evil_files = [os.path.join(evil_dir, f) for f in os.listdir(evil_dir) if os.path.isfile(os.path.join(evil_dir, f))]

    assert len(clean_files) > 0, "No clean files found in corpus"
    assert len(evil_files) > 0, "No evil files found in corpus"

    bypassed_evil = []
    modified_clean = []

    for cf in clean_files:
        code = post_file(url, cf)
        if code != 200:
            modified_clean.append(os.path.basename(cf))

    for ef in evil_files:
        code = post_file(url, ef)
        if code != 400:
            bypassed_evil.append(os.path.basename(ef))

    error_msg = []
    if bypassed_evil:
        error_msg.append(f"{len(bypassed_evil)} of {len(evil_files)} evil bypassed: {', '.join(bypassed_evil)}")
    if modified_clean:
        error_msg.append(f"{len(modified_clean)} of {len(clean_files)} clean modified: {', '.join(modified_clean)}")

    if error_msg:
        pytest.fail(" | ".join(error_msg))